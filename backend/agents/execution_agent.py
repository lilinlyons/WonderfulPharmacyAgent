from workflows import (
    active_ingredients,
    fallback,
    greetings,
    medication_dosage,
    medication_info,
    prescription_requirements,
    refill_request,
    stock_check,
    safety_redirect,
    support_request
)


class ExecutionAgent:
    """
    Routes self.intents to their corresponding workflow handlers.
    Always returns a callable handler.
    """

    def __init__(self, logger, intent):
        self.logger = logger
        self.intent = intent

    def route(self):
        """
        Route an intent to the correct workflow handler.
        """
        try:
            self.logger.info("Routing intent: %s", self.intent)

            if self.intent in {
                self.intent.MEDICAL_ADVICE,
                self.intent.SIDE_EFFECTS_CONCERN,
                self.intent.DRUG_INTERACTIONS,
            }:
                self.logger.debug("intent mapped to safety_redirect")
                return safety_redirect.handle

            if self.intent == self.intent.STOCK_CHECK:
                self.logger.debug("intent mapped to stock_check")
                return stock_check.handle

            if self.intent == self.intent.ACTIVE_INGREDIENTS:
                self.logger.debug("intent mapped to active_ingredients")
                return active_ingredients.handle

            if self.intent == self.intent.PRESCRIPTION_REQUIREMENT:
                self.logger.debug("intent mapped to prescription_requirements")
                return prescription_requirements.handle

            if self.intent == self.intent.GREETING:
                self.logger.debug("intent mapped to greetings")
                return greetings.handle

            if self.intent == self.intent.MEDICATION_INFO:
                self.logger.debug("intent mapped to medication_info")
                return medication_info.handle

            if self.intent == self.intent.MEDICATION_DOSAGE:
                self.logger.debug("intent mapped to medication_dosage")
                return medication_dosage.handle

            if self.intent == self.intent.SUPPORT:
                self.logger.debug("self.intent mapped to support_request")
                return support_request.handle

            if self.intent == self.intent.REFILL_REQUEST:
                self.logger.debug("intent mapped to refill_request")
                return refill_request.handle

            self.logger.info(
                "No explicit route for intent %s, using fallback", self.intent
            )


            return fallback.handle

        except Exception:
            self.logger.exception("Routing failed for intent: %s", self.intent)
            return fallback.handle

    def execute(self, user_message: str, user_id: str):
        handler = self.route()
        workflow_result = handler(
                user_message,
                user_id=user_id,
            )

        system_context = workflow_result.get("context", "")

        return user_message, system_context