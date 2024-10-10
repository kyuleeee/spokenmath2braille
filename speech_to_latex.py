import whisper
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#in order to deal with this, I had to install python3.10 version and the interpreter to 3.10 as well. 

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

def correct_errors(text,model_name):
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return corrected_text

def text_to_latex(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained("t5-base") #it got some error when finetuned tokenzier was used 
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    latex_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return latex_text

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
    return latex_text

# 사용 예시
audio_file = "temp.wav"
error_correction_model = "Hyeonsieun/MathSpeech_T5_base_corrector"
latex_translation_model = "Hyeonsieun/MathSpeech_T5_base_translator"

result = process_math_audio(audio_file, error_correction_model, latex_translation_model)
print("Final result:", result)