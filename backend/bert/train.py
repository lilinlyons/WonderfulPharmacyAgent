from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset
from labels import INTENT_LABELS

MODEL_NAME = "bert-base-multilingual-cased"
NUM_LABELS = len(INTENT_LABELS)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length")

dataset = load_dataset(
    "json",
    data_files={"train": "backend/bert/data/train.jsonl"},
)

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.rename_column("label", "labels")
dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS
)

training_args = TrainingArguments(
    output_dir="backend/bert/model_out",
    num_train_epochs=4,
    per_device_train_batch_size=8,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
)

trainer.train()
trainer.save_model("backend/bert/model_out")
tokenizer.save_pretrained("backend/bert/model_out")
