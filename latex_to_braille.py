
import json
import os
import subprocess
import base64
from pathlib import Path
import re

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

def writeTex(eqns):
    with open("temp.tex", "w") as texFile:
        texFile.write(r"\documentclass[12pt, letterpaper, twoside]{article}" + "\n")
        texFile.write(r"\usepackage[utf8]{inputenc}" + "\n\n")
        texFile.write(r"\begin{document}" + "\n")
        for e in eqns:
            if e['content'] is not None:
                texFile.write("\\begin{equation}\n" + e['content'] + "\\end{equation}\n")
        texFile.write(r"\end{document}" + "\n")

def compile_latex(tex_file='temp.tex', aux_file='temp.aux'):
    with open(tex_file, 'r') as f:
        content = f.read()

    doc_class = re.search(r'\\documentclass.*{(.+?)}', content)
    doc_class = doc_class.group(1) if doc_class else 'article'

    packages = re.findall(r'\\usepackage.*{(.+?)}', content)
    sections = re.findall(r'\\section{(.+?)}', content)
    equations = re.findall(r'\\begin{equation}(.*?)\\end{equation}', content, re.DOTALL)

    with open(aux_file, 'w') as f:
        f.write('\\relax\n')
        f.write(f'\\@input{{packages/{doc_class}.aux}}\n')
        
        for package in packages:
            f.write(f'\\@input{{packages/{package}.aux}}\n')
        
        f.write('\\@writefile{toc}{\n')
        for i, section in enumerate(sections, 1):
            f.write(f'  \\contentsline {{section}}{{{section}}}{{{i}}}{{section*.{i}}}%\n')
        f.write('}\n')

        for i, equation in enumerate(equations, 1):
            f.write(f'\\newlabel{{eq:{i}}}{{{{({i})}}{{1}}}}\n')

        f.write('\\gdef \\@abspage@last{1}\n')

    print(f"Simple AUX file '{aux_file}' has been created based on '{tex_file}'.")

def texFile2Nemeth():
    texFile = Path("temp.tex").resolve()
    auxFile = Path("temp.aux").resolve()
    nemethJson = Path("latex2nemeth/encodings/nemeth.json").resolve()
    jarFile = Path("latex2nemeth/target/latex2nemeth.jar").resolve()

    cmd = [
        "java",
        "-jar",
        str(jarFile),
        str(texFile),
        str(auxFile),
        "-e",
        str(nemethJson)
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Command executed successfully")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
        print("Error output:", e.stderr)
    except FileNotFoundError:
        print("Java or the specified JAR file was not found. Please ensure Java is installed and the path to the JAR file is correct.")

def readNemethFile():
    with open("temp0.nemeth", "rb") as nemethFile:
        nem = nemethFile.read()
        nem64 = base64.b64encode(nem)
        denem = base64.b64decode(nem64)
        eqnNemeth = denem.decode("utf-16").split("\n\n")
    return eqnNemeth

def latex2Nemeth(equations):
    opening, closing = "⠸⠩", "⠸⠱" 
    writeTex(equations) #writing temp.tex file 
    compile_latex('temp.tex', 'temp.aux') #making aux file
    texFile2Nemeth() #converting tex to nemeth 
    eqnNemeth = readNemethFile() #nemeth to readable utf-16 
    for i, eqn in enumerate(equations):
        if eqn['content'] is not None:
            eqn['braille'] = opening + eqnNemeth[i] + closing
    return equations

def text_to_braille(text):
    return getBraille(text)

def latex_to_nemeth(latex):
    equations = [{'content': latex}]
    nemeth_equations = latex2Nemeth(equations)
    return nemeth_equations[0]['braille'] if nemeth_equations else ''

def text2UEB(texts): #이 코드 있어야 하는지 점검! 
    for txt in texts:
        txt['braille'] = getBraille(txt['content'])
    return texts

def writeToMasterBraille(brailleFile, parserOut, pageNo): #이 코드 있어야 하는지 점검! 
    brailleFile.write("Page no: " + str(pageNo) + '\n')
    brailleFile.write(getBraille("Page no: " + str(pageNo)) + '\n')
    for x in parserOut:
        if x['braille'] is not None:
            print(x['id'], x['type'], x['braille'])
            brailleFile.write(x['type'] + '\n')
            brailleFile.write(x['braille'] + '\n\n')
