import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets import load_dataset
import numpy as np
import argparse
from seqeval.metrics import classification_report

# 인자 파싱
parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--batch_size", type=int, default=32)
parser.add_argument("--learning_rate", type=float, default=1e-4)
parser.add_argument("--weight_decay", type=float, default=0.01)
parser.add_argument("--max_seq_length", type=int, default=128)
parser.add_argument("--num_train_epochs", type=int, default=1)
args = parser.parse_args()

# 데이터셋 로드
data = load_dataset('Kyudan/MathBridge')

# 상수 
TASK = "ner"
MODEL_CHECKPOINT = "bert-base-uncased"
LABEL_LIST = ["O", "B-MATH", "I-MATH"]
NUM_LABELS = len(LABEL_LIST)
MAX_LENGTH = args.max_seq_length
TRAIN_SIZE = 100000
VALID_SIZE = 10000
TEST_SIZE = 10000

# 레이블 매핑
id2label = {id: label for id, label in enumerate(LABEL_LIST)}
label2id = {label: id for id, label in enumerate(LABEL_LIST)}

# 토크나이저 및 모델 초기화
tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT)
model = AutoModelForTokenClassification.from_pretrained(MODEL_CHECKPOINT, num_labels=NUM_LABELS, id2label=id2label, label2id=label2id)

# 전처리 함수
def preprocess_function(examples):
    combined_texts = [f"{before} {spoken} {after}" for before, spoken, after in
                      zip(examples['context_before'], examples['spoken_English'], examples['context_after'])]
    tokenized_inputs = tokenizer(combined_texts, truncation=True, padding='max_length', max_length=MAX_LENGTH)
    labels = []
    for i, input_ids in enumerate(tokenized_inputs["input_ids"]):
        label = [-100] * MAX_LENGTH  # -100 represents padding
        before_tokens = tokenizer(examples['context_before'][i], add_special_tokens=False)["input_ids"]
        spoken_tokens = tokenizer(examples['spoken_English'][i], add_special_tokens=False)["input_ids"]
        start_idx = len(before_tokens) + 1  # +1 for [CLS] token
        end_idx = min(start_idx + len(spoken_tokens), MAX_LENGTH - 1)  # -1 for [SEP] token
        if start_idx < end_idx:
            label[start_idx] = label2id["B-MATH"]
            for j in range(start_idx + 1, end_idx):
                label[j] = label2id["I-MATH"]
        labels.append(label)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# 데이터셋 분할 및 전처리
full_dataset = data['train'].shuffle(seed=args.seed)
train_dataset = full_dataset.select(range(TRAIN_SIZE))
remaining = full_dataset.select(range(TRAIN_SIZE, len(full_dataset)))
valid_dataset = remaining.select(range(VALID_SIZE))
test_dataset = remaining.select(range(VALID_SIZE, VALID_SIZE + TEST_SIZE))

tokenized_datasets = {
    'train': train_dataset.map(preprocess_function, batched=True, remove_columns=train_dataset.column_names),
    'validation': valid_dataset.map(preprocess_function, batched=True, remove_columns=valid_dataset.column_names),
    'test': test_dataset.map(preprocess_function, batched=True, remove_columns=test_dataset.column_names)
}

print(f"Train size: {len(tokenized_datasets['train'])}")
print(f"Validation size: {len(tokenized_datasets['validation'])}")
print(f"Test size: {len(tokenized_datasets['test'])}")

# 평가 메트릭 계산
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [LABEL_LIST[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [LABEL_LIST[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    
    # 직접 정확도 계산
    correct = sum(pred == label for preds, labels in zip(true_predictions, true_labels) for pred, label in zip(preds, labels))
    total = sum(len(labels) for labels in true_labels)
    accuracy = correct / total if total > 0 else 0

    results = classification_report(true_labels, true_predictions, output_dict=True)
    return {
        "precision": results["weighted avg"]["precision"],
        "recall": results["weighted avg"]["recall"],
        "f1": results["weighted avg"]["f1-score"],
        "accuracy": accuracy,
    }

# 훈련 인자
training_args = TrainingArguments(
    f"mathbridge_{args.batch_size}_bert",
    learning_rate=args.learning_rate,
    per_device_train_batch_size=args.batch_size,
    per_device_eval_batch_size=args.batch_size,
    num_train_epochs=args.num_train_epochs,
    weight_decay=args.weight_decay,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    greater_is_better=True,
    push_to_hub=False,
)

# 트레이너 초기화
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 훈련 시작b
print("Starting training...")
trainer.train()

# 평가
print("Evaluating...")
eval_results = trainer.evaluate()
print(f"Evaluation results: {eval_results}")

# 모델 저장
model_name = f"mathbridge-bert"
model.save_pretrained(f"./{model_name}")
tokenizer.save_pretrained(f"./{model_name}")

print(f"Model saved as {model_name}")

# Hugging Face Hub에 업로드(선택적)
model.push_to_hub(model_name)
tokenizer.push_to_hub(model_name)

print("Training and evaluation completed.")