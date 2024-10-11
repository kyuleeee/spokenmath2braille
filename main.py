from speech_to_text import transcribe_audio
from text_to_latex import correct_errors, spoken_math_detection, text_to_latex
from latex_to_braille import latex_to_nemeth, text_to_braille

def detect_math_segments(text, math_detection_model):
    """
    텍스트에서 수학 표현을 감지하고 세그먼트로 분리합니다.
    """
    detected_labels = spoken_math_detection(text, math_detection_model)
    
    segments = []
    current_segment = {"type": "text", "content": ""}
    
    for token, label in detected_labels:
        if label == "O" and current_segment["type"] == "text":
            current_segment["content"] += token + " "
        elif label in ["B-MATH", "I-MATH"] and current_segment["type"] == "math":
            current_segment["content"] += token + " "
        else:
            if current_segment["content"]:
                segments.append(current_segment)
            current_segment = {"type": "math" if label in ["B-MATH", "I-MATH"] else "text", "content": token + " "}
    
    if current_segment["content"]:
        segments.append(current_segment)
    
    return segments

def process_text_segment(text):
    """
    일반 텍스트 세그먼트를 Braille로 변환합니다.
    """
    return text_to_braille(text.strip())

def process_math_segment(text, latex_translation_model):
    """
    수학 표현 세그먼트를 Nemeth Braille로 변환합니다.
    """
    latex_text = text_to_latex(text.strip(), latex_translation_model)
    return latex_to_nemeth(latex_text)

def process_math_audio(audio_file, error_correction_model, latex_translation_model, math_detection_model):
    # 1. 음성을 텍스트로 변환
    transcribed_text = transcribe_audio(audio_file)
    print("Transcribed text:", transcribed_text)
    
    # 2. 오류 교정
    corrected_text = correct_errors(transcribed_text, error_correction_model)
    print("Corrected text:", corrected_text)
    
    # 3. 수학 표현 감지 및 세그먼트 분리
    segments = detect_math_segments(corrected_text, math_detection_model)
    
    # 4. 각 세그먼트 처리
    result = []
    for segment in segments:
        if segment["type"] == "text":
            braille_text = process_text_segment(segment["content"])
            result.append(("text", braille_text))
        else:  # math
            nemeth_text = process_math_segment(segment["content"], latex_translation_model)
            result.append(("math", nemeth_text))
    
    return result

def main():
    audio_file = "temp.wav"
    error_correction_model = "Hyeonsieun/MathSpeech_T5_base_corrector"
    latex_translation_model = "Hyeonsieun/MathSpeech_T5_base_translator"
    math_detection_model = "jeongyoun/distilbert-base-uncased-finetuned-ner-increased"  # 실제 모델 이름으로 변경해주세요
    
    result = process_math_audio(audio_file, error_correction_model, latex_translation_model, math_detection_model)
    
    print("Final result (audio to mixed Braille/Nemeth):")
    for segment_type, content in result:
        print(f"{segment_type.capitalize()}: {content}")

if __name__ == "__main__":
    main()