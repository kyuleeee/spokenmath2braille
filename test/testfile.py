import openai 
from datasets import load_dataset


dataset = load_dataset("1anonymous1/MathSpeech")

def tokenize_text(text):
        """Simple word tokenization."""
        return [token for token in text.strip().split() if token]

def generate_answer(text,prompt): 
  openai.api_key = api_key
  openai.api_base = api_base
  openai.api_type = api_type
  openai.api_version = api_version
      try:
            #add transcription! 
            response = openai.ChatCompletion.create(
                engine="gpt1",
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": f'Text: "{text}"\nWords ({len(tokens)}): {tokens}'}
                ],
                temperature=0.1,
                max_tokens=1000,
                n=1,
                stop=None
            )
            #before math 
            response_text = response.choices[0].message['content'].strip()
            response = self._parse_gpt_response(response_text, len(tokens))
      except Exception as e:
            print(f"API error in get_labels: {str(e)}")
            response = "error"
     
     return response
          

def add_to_transcription(dataset,add):
    for i in range(len(dataset)):
      text =dataset['transcription'][i]
      tokens = tokenize_text(text)
      before_after =generate_answer(tokens,prompt)
      before =before_after.strip(',')[0]
      after  =before_after.strip(',')[1]
      
      #put things in the transcription 
      dataset['transcription'][i] = before + dataset['transcription'][i] + after 
      
      # put things in nemeth + braille 
      dataset['nemeth_braille'][i] = text_to_braille(before) +latex_to_nemeth(transcription[i]) + text_to_braille(after)
            
          

def add_to_audio(dataset):
  dataset.add_audio

dataset = load_dataset("1anonymous1/MathSpeech") 
dataset = dataset.map(add_to_transcription, with_indices=True)
dataset = dataset.map(add_nemeth, with_indices=True)
dataset = dataset.map(add_to_audio,with_indices=True)
