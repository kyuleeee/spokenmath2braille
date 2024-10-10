from braille_converter import text_to_braille, latex_to_nemeth

def main():
    # Text to Braille
    text_input = "Hello, World!"
    braille_output = text_to_braille(text_input)
    print(f"Text: {text_input}")
    print(f"Braille: {braille_output}")

    # LaTeX to Nemeth
    latex_input = r"f(x) = x^2 + 2x + 1"
    nemeth_output = latex_to_nemeth(latex_input)
    print(f"\nLaTeX: {latex_input}")
    print(f"Nemeth: {nemeth_output}")

if __name__ == "__main__":
    main()