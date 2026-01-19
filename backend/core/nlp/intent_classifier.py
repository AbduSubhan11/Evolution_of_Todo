from typing import Dict, Any, Optional
import re


class IntentClassifier:
    """
    Simple rule-based intent classifier for interpreting user commands
    In a production system, this would likely use ML models or more sophisticated NLP
    """

    def __init__(self):
        # Define patterns for different intents
        self.intent_patterns = {
            "add_task": [
                r"(?:add|create|make|new|remember|remind me to)\s+(?:a\s+)?(?:task|to\s+)?(.+)",
                r"(?:create|add)\s+(.+?)\s+(?:as\s+)?(?:a\s+)?task",
                r"(?:i\s+need\s+to|i\s+want\s+to)\s+(.+)"
            ],
            "list_tasks": [
                r"(?:show|display|list|see|view)\s+(?:my\s+)?(?:tasks?|todo|todos)",
                r"(?:what\s+(?:are|is)\s+(?:my\s+)?(?:tasks?|todo|todos))",
                r"(?:show\s+me\s+)?(?:all\s+)?(?:my\s+)?(?:tasks?|todo|todos)",
                r"what.+done",  # "what have I done?", "what's done?"
            ],
            "complete_task": [
                r"(?:complete|finish|done|mark as done|done with)\s+(?:the\s+)?(.+)",
                r"(?:finish\s+up\s+)?(.+)\s+(?:is\s+)?(?:done|complete|finished)",
                r"(?:i\s+have\s+)?(?:completed|finished)\s+(?:the\s+)?(.+)"
            ],
            "delete_task": [
                r"(?:delete|remove|erase|get rid of|cancel)\s+(?:the\s+)?(.+)",
                r"(?:remove\s+)?(.+)\s+(?:from\s+my\s+)?(?:tasks?|list)",
            ],
            "update_task": [
                r"(?:change|update|modify|rename|edit)\s+(?:the\s+)?(.+?)\s+(?:to|as)\s+(.+)",
                r"(?:update|change)\s+(?:the\s+)?(.+?)\s+(?:with|and)\s+(.+)"
            ]
        }

    def classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify the intent of the user's message and extract relevant parameters
        """
        text_lower = text.lower().strip()

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    groups = match.groups()

                    # Different intents have different parameter extraction needs
                    if intent == "add_task":
                        return {
                            "intent": "add_task",
                            "parameters": {
                                "title": groups[0].strip() if groups else text
                            }
                        }
                    elif intent == "list_tasks":
                        # Check if there's a status filter in the query
                        status_filter = None
                        if "completed" in text_lower or "done" in text_lower:
                            status_filter = "completed"
                        elif "pending" in text_lower or "not done" in text_lower:
                            status_filter = "pending"

                        return {
                            "intent": "list_tasks",
                            "parameters": {
                                "status_filter": status_filter
                            } if status_filter else {}
                        }
                    elif intent in ["complete_task", "delete_task"]:
                        # Extract task reference (could be title or other identifier)
                        return {
                            "intent": intent,
                            "parameters": {
                                "task_ref": groups[0].strip() if groups else text
                            }
                        }
                    elif intent == "update_task":
                        if len(groups) >= 2:
                            return {
                                "intent": "update_task",
                                "parameters": {
                                    "task_ref": groups[0].strip(),
                                    "new_value": groups[1].strip()
                                }
                            }

        # If no specific intent is matched, default to a general intent
        return {
            "intent": "unknown",
            "parameters": {
                "original_text": text
            }
        }

    def extract_task_id_from_reference(self, task_ref: str, available_tasks: list) -> Optional[str]:
        """
        Helper method to extract a specific task ID from a textual reference
        This would typically involve fuzzy matching against available tasks
        """
        # This is a simplified implementation
        # In a real system, you'd use fuzzy matching, embeddings, or other NLP techniques

        task_ref_lower = task_ref.lower()

        # Look for exact matches first
        for task in available_tasks:
            if task.get('title', '').lower() == task_ref_lower:
                return task.get('id')

        # Look for partial matches
        for task in available_tasks:
            if task_ref_lower in task.get('title', '').lower():
                return task.get('id')

        # If nothing matches, return None
        return None


# Global instance
intent_classifier = IntentClassifier()