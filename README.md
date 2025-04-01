# spokenmath2braille

# Framework Overview 
<img width="1405" alt="Image" src="https://github.com/user-attachments/assets/2be46da6-194b-461d-b8f3-f76924677bb3" />


# Math Audio to Braille Converter

## Overview
This project converts spoken mathematical expressions into Braille, specifically a mix of standard Braille for text and Nemeth Braille for mathematical content. The pipeline processes audio input, detects mathematical segments, and translates them into the appropriate Braille format.

## Features
- Transcribes audio into text
- Corrects transcription errors
- Detects mathematical expressions within the text
- Converts standard text to Braille
- Translates mathematical expressions into LaTeX and then into Nemeth Braille

## Installation
### Prerequisites
- Python 3.7+
- Required libraries: `torch`, `transformers`, `speechrecognition`, `numpy`
- Pre-trained models for error correction, LaTeX translation, and math detection

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/kyuleeee/spokenmath2braille.git
   cd math-audio-to-braille
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Running the Main Script
To process an audio file and convert it to Braille, run:
```bash
python main.py
```
By default, it processes `temp.wav`. To use a different file, modify the `audio_file` variable in `main.py`.

## Code Structure
### `process_math_audio(audio_file, error_correction_model, latex_translation_model, math_detection_model)`
Main function to process an audio file and generate mixed Braille output.

1. **Speech-to-text conversion**: Transcribes the given audio file.
2. **Error correction**: Uses an NLP model to correct transcription errors.
3. **Math detection**: Identifies mathematical expressions in the text.
4. **Segment processing**:
   - Standard text is converted to Braille.
   - Mathematical expressions are converted to LaTeX, then translated into Nemeth Braille.

### `detect_math_segments(text, math_detection_model)`
Splits the corrected text into separate text and math segments.

### `process_text_segment(text)`
Converts regular text into Braille.

### `process_math_segment(text, latex_translation_model)`
Converts mathematical expressions into LaTeX, then translates them into Nemeth Braille.

### `main()`
Defines the models used and processes a sample audio file.

## Models Used
- **Error Correction Model**: `Hyeonsieun/MathSpeech_T5_base_corrector`
- **LaTeX Translation Model**: `Hyeonsieun/MathSpeech_T5_base_translator`
- **Math Detection Model**: `jeongyoun/distilbert-base-uncased-finetuned-ner-increased` -> for more information about Math Detection Model, Please refer to https://github.com/kyuleeee/MiBERT

## Output Format
The final output consists of a list of tuples containing the segment type (`"text"` or `"math"`) and the corresponding Braille representation.

Example:
```
Final result (audio to mixed Braille/Nemeth):
Text: ⠠⠞⠓⠊⠎ ⠊⠎ ⠁ ⠞⠑⠎⠞ ⠎⠑⠝⠞⠑⠝⠉⠑
Math: ⠰⠹⠁⠃⠲⠉⠰⠼
```

## Future Improvements
- Support for more languages and Braille variants
- Optimization for real-time processing
- Improved mathematical expression recognition

## License
This project is licensed under the MIT License.

