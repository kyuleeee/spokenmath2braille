from speech_to_text import transcribe_audio
from text_to_latex import spoken_math_detection, text_to_latex
from latex_to_braille import improved_text_to_latex, latex_to_nemeth , text_to_braille

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
    try:
        # 텍스트를 개선된 LaTeX로 변환
        latex_text = improved_text_to_latex(text.strip(), latex_translation_model)
        
        # LaTeX를 Nemeth Braille로 변환
        nemeth_braille = latex_to_nemeth(latex_text)
        
        return nemeth_braille
    except Exception as e:
        print(f"Error in processing math segment: {e}")
        return f"⠸⠩Error: Unable to convert '{text}'⠸⠱"  # 오류 발생 시 점자로 오류 메시지 반환

def process_math_audio(audio_file, latex_translation_model, math_detection_model):
    # 1. 음성을 텍스트로 변환
    transcribed_text = transcribe_audio(audio_file)
    print("Transcribed text:", transcribed_text)
    
    transcribed_text = "one plus two is theree but I don't like three"
    # 2.  수학 표현 감지 및 세그먼트 분리
    segments = detect_math_segments(transcribed_text, math_detection_model)
    
    # 43 각 세그먼트 처리
    result = []
    for segment in segments:
        if segment["type"] == "text":
            braille_text = process_text_segment(segment["content"])
            result.append(("text", braille_text))
        else:  # math
            nemeth_text = process_math_segment(segment["content"], latex_translation_model)
            result.append(("math", nemeth_text))
    print(result)
    return result

def main():
    audio_file = "temp.wav"
    latex_translation_model = "Hyeonsieun/MathSpeech_T5_small_translator"
    math_detection_model = "jeongyoun/mathbridge-bert"  # 실제 모델 이름으로 변경해주세요
    
    result = process_math_audio(audio_file, latex_translation_model, math_detection_model)
    
    print("Final result (audio to mixed Braille/Nemeth):")
    for segment_type, content in result:
        print(f"{segment_type.capitalize()}: {content}")

if __name__ == "__main__":
    main()