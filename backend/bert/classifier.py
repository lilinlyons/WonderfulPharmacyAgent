from bert.model import tokenizer, model
from bert.labels import INTENT_LABELS, Intent
import torch

CONFIDENCE_THRESHOLD = 0.2

def classify_intent(text: str) -> Intent:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]

    best_idx = torch.argmax(probs).item()
    confidence = probs[best_idx].item()

    if confidence < CONFIDENCE_THRESHOLD:
        return Intent.UNKNOWN

    return INTENT_LABELS[best_idx]
