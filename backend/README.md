# Workflow: Active Ingredients Lookup

## 1. Name and Purpose
`active_ingredients.py` - Retrieves active ingredients for a given medication name and returns formatted medication details.

## 2. Inputs
- `message` (str, required): Medication name to look up (e.g., "aspirin", "ibuprofen")
- `user_id` (str, optional): User identifier for logging and tracking

## 3. Output Schema
```python
{
    "type": "active_ingredients",
    "context": "Medication name: {name}\nActive ingredient(s): {ingredient}"
}
```

## 4. Error Handling
- **Medication not found**: Returns context message "Medication not found in the system."
- **Database exception**: Catches all exceptions and returns "Sorry, there was an internal error while retrieving the medication information."

## 5. Fallback Behavior
```python
    if not med:
        logger.info("Medication not found")
        return {
            "type": "active_ingredients",
            "context": "Medication not found in the system."
        }

```
# Workflow: Medication Info Lookup

## 1. Name and Purpose
`medication_info.py` - Retrieves comprehensive medication information including generic name, form, strength, and warnings.

## 2. Inputs
- `message` (str, required): Medication name to look up (e.g., "aspirin", "ibuprofen")
- `user_id` (str, optional): User identifier for logging and tracking

## 3. Output Schema
```python
{
    "type": "medication_info",
    "context": "Medication name: {name}\nGeneric name: {generic_name}\nForm: {form}\nStrength: {strength}\nWarnings: {warnings_en}"
}
```

## 4. Error Handling
- **Medication not found**: Returns context message "Medication not found."
- **Database exception**: Catches all exceptions and returns "Sorry, there was an internal error while retrieving the medication information."

## 5. Fallback Behavior
```python
    if not med:
        logger.info("Medication not found")
        return {
            "type": "active_ingredients",
            "context": "Medication not found in the system."
        }
```


# Workflow: Medication Dosage Lookup

## 1. Name and Purpose
`medication_dosage.py` - Retrieves label dosage instructions for a given medication and returns formatted dosing guidance with medical disclaimer.

## 2. Inputs
- `message` (str, required): Medication name to look up (e.g., "aspirin", "ibuprofen")
- `user_id` (str, optional): User identifier for logging and tracking

## 3. Output Schema
```python
{
    "type": "medication_dosage",
    "context": "Medication name: {name}\nLabel dosage instructions:\n{label_instructions_en}\n\nFor personalized dosing or medical advice, please consult a pharmacist or doctor."
}
```

## 4. Error Handling
- **Medication not found**: Returns context message "Medication not found."
- **Database exception**: Catches all exceptions and returns "Sorry, there was an internal error while retrieving the medication information."

## 5. Fallback Behavior

**Fallback to Generic Dosage Instructions**
```python
if not med:
    return {
        "type": "medication_dosage",
        "context": f"Standard dosage information for {message} unavailable. Please refer to the medication package insert or consult a healthcare provider."
    }
```
# Workflow: Prescription Requirement Lookup

## 1. Name and Purpose
`prescription_requirements.py` - Determines whether a medication requires a prescription and provides guidance for obtaining one if needed.

## 2. Inputs
- `message` (str, required): Medication name to look up (e.g., "aspirin", "amoxicillin")
- `user_id` (str, optional): User identifier for logging and tracking

## 3. Output Schema
```python
{
    "type": "prescription_requirement",
    "context": "Medication name: {name}\nPrescription required: Yes, please contact your Doctor if you require a prescription. / No"
}
```

## 4. Error Handling
- **Medication not found**: Returns context message "Medication not found."
- **Database exception**: Catches all exceptions and returns "Sorry, there was an internal error while retrieving the medication information."

## 5. Fallback Behavior

**Cache Layer**
```python
try:
    med = get_medication_by_name(message)
except Exception:
    med = get_cached_medication(message)
    if med:
        logger.info("Serving RX requirement from cache")
        return {"type": "prescription_requirement", "context": f"[Cached] {med['name']} RX info..."}
```
**Default to Conservative Assumption**
```python
    if not med:
        logger.info("Medication not found")
        return {
            "type": "prescription_requirement",
            "context": "Medication not found."
        }
```

# Workflow: Prescription Refill Request

## 1. Name and Purpose
`refill_request.py` - Submits a prescription refill request for an authenticated user. Validates active prescriptions, checks refill availability, creates refill request record, and deducts one refill from the prescription.

## 2. Inputs
- `message` (str, optional): User notes or reason for refill request
- `user_id` (str, required): Authenticated user identifier required for request submission

## 3. Output Schema
```python
{
    "type": "refill_request",
    "context": "Refill request submitted successfully with request ID, status, medication details...",
    "data": {
        "request_id": str,
        "user_id": str,
        "medication_id": int,
        "status": "pending",
        "refills_left": int,
        "created_at": str
    }
}
```

## 4. Error Handling
- **Missing user_id**: Returns "Unable to submit refill request. User not identified."
- **No active prescription**: Returns "You do not have an active prescription on file. Please contact your pharmacist or doctor."
- **No refills remaining**: Returns "Your prescription has no refills left. Please contact your doctor."
- **Database exception**: Returns "Sorry, we couldn't submit your refill request. Please try again." with rollback on failure.

## 5. Fallback Behavior
**Failure graceful fallback**
```python
    except Exception:
        logger.exception("Failed to create refill request")
        try:
            c.rollback()
            c.close()
        except Exception:
            pass

        return {
            "type": "refill_request",
            "context": "Sorry, we couldn't submit your refill request. Please try again."
        }
```

**Current Implementation:** Basic exception handling with transaction rollback; no message queue or email fallback.
