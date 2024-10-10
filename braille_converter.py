import json
import os
from content_to_braille import getBraille, latex2Nemeth

# Load the Braille mapping
nemeth_json_path = os.path.join('/Users/lobeli/Desktop/학부인턴/spokenmath2braille/latex2nemeth-code/src/main/resources/encoding/nemeth.json')
with open(nemeth_json_path, 'r', encoding='utf-8') as f:
    braille_map = json.load(f)

def text_to_braille(text):
    """Convert simple text to Braille."""
    return getBraille(text)

def latex_to_nemeth(latex):
    """Convert simple LaTeX to Nemeth Braille code."""
    equations = [{'content': latex}]
    nemeth_equations = latex2Nemeth(equations)
    return nemeth_equations[0]['braille'] if nemeth_equations else ''