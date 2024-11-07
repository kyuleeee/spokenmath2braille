
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification
import torch
import openai
import re

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


# def spoken_math_detection(text, model_name):
#     # 디바이스 설정
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#     # 토크나이저와 모델 로드
#     tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
#     model = AutoModelForTokenClassification.from_pretrained(model_name)
#     model.to(device)

#     # 입력 텍스트 토크나이징
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#     inputs = {k: v.to(device) for k, v in inputs.items()}

#     # 모델 추론
#     with torch.no_grad():
#         outputs = model(**inputs)

#     # 예측 결과 처리
#     predictions = torch.argmax(outputs.logits, dim=-1)
#     predicted_labels = [model.config.id2label[t.item()] for t in predictions[0]]

#     # 원본 토큰과 예측 레이블 매칭
#     tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
#     result = []
#     for token, label in zip(tokens, predicted_labels):
#         if token.startswith("##"):
#             if result:
#                 result[-1] = (result[-1][0] + token[2:], result[-1][1])
#         else:
#             result.append((token, label))

#     # [CLS] 및 [SEP] 토큰 제거
#     result = [r for r in result if r[0] not in ['[CLS]', '[SEP]']]

#     return result

class SpokenMathDetector:
    def __init__(self, api_key, api_base, api_type='azure', api_version='2024-05-01-preview'):
        """Initialize with OpenAI/Azure credentials."""
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_type = api_type
        openai.api_version = api_version
        self.LABEL_LIST = ["O", "B-MATH", "I-MATH"]

    def _create_system_prompt(self):
        """Create system prompt for spoken mathematics detection."""
        return """You are a specialized Named Entity Recognition (NER) system designed to detect mathematical expressions in text, particularly in the context of educational videos or lectures.

Your task is to label mathematical expressions in the given text with B-MATH (beginning of a math expression) and I-MATH (inside a math expression). Label non-mathematical parts with O.

When identifying mathematical expressions, consider the following:

1. Numbers and mathematical operators (e.g., +, -, *, /, =, <, >)
2. Mathematical terms and concepts (e.g., vector, matrix, equation, function, derivative)
3. Geometric concepts (e.g., line, plane, angle, triangle)
4. Variables and constants (e.g., x, y, z, pi, e)
5. Mathematical structures (e.g., sets, groups, fields)
6. Coordinate representations (e.g., "two minus one" as a vector component)
7. Equation descriptions (e.g., "x squared plus y squared equals z squared")

Important guidelines:
- Context is crucial. A number alone doesn't always indicate a mathematical expression.
- Pay attention to mathematical verbs (e.g., add, subtract, multiply, divide, integrate, differentiate, equal).
- Consider phrases that describe mathematical operations or relationships.
- Be aware of colloquial ways of expressing mathematical concepts in spoken language.

Examples:
1. Input: The equation x squared plus y squared equals z squared represents a sphere.
   Output: ['O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'O', 'O', 'O']

2. Input: We need to find the derivative of f of x with respect to x.
   Output: ['O', 'O', 'O', 'O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'O']

3. Input: Let's consider the vector two minus one and add it to the matrix.
   Output: ['O', 'O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'O', 'O', 'O', 'O', 'O', 'B-MATH', 'O']

4. Input: multiply matrix A by vector x to get vector b
    Output: ['B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH']

5.  Input: solve x equals five then y equals x plus three
    Output: ['O', 'B-MATH', 'I-MATH', 'I-MATH', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH']


6.  Input: the mean of x one through x n equals mu
    Output: ['O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH']




Only return the list of labels, no explanation. Ensure the number of labels matches the number of words exactly."""

    def tokenize_text(self, text):
        """Simple word tokenization."""
        return [token for token in text.strip().split() if token]

    def _parse_gpt_response(self, response_text, num_tokens):
        """Parse and validate GPT response."""
        try:
            # Clean up the response text
            cleaned = response_text.strip()
            # Handle different list formats
            if cleaned.startswith('[') and cleaned.endswith(']'):
                labels = eval(cleaned)
            else:
                # Split on commas if not in proper list format
                labels = [label.strip(' "\'[]') for label in cleaned.split(',')]
            
            # Validate labels
            if len(labels) == num_tokens and all(label in self.LABEL_LIST for label in labels):
                return labels
        except Exception as e:
            print(f"Error parsing response: {response_text}")
            print(f"Error details: {str(e)}")
            
        # Fallback: return all O labels
        return ['O'] * num_tokens

    def get_labels(self, text):
        """Get tokens and their corresponding labels."""
        tokens = self.tokenize_text(text)
        
        try:
            response = openai.ChatCompletion.create(
                engine="gpt1",
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": f'Text: "{text}"\nWords ({len(tokens)}): {tokens}'}
                ],
                temperature=0.1,
                max_tokens=1000,
                n=1,
                stop=None
            )
            
            response_text = response.choices[0].message['content'].strip()
            labels = self._parse_gpt_response(response_text, len(tokens))
            return tokens, labels
            
        except Exception as e:
            print(f"API error in get_labels: {str(e)}")
            return tokens, ['O'] * len(tokens)

def spoken_math_detection(text, model_name=None):
    """
    Detect mathematical expressions using OpenAI API.
    model_name parameter is kept for compatibility but not used.
    """
    detector = SpokenMathDetector(
        api_key=_,
        api_base=,
        api_type='',
        api_version=''
    )
    
    tokens, labels = detector.get_labels(text)
    return list(zip(tokens, labels))

def detect_math_segments(text):
    """Convert text into segments with math detection."""
    token_labels = spoken_math_detection(text)
    segments = []
    current_segment = {"type": "text", "content": ""}
    
    for token, label in token_labels:
        if label == "O" and current_segment["type"] == "text":
            current_segment["content"] += token + " "
        elif label in ["B-MATH", "I-MATH"] and current_segment["type"] == "math":
            current_segment["content"] += token + " "
        else:
            if current_segment["content"]:
                current_segment["content"] = current_segment["content"].strip()
                segments.append(current_segment)
            current_segment = {
                "type": "math" if label in ["B-MATH", "I-MATH"] else "text",
                "content": token + " "
            }
    
    if current_segment["content"]:
        current_segment["content"] = current_segment["content"].strip()
        segments.append(current_segment)
    
    return segments

if __name__ == "__main__":
    # Test texts
    test_texts = [
        "The equation x squared plus y squared equals z squared represents a sphere",
        "We need to find the derivative of f of x with respect to x",
        "Let's consider the vector two minus one and add it to the matrix",
        "The second column is the vector three four five",
        "The sine of theta plus the cosine of phi",
        "A right triangle with angle measuring ninety degrees",
        "Solve for y when two x plus three y equals six",
        "I have two dogs at home",  # Non-mathematical context
        "The complex number two plus i times three"
    ]

    try:
        for text in test_texts:
            print(f"\nInput text: {text}")
            results = spoken_math_detection(text)
            print("Tokens and labels:")
            for token, label in results:
                print(f"{token}: {label}")
            print("-" * 50)
    except Exception as e:
        print(f"Error during testing: {str(e)}")