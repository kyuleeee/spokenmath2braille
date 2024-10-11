
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification
import torch

def correct_errors(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return corrected_text

def text_to_latex(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    latex_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return latex_text


# def spoken_math_detection(text,model_name):
#     LABEL_LIST = ["O", "B-MATH", "I-MATH"]
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=2)
    
#     inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")
#     inputs = {k: v.to(device) for k, v in inputs.items()}

#     with torch.no_grad():
#         outputs = model(**inputs)

#     predictions = torch.argmax(outputs.logits, dim=-1)
#     tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

#     result = []
#     for token, pred in zip(tokens, predictions[0]):
#         if token.startswith("##"):
#             result[-1] = (result[-1][0] + token[2:], result[-1][1])
#         else:
#             result.append((token, LABEL_LIST[pred]))

#     return result


def spoken_math_detection(text, model_name):
    # 디바이스 설정
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 토크나이저와 모델 로드
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    model.to(device)

    # 입력 텍스트 토크나이징
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # 모델 추론
    with torch.no_grad():
        outputs = model(**inputs)

    # 예측 결과 처리
    predictions = torch.argmax(outputs.logits, dim=-1)
    predicted_labels = [model.config.id2label[t.item()] for t in predictions[0]]

    # 원본 토큰과 예측 레이블 매칭
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    result = []
    for token, label in zip(tokens, predicted_labels):
        if token.startswith("##"):
            if result:
                result[-1] = (result[-1][0] + token[2:], result[-1][1])
        else:
            result.append((token, label))

    # [CLS] 및 [SEP] 토큰 제거
    result = [r for r in result if r[0] not in ['[CLS]', '[SEP]']]

    return result
    
    
    
