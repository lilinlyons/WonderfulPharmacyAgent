TOOLS = [
  {
    "type": "function",
    "function": {
      "name": "get_medication_by_name",
      "description": "Fetch medication facts by name (brand or generic). Returns only factual label-style info from DB.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string", "description": "Medication name typed by user (brand or generic)."},
          "language": {"type": "string", "enum": ["en", "he"]}
        },
        "required": ["query", "language"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "check_stock",
      "description": "Check stock availability for a medication in a given store location.",
      "parameters": {
        "type": "object",
        "properties": {
          "medication_id": {"type": "string"},
          "store_id": {"type": "string"},
        },
        "required": ["medication_id", "store_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_user_prescriptions",
      "description": "List a user's prescriptions and their status (active/expired/refills left).",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"}
        },
        "required": ["user_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "request_refill",
      "description": "Create a refill request for an existing prescription. Does not approve clinically; only logs request.",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "prescription_id": {"type": "string"}
        },
        "required": ["user_id", "prescription_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "create_support_ticket",
      "description": "Open a customer service ticket (delivery, store hours, insurance receipt, etc.).",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "topic": {"type": "string"},
          "details": {"type": "string"}
        },
        "required": ["user_id", "topic", "details"],
        "additionalProperties": False
      }
    }
  }
]
