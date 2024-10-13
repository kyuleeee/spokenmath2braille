import json
import os
import subprocess
import base64
from pathlib import Path
import re
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from huggingface_hub import HfApi, HfFolder

# Load the Braille mapping
nemeth_json_path = os.path.join('latex2nemeth/encodings/nemeth.json')
with open(nemeth_json_path, 'r', encoding='utf-8') as f:
    braille_map = json.load(f)

# Load braille map for text to braille conversion
brailleMap = json.load(open("braille_map.json",))

#=================================================#
#==========text => braille conversion=============# 
def getBraille(text):
    braille = ""
    for char in text:
        try:
            braille += brailleMap[char.lower()]
        except KeyError:
            braille += brailleMap[" "]
    return braille

def text_to_braille(text):
    return getBraille(text)



"""
LaTex text => corrected LaTeX
corrected LaTeX => nemeth 
"""
#=================================================#
#==========  LaTeX text => corrected LaTeX ==============# 



#1. check and convert text to LaTeX

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
        # 기존 형식이 올바르다면, 불필요한 공백과 별표만 제거 : this is really necessary because if the blank exists, the compilation will fail
        return re.sub(r'\s*\*\s*', '', latex_text)
    
    # 형식이 올바르지 않다면, 새로운 형식으로 변경
    equation_content = re.search(r'\$(.*?)\$', latex_text)
    if equation_content:
        equation = equation_content.group(1)
    else:
        equation = latex_text  # 달러 기호가 없으면 전체를 수식으로 간주

    modified_latex = f"""\\documentclass[12pt,letterpaper,twoside]{{article}}
\\usepackage[utf8]{{inputenc}}

\\begin{{document}}
\\begin{{equation}}
{equation}
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


#2. LaTeX output to correct formatting
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



#=================================================#
#========= correctedLaTeX => nemeth ===========#



def compile_latex(tex_file='temp.tex'):
    """Compile LaTeX file using pdflatex."""
    try:
        result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-file-line-error", tex_file], 
                                check=True, capture_output=True, text=True)
        print("LaTeX compilation successful")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during LaTeX compilation: {e}")
    except FileNotFoundError:
        print("pdflatex not found. Please ensure LaTeX is installed and in your system PATH.")

def texFile2Nemeth(tex_file="temp.tex", aux_file="temp.aux", jar_file="latex2nemeth/latex2nemeth.jar", nemeth_json="latex2nemeth/encodings/nemeth.json"):
    """Convert LaTeX file to Nemeth braille using latex2nemeth.jar."""
    cmd = [
        "java",
        "-jar",
        str(Path(jar_file).resolve()),
        str(Path(tex_file).resolve()),
        str(Path(aux_file).resolve()),
        "-e",
        str(Path(nemeth_json).resolve())
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("LaTeX to Nemeth conversion successful")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during LaTeX to Nemeth conversion: {e}")
    except FileNotFoundError:
        print("Java or the specified JAR file was not found. Please ensure Java is installed and the path to the JAR file is correct.")

def readNemethFile(max_attempts=10, delay=1):
    """Read the generated Nemeth file."""
    for attempt in range(max_attempts):
        nemeth_files = list(Path(".").glob("temp*.nemeth"))
        if nemeth_files:
            latest_nemeth_file = max(nemeth_files, key=os.path.getctime)
            try:
                with open(latest_nemeth_file, "rb") as nemethFile:
                    nem = nemethFile.read()
                    nem64 = base64.b64encode(nem)
                    denem = base64.b64decode(nem64)
                    return denem.decode("utf-16").split("\n\n")
            except Exception as e:
                print(f"Error reading nemeth file (attempt {attempt + 1}): {e}")
        else:
            print(f"Nemeth file not found. Attempt {attempt + 1} of {max_attempts}")
        
        if attempt < max_attempts - 1:
            time.sleep(delay)
    
    raise FileNotFoundError("No temp*.nemeth file found after multiple attempts.")

def latex2Nemeth(equations):
    """Convert LaTeX equations to Nemeth braille."""
    opening, closing = "⠸⠩", "⠸⠱"
    writeTex(equations)
    compile_latex()
    texFile2Nemeth()
    eqnNemeth = readNemethFile()
    for i, eqn in enumerate(equations):
        if eqn['content'] is not None:
            eqn['braille'] = opening + eqnNemeth[i] + closing
    return equations

def latex_to_nemeth(latex):
    """Convert LaTeX directly to Nemeth braille."""
    opening, closing = "⠸⠩", "⠸⠱"
    
    with open("temp.tex", "w") as tex_file:
        tex_file.write(latex)

    # Compile LaTeX
    compile_latex()

    # Convert to Nemeth
    texFile2Nemeth()

    # Read Nemeth file
    nemeth_content = readNemethFile()[0]  # Assuming single equation, take first element

    return opening + nemeth_content + closing


#=============== LaTeX text => braille ==============================


# 테스트 함수
def test_improved_text_to_latex(model_name, test_inputs):
    for i, text in enumerate(test_inputs, 1):
        print(f"\nTest {i}:")
        print(f"Input: {text}")
        latex_output = improved_text_to_latex(text, model_name)
        print(f"Output:\n{latex_output}")
        print("Is in desired format:", check_latex_format(latex_output))
        print("=" * 80)
        braille = latex_to_nemeth(latex_output)
        print(braille)
    

if __name__ == "__main__":
    # 테스트 실행
    model_name = "Hyeonsieun/MathSpeech_T5_base_translator"
    test_inputs = [
        "The equation is E equals m c squared",
        "The quadratic formula is x equals negative b plus or minus square root of b squared minus four a c all over two a",
        "The area of a circle is pi r squared",
        "The sum of the angles in a triangle is 180 degrees"
    ]

    test_improved_text_to_latex(model_name, test_inputs) 