
import json
import os
import subprocess
import base64
from pathlib import Path
import re
import time


#========THIS IS FOR TEXT => BRAILLE ======================# 
# Load the Braille mapping
nemeth_json_path = os.path.join('latex2nemeth/encodings/nemeth.json')
with open(nemeth_json_path, 'r', encoding='utf-8') as f:
    braille_map = json.load(f)

# Load braille map for text to braille conversion
brailleMap = json.load(open("braille_map.json",))

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



#===========THIS IS FOR LATEX => NEMETH ======================# 
def writeTex(eqns):
    texFile = open("temp.tex", "w")
    first = r"\documentclass[12pt, letterpaper, twoside]{article}" + "\n"
    second = r"\usepackage[utf8]{inputenc}" + "\n\n"
    begin = r"\begin{document}" + "\n"
    end = r"\end{document}" + "\n"

    with open("temp.tex", "r+") as texFile:
        for l in [first, second, begin]:
            texFile.write(l)
        for e in eqns:
            if e['content'] is None:
                continue
            texFile.write("\\begin{equation}\n" + e['content'] + "\\end{equation}\n")
        texFile.write(end)


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
    equations = [{'content': latex}]
    nemeth_equations = latex2Nemeth(equations)
    return nemeth_equations[0]['braille'] if nemeth_equations else ''



def text_to_braille(text):
    return getBraille(text)

