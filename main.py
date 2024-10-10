from speech_to_text import transcribe_audio
from text_to_latex import correct_errors, text_to_latex
from latex_to_braille import latex_to_nemeth, text_to_braille

def process_math_audio(audio_file, error_correction_model, latex_translation_model):
    # 1. 음성을 텍스트로 변환
    transcribed_text = transcribe_audio(audio_file)
    print("Transcribed text:", transcribed_text)
    
    # 2. 오류 교정
    corrected_text = correct_errors(transcribed_text, error_correction_model)
    print("Corrected text:", corrected_text)
    
    # 3. LaTeX로 변환
    latex_text = text_to_latex(corrected_text, latex_translation_model)
    print("LaTeX text:", latex_text)
    
    # 4. Braille(Nemeth)로 변환
    braille_text = latex_to_nemeth(latex_text)
    print("Braille text:", braille_text)
    
    return braille_text

def main():
    # 음성에서 점자로 변환
    audio_file = "temp.wav"
    error_correction_model = "Hyeonsieun/MathSpeech_T5_base_corrector"
    latex_translation_model = "Hyeonsieun/MathSpeech_T5_base_translator"

    result = process_math_audio(audio_file, error_correction_model, latex_translation_model)
    print("Final result (audio to braille):", result)

    # 텍스트에서 점자로 변환
    text_input = "Hello, World!"
    braille_output = text_to_braille(text_input)
    print(f"\nText: {text_input}")
    print(f"Braille: {braille_output}")

    # LaTeX에서 Nemeth로 변환
    latex_input = r"f(x) = x^2 + 2x + 1"
    nemeth_output = latex_to_nemeth(latex_input)
    print(f"\nLaTeX: {latex_input}")
    print(f"Nemeth: {nemeth_output}")

if __name__ == "__main__":
    main()