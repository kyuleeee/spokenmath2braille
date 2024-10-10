import subprocess
import base64
import json
from pathlib import Path
import os
import re

brailleMap = json.load(open("braille_map.json",))


#text => braille 
def getBraille(text):
    braille = ""
    for char in text:
        try:
            braille += brailleMap[char.lower()]
        except KeyError:
            braille += brailleMap[" "]
    return braille

##==================================================================## 
#equation => tex
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

#tex => aux 
def compile_latex(tex_file='temp.tex', aux_file='temp.aux'):
    with open(tex_file, 'r') as f:
        content = f.read()

    # 문서 클래스 찾기
    doc_class = re.search(r'\\documentclass.*{(.+?)}', content)
    doc_class = doc_class.group(1) if doc_class else 'article'

    # 패키지 찾기
    packages = re.findall(r'\\usepackage.*{(.+?)}', content)

    # 섹션 찾기
    sections = re.findall(r'\\section{(.+?)}', content)

    # 수식 찾기
    equations = re.findall(r'\\begin{equation}(.*?)\\end{equation}', content, re.DOTALL)

    # aux 파일 작성
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



#tex + aux + jar => nemeth code 

def texFile2Nemeth():
    texFile = Path("temp.tex").resolve()
    auxFile = Path("temp.aux").resolve()
    nemethJson = Path("latex2nemeth-code/target/classes/encoding/nemeth.json").resolve()
    jarFile = Path("latex2nemeth-code/target/latex2nemeth.jar").resolve()

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



#nemeth => print 
def readNemethFile():
    nemethFile = open("temp0.nemeth", "rb")
    nem = nemethFile.read()
    nem64 = base64.b64encode(nem)
    denem = base64.b64decode(nem64)
    eqnNemeth = denem.decode("utf-16").split("\n\n")
    return eqnNemeth


def latex2Nemeth(equations):
    opening, closing = "⠸⠩", "⠸⠱"
    writeTex(equations)
    compile_latex('temp.tex','temp.aux')
    texFile2Nemeth()
    eqnNemeth = readNemethFile()
    for i ,eqn in enumerate(equations):
        if eqn['content'] is None:
            continue
        eqn['braille'] = opening + eqnNemeth[i] + closing

    return equations


def text2UEB(texts):
    for txt in texts:
        txt['braille'] = getBraille(txt['content'])
    return texts


def writeToMasterBraille(brailleFile, parserOut, pageNo):
    brailleFile.write("Page no: " + str(pageNo) + '\n') # added only for visual purpose
    brailleFile.write(getBraille("Page no: " + str(pageNo)) + '\n')
    for x in parserOut:
        if x['braille'] is not None:
            print(x['id'], x['type'], x['braille'])
            brailleFile.write(x['type'] + '\n') # added only for visual purpose
            brailleFile.write(x['braille'] + '\n\n')


