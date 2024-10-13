from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForTokenClassification
import torch
import os 
from huggingface_hub import HfApi, HfFolder


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
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    latex_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Check and modify the format if necessary
    latex_text = modify_latex_format(latex_text)
    
    print(latex_text)
    return latex_text
  
  
def test_text_to_latex(model_name, test_inputs):
    for i, text in enumerate(test_inputs, 1):
        print(f"\nTest {i}:")
        print(f"Input: {text}")
        latex_output = text_to_latex(text, model_name)
        print(f"Output:\n{latex_output}")
        print("Is in desired format:", check_latex_format(latex_output))
        print("-" * 50)

# Example usage
model_name = "Hyeonsieun/MathSpeech_T5_base_translator"
test_inputs = [
    "The equation is E equals m c squared",
    "The quadratic formula is x equals negative b plus or minus square root of b squared minus four a c all over two a",
    "The area of a circle is pi r squared",
    "The sum of the angles in a triangle is 180 degrees"
]

test_text_to_latex(model_name, test_inputs)