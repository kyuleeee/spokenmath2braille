from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification
import torch
import os 
from huggingface_hub import HfApi, HfFolder
import re


def check_latex_format(latex_text):
    """
    Check if the LaTeX text is in the desired format.
    Returns True if it's in the correct format, False otherwise.
    """
    required_elements = [
        r"\documentclass[12pt, letterpaper, twoside]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\begin{document}",
        r"\begin{equation}",
        r"\end{equation}",
        r"\end{document}"
    ]
    
    return all(element in latex_text for element in required_elements)

def modify_latex_format(latex_text):
    """
    Modify the LaTeX text to match the desired format if necessary.
    """
    if check_latex_format(latex_text):
        return latex_text
    
    # If not in the correct format, we'll assume it's just the equation content
    modified_latex = f"""\\documentclass[12pt, letterpaper, twoside]{{article}}
\\usepackage[utf8]{{inputenc}}

\\begin{{document}}
\\begin{{equation}}
{latex_text}
\\end{{equation}}
\\end{{document}}
"""
    return modified_latex

def text_to_latex(text, model_name): 
    """
    use pretrained model to make text to latex format 
    """
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    latex_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Check and modify the format if necessary
    latex_text = modify_latex_format(latex_text)
    
    print(latex_text)
    return latex_text

import re

def postprocess_latex_equation(latex):
    print("Original LaTeX:")
    print(latex)
    print("-" * 50)

    # LaTeX 문서 구조 파싱
    parts = latex.split("\\begin{document}")
    if len(parts) != 2:
        print("Could not find \\begin{document}")
        return latex

    preamble, document = parts
    document_parts = document.split("\\end{document}")
    if len(document_parts) != 2:
        print("Could not find \\end{document}")
        return latex

    document_content = document_parts[0].strip()

    print("Document content:")
    print(document_content)
    print("-" * 50)

    # 수식 부분 추출
    equation_parts = document_content.split("\\begin{equation}")
    if len(equation_parts) != 2:
        print("Could not find \\begin{equation}")
        return latex

    equation = equation_parts[1].split("\\end{equation}")[0].strip()

    print("Original equation:")
    print(equation)
    print("-" * 50)

    # 일반적인 오류 수정
    equation = equation.replace('$ ', '$').replace(' $', '$')  # 불필요한 공백 제거
    equation = equation.replace('mathcal', '\\mathcal')
    equation = equation.replace('text', '\\text')
    equation = equation.replace('quad', '\\quad')
    equation = equation.replace('operatorname', '\\operatorname')
    equation = equation.replace('sum', '\\sum')
    equation = equation.replace('frac', '\\frac')
    equation = equation.replace('sqrt', '\\sqrt')
    
    # 제곱 표현 수정
    equation = re.sub(r'(\w+)\s+2', r'\1^2', equation)
    
    # 분수 표현 개선 (예: x= frac -> x = \frac{...}{...})
    if '\\frac' in equation and '{' not in equation:
        equation = equation.replace('\\frac', '\\frac{...}{...}')
    
    # 각도 표현 수정
    equation = equation.replace('circ', '^\\circ')

    print("Processed equation:")
    print(equation)
    print("-" * 50)

    # 수정된 수식을 문서에 다시 삽입
    processed_document = (
        equation_parts[0] +
        "\\begin{{equation}}\n{}\n\\end{{equation}}".format(equation) +
        equation_parts[1].split('\\end{equation}')[1]
    )

    # 전체 LaTeX 문서 재구성
    processed_latex = (
        preamble +
        "\\begin{{document}}\n{}\n\\end{{document}}".format(processed_document) +
        document_parts[1]
    )

    print("Processed LaTeX:")
    print(processed_latex)
    print("-" * 50)

    return processed_latex

def improved_text_to_latex(text, model_name):
    # 기존의 text_to_latex 함수 호출
    latex_output = text_to_latex(text, model_name)
    
    # 후처리 적용
    processed_latex = postprocess_latex_equation(latex_output)
    
    return processed_latex

# 테스트 함수
def test_improved_text_to_latex(model_name, test_inputs):
    for i, text in enumerate(test_inputs, 1):
        print(f"\nTest {i}:")
        print(f"Input: {text}")
        latex_output = improved_text_to_latex(text, model_name)
        print(f"Output:\n{latex_output}")
        print("Is in desired format:", check_latex_format(latex_output))
        print("=" * 80)

# 테스트 실행
model_name = "Hyeonsieun/MathSpeech_T5_base_translator"
test_inputs = [
    "The equation is E equals m c squared",
    "The quadratic formula is x equals negative b plus or minus square root of b squared minus four a c all over two a",
    "The area of a circle is pi r squared",
    "The sum of the angles in a triangle is 180 degrees"
]

test_improved_text_to_latex(model_name, test_inputs)
