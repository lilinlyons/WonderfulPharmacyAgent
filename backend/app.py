import os
import time
from fastapi import FastAPI, Request, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum

from agents.agent_utils.session_state import (
    get_conversation_context,
    set_user_message,
    set_agent_message,
)
from agents.agent_utils.rephrase_question import rephrase_with_session_context

from agents.context_agent import ContextAgent
from agents.execution_agent import ExecutionAgent
from agents.intent_agent import IntentAgent

from utils.prescription.get_prescriptions_per_user import get_prescription_per_user
from utils.support.get_support_per_user import get_support_per_user
from utils.prescription.get_all_prescription_requests import get_all_prescription_requests
from utils.support.get_all_support_requests import get_all_support_requests
from utils.medication.get_medications_sold import get_medications_sold
from utils.db.db import conn
from utils.prescription.update_prescription_request_status import update_prescription_request_status
from utils.support.update_support_request_status import update_support_request_status
from utils.users.get_user_by_id import get_user_by_id
from utils.users.fetch_users import fetch_users

from bert.labels import Intent
from agents.agent_utils.policy_prompt import SYSTEM_PROMPT
from utils.logging_utils.session_logger import get_session_logger

load_dotenv()

app = FastAPI(title="Pharmacy Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
LLM_TIMEOUT_SECONDS = 60

# ============================================================================
# Constants & Enums
# ============================================================================

VALID_STATUSES = {"Pending", "In Progress", "Completed"}


class StatusEnum(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


# ============================================================================
# Helper Functions
# ============================================================================

def validate_user(user_id: str):
    """Validate user exists and return user object"""
    if not user_id or not user_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id is required",
        )

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or non-existent user",
        )
    return user


def validate_status(status_value: str):
    """Validate status is allowed"""
    if status_value not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Allowed: {', '.join(VALID_STATUSES)}",
        )
    return status_value


def enrich_prescription(p, user_id=None):
    """Add missing fields to prescription object"""
    try:
        # Convert to dict if not already
        if isinstance(p, dict):
            enriched = p.copy()
        else:
            enriched = vars(p).copy() if hasattr(p, '__dict__') else p

        # If we have medication_id but no medication_name, fetch it from DB
        if "medication_name" not in enriched and "medication_id" in enriched:
            med_name = get_medication_name(enriched.get("medication_id"))
            enriched["medication_name"] = med_name

        # Add user_id if provided
        if user_id and "user_id" not in enriched:
            enriched["user_id"] = user_id

        return enriched
    except Exception:
        # If enrichment fails, return original
        return p


def get_medication_name(medication_id):
    """Get medication name from database"""
    try:
        c = conn()
        cur = c.cursor()
        cur.execute(
            "SELECT brand_name, generic_name FROM medications WHERE id = ?",
            (medication_id,)
        )
        row = cur.fetchone()
        c.close()

        if row:
            row_dict = dict(row)
            return row_dict.get("brand_name") or row_dict.get("generic_name") or medication_id
        return medication_id
    except Exception:
        return medication_id


def enrich_support(s, user_id=None):
    """Add missing fields to support request object"""
    try:
        # Convert to dict if not already
        if isinstance(s, dict):
            enriched = s.copy()
        else:
            enriched = vars(s).copy() if hasattr(s, '__dict__') else s

        # Add user_id if provided
        if user_id and "user_id" not in enriched:
            enriched["user_id"] = user_id

        return enriched
    except Exception:
        # If enrichment fails, return original
        return s


def enrich_prescriptions(prescriptions, user_id=None):
    """Enrich list of prescriptions"""
    return [enrich_prescription(p, user_id) for p in prescriptions] if prescriptions else []


def enrich_supports(supports, user_id=None):
    """Enrich list of support requests"""
    return [enrich_support(s, user_id) for s in supports] if supports else []


# ============================================================================
# User Endpoints
# ============================================================================

@app.get("/users", tags=["Users"])
def list_users():
    """Get all available users"""
    try:
        users = fetch_users()
        return {
            "success": True,
            "data": [
                {
                    "id": u["id"],
                    "full_name": u["full_name"],
                    "role": u["role"],
                    "lang": u["preferred_lang"],
                }
                for u in users
            ]
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users",
        )


@app.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: str):
    """Get specific user details"""
    user = validate_user(user_id)
    return {
        "success": True,
        "data": {
            "id": user["id"],
            "full_name": user["full_name"],
            "role": user["role"],
            "lang": user["preferred_lang"],
        }
    }


# ============================================================================
# Prescription Endpoints
# ============================================================================

@app.get("/users/{user_id}/prescriptions", tags=["Prescriptions"])
def list_prescriptions(
        user_id: str,
        status_filter: str = Query(None, description="Filter by status"),
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(0, ge=0),
):
    """Get user's prescriptions with filtering and pagination"""
    user = validate_user(user_id)

    if status_filter:
        validate_status(status_filter)

    try:
        prescriptions = get_prescription_per_user(user_id)
        prescriptions = prescriptions if prescriptions else []

        # Enrich with user_id and medication_id
        prescriptions = enrich_prescriptions(prescriptions, user_id)

        # Filter by status
        if status_filter:
            prescriptions = [p for p in prescriptions if p.get("status") == status_filter]

        total = len(prescriptions)
        prescriptions = prescriptions[offset:offset + limit]

        return {
            "success": True,
            "data": prescriptions,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prescriptions",
        )


@app.get("/users/{user_id}/prescriptions/{prescription_id}", tags=["Prescriptions"])
def get_prescription(user_id: str, prescription_id: str):
    """Get single prescription details"""
    user = validate_user(user_id)

    try:
        prescriptions = get_prescription_per_user(user_id)
        prescription = next(
            (p for p in prescriptions if p.get("id") == prescription_id),
            None
        )

        if not prescription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prescription not found",
            )

        prescription = enrich_prescription(prescription, user_id)
        return {
            "success": True,
            "data": prescription
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prescription",
        )


@app.patch("/users/{user_id}/prescriptions/{prescription_id}/status", tags=["Prescriptions"])
async def update_prescription_status(
        user_id: str,
        prescription_id: str,
        req: Request
):
    """Update prescription status"""
    user = validate_user(user_id)

    try:
        body = await req.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid JSON request body",
        )

    status_value = body.get("status")
    if not status_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="status field is required",
        )

    validate_status(status_value)

    try:
        update_prescription_request_status(prescription_id, status_value)
        return {
            "success": True,
            "data": {
                "id": prescription_id,
                "status": status_value,
                "message": f"Prescription status updated to {status_value}",
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update prescription status",
        )


# ============================================================================
# Support Ticket Endpoints
# ============================================================================

@app.get("/users/{user_id}/support-tickets", tags=["Support"])
def list_support_requests(
        user_id: str,
        status_filter: str = Query(None, description="Filter by status"),
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(0, ge=0),
):
    """Get user's support tickets with filtering and pagination"""
    user = validate_user(user_id)

    if status_filter:
        validate_status(status_filter)

    try:
        tickets = get_support_per_user(user_id)
        tickets = tickets if tickets else []

        # Enrich with user_id
        tickets = enrich_supports(tickets, user_id)

        if status_filter:
            tickets = [t for t in tickets if t.get("status") == status_filter]

        total = len(tickets)
        tickets = tickets[offset:offset + limit]

        return {
            "success": True,
            "data": tickets,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve support tickets",
        )


@app.get("/users/{user_id}/support-tickets/{ticket_id}", tags=["Support"])
def get_support_ticket(user_id: str, ticket_id: str):
    """Get single support ticket details"""
    user = validate_user(user_id)

    try:
        tickets = get_support_per_user(user_id)
        ticket = next(
            (t for t in tickets if t.get("id") == ticket_id),
            None
        )

        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Support ticket not found",
            )

        ticket = enrich_support(ticket, user_id)
        return {
            "success": True,
            "data": ticket
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve support ticket",
        )


@app.patch("/users/{user_id}/support-tickets/{ticket_id}/status", tags=["Support"])
async def update_support_status(
        user_id: str,
        ticket_id: str,
        req: Request
):
    """Update support ticket status"""
    user = validate_user(user_id)

    try:
        body = await req.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid JSON request body",
        )

    status_value = body.get("status")
    if not status_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="status field is required",
        )

    validate_status(status_value)

    try:
        update_support_request_status(ticket_id, status_value)
        return {
            "success": True,
            "data": {
                "id": ticket_id,
                "status": status_value,
                "message": f"Support ticket status updated to {status_value}",
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update support ticket status",
        )


# ============================================================================
# Pharmacist Endpoints
# ============================================================================

@app.get("/pharmacist/dashboard", tags=["Pharmacist"])
def pharmacist_dashboard(user_id: str = Query(..., description="Pharmacist user ID")):
    """Get pharmacist dashboard with all data"""
    user = validate_user(user_id)

    if user.get("role") != "pharmacist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only pharmacists can access dashboard",
        )

    try:
        prescriptions = get_all_prescription_requests() or []
        support_requests = get_all_support_requests() or []
        medications_sold = get_medications_sold() or []

        # Enrich all data
        prescriptions = enrich_prescriptions(prescriptions)
        support_requests = enrich_supports(support_requests)

        return {
            "success": True,
            "data": {
                "prescriptions": prescriptions,
                "support_requests": support_requests,
                "medications_sold": medications_sold,
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve dashboard data",
        )


@app.get("/pharmacist/prescriptions", tags=["Pharmacist"])
def pharmacist_prescriptions(
        user_id: str = Query(..., description="Pharmacist user ID"),
        status_filter: str = Query(None, description="Filter by status"),
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(0, ge=0),
):
    """Get all prescriptions (pharmacist only)"""
    user = validate_user(user_id)

    if user.get("role") != "pharmacist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only pharmacists can access this resource",
        )

    if status_filter:
        validate_status(status_filter)

    try:
        prescriptions = get_all_prescription_requests() or []
        prescriptions = enrich_prescriptions(prescriptions)

        if status_filter:
            prescriptions = [p for p in prescriptions if p.get("status") == status_filter]

        total = len(prescriptions)
        prescriptions = prescriptions[offset:offset + limit]

        return {
            "success": True,
            "data": prescriptions,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prescriptions",
        )


# ============================================================================
# Chat Endpoint
# ============================================================================

"""
Example: How to integrate session state and rephrase into chat endpoint
"""

from agents.agent_utils.session_state import (
    get_conversation_context,
    set_user_message,
    set_agent_message,
)
from agents.agent_utils.rephrase_question import rephrase_with_session_context

@app.post("/chat", tags=["Chat"])
async def chat(req: Request):
    """Send message to AI pharmacist agent"""
    try:
        body = await req.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON request body",
        )

    user_message = body.get("message", "").strip()
    session_id = body.get("session_id", "anonymous")
    user_id = body.get("user_id")

    user = validate_user(user_id)
    logger = get_session_logger(session_id, user_id)
    logger.info("New chat request from %s", user.get("full_name", "Unknown"))

    # Pharmacist dashboard shortcut
    if user.get("role") == "pharmacist":
        logger.info("Pharmacist accessed dashboard")
        try:
            prescriptions = get_all_prescription_requests() or []
            support_requests = get_all_support_requests() or []
            medications_sold = get_medications_sold() or []

            prescriptions = enrich_prescriptions(prescriptions)
            support_requests = enrich_supports(support_requests)

            return {
                "success": True,
                "type": "dashboard",
                "data": {
                    "prescriptions": prescriptions,
                    "support_requests": support_requests,
                    "medications_sold": medications_sold,
                }
            }
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve dashboard data",
            )

    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )

    # ========== Get session context and rephrase if needed ==========
    session_context = get_conversation_context(session_id)
    rephrased_message = rephrase_with_session_context(
        client=client,
        current_message=user_message,
        session_state=session_context,
        user_id=user_id
    )

    logger.info("Original: %s", user_message[:100])
    if rephrased_message != user_message:
        logger.info("Rephrased: %s", rephrased_message[:100])
    # ================================================================

    # Agent Pipeline - use rephrased message
    try:
        processed_message = ContextAgent(client, logger).process(
            session_id, rephrased_message, user_id
        )
    except Exception:
        logger.exception("ContextAgent failed (non-fatal)")
        processed_message = rephrased_message

    try:
        intent = IntentAgent(logger).process(processed_message, user_id)
    except Exception:
        logger.exception("IntentAgent failed")
        intent = Intent.UNKNOWN

    if intent == Intent.UNKNOWN:
        logger.info("UNKNOWN intent")
        system_context = ""
        user_prompt = (
            "Tell the user politely that you can only help with pharmacy-related "
            "questions such as medications, prescriptions, or availability."
        )
    else:
        try:
            user_prompt, system_context = ExecutionAgent(
                logger, intent
            ).execute(processed_message, user_id)
            logger.info("Workflow executed successfully")
        except Exception:
            logger.exception("ExecutionAgent failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process request",
            )

    # FIX: Store user message BEFORE streaming starts
    set_user_message(session_id, user_message)

    # Buffer to collect the full response
    agent_response_buffer = []

    async def event_stream():
        """Stream agent response and collect for storage"""
        try:
            response = client.responses.create(
                model="gpt-5",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )

            for event in response:
                if event.type == "response.output_text.delta" and event.delta:
                    agent_response_buffer.append(event.delta)
                    yield event.delta

        except Exception:
            logger.exception("LLM streaming failed")
            yield "Sorry, something went wrong."
            return

        # FIX: Store agent message AFTER streaming completes
        full_agent_response = "".join(agent_response_buffer).strip()
        if full_agent_response:
            set_agent_message(session_id, full_agent_response)
            logger.info("Agent response stored in session: %s", full_agent_response[:100])

    return StreamingResponse(event_stream(), media_type="text/plain")

# ============================================================================
# Health Check
# ============================================================================

@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint"""
    return {
        "success": True,
        "service": "Pharmacy Agent Backend",
        "status": "healthy"
    }