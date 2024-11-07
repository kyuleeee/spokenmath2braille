import openai
from typing import List, Tuple
import re

class SpokenMathDetector:
    def __init__(self, api_key: str, api_base: str, api_type: str = 'azure', api_version: str = '2024-05-01-preview'):
        """Initialize with OpenAI/Azure credentials."""
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_type = api_type
        openai.api_version = api_version
        self.LABEL_LIST = ["O", "B-MATH", "I-MATH"]

    def _create_system_prompt(self) -> str:
        """Create system prompt for spoken mathematics detection."""
        return """
You are a specialized Named Entity Recognition (NER) system designed to detect mathematical expressions in text, particularly in the context of educational videos or lectures.

Your task is to label mathematical expressions in the given text with B-MATH (beginning of a math expression) and I-MATH (inside a math expression). Label non-mathematical parts with O.

When identifying mathematical expressions, consider the following:

1. Numbers and mathematical operators (e.g., +, -, *, /, =, <, >)
2. Mathematical terms and concepts (e.g., vector, matrix, equation, function, derivative)
3. Geometric concepts (e.g., line, plane, angle, triangle)
4. Variables and constants (e.g., x, y, z, pi, e)
5. Mathematical structures (e.g., sets, groups, fields)
6. Coordinate representations (e.g., "two minus one" as a vector component)
7. Equation descriptions (e.g., "x squared plus y squared equals z squared")

Important guidelines:
- Context is crucial. A number alone doesn't always indicate a mathematical expression.
- Pay attention to mathematical verbs (e.g., add, subtract, multiply, divide, integrate, differentiate,equal).
- Consider phrases that describe mathematical operations or relationships.
- Be aware of colloquial ways of expressing mathematical concepts in spoken language.


Examples:
1. Input: The equation x squared plus y squared equals z squared represents a sphere.
   Output: ['O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'O', 'O', 'O']

2. Input: We need to find the derivative of f of x with respect to x.
   Output: ['O', 'O', 'O', 'O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'O']

3. Input: Let's consider the vector two minus one and add it to the matrix.
   Output: ['O', 'O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'O', 'O', 'O', 'O', 'O', 'B-MATH', 'O']

4. Input: The second column is the vector three four five.
   Output: ['O', 'B-MATH', 'I-MATH', 'O', 'O', 'B-MATH', 'I-MATH', 'I-MATH', 'I-MATH', 'I-MATH']

Only return the list of labels, no explanation. Ensure the number of labels matches the number of words exactly."""

    def _create_user_prompt(self, text: str, tokens: List[str]) -> str:
        """Create user prompt with explicit token count."""
        return f"""Text: "{text}"
Words ({len(tokens)}): {tokens}
Return exactly {len(tokens)} labels."""

    def tokenize_text(self, text: str) -> List[str]:
        """Simple word tokenization."""
        return [token for token in text.strip().split() if token]

    def _parse_gpt_response(self, response_text: str, num_tokens: int) -> List[str]:
        """Parse and validate GPT response."""
        try:
            # Clean up the response text
            cleaned = response_text.strip()
            # Handle different list formats
            if cleaned.startswith('[') and cleaned.endswith(']'):
                labels = eval(cleaned)
            else:
                # Split on commas if not in proper list format
                labels = [label.strip(' "\'[]') for label in cleaned.split(',')]
            
            # Validate labels
            if len(labels) == num_tokens and all(label in self.LABEL_LIST for label in labels):
                return labels
        except:
            pass
        
        # Fallback: return all O labels
        return ['O'] * num_tokens

    def get_labels(self, text: str) -> Tuple[List[str], List[str]]:
        """Get tokens and their corresponding labels."""
        tokens = self.tokenize_text(text)
        
        try:
            response = openai.ChatCompletion.create(
                engine="gpt1",
                messages=[
                    {"role": "system", "content": self._create_system_prompt()},
                    {"role": "user", "content": self._create_user_prompt(text, tokens)}
                ],
                temperature=0.1,
                max_tokens=1000,
                n=1,
                stop=None
            )
            
            response_text = response.choices[0].message['content'].strip()
            labels = self._parse_gpt_response(response_text, len(tokens))
            return tokens, labels
            
        except Exception as e:
            print(f"Error in get_labels: {e}")
            return tokens, ['O'] * len(tokens)

def spoken_math_detection(text: str, api_config: dict) -> List[Tuple[str, str]]:
    """
    Detect mathematical expressions in spoken text.
    Returns list of (token, label) tuples.
    """
    detector = SpokenMathDetector(
        api_key=api_config['api_key'],
        api_base=api_config['api_base'],
        api_type=api_config.get('api_type', 'azure'),
        api_version=api_config.get('api_version', '2024-05-01-preview')
    )
    
    tokens, labels = detector.get_labels(text)
    return list(zip(tokens, labels))

def detect_math_segments(text: str, api_config: dict) -> List[dict]:
    """
    Convert text into segments with math detection.
    Returns list of segment dictionaries.
    """
    token_labels = spoken_math_detection(text, api_config)
    segments = []
    current_segment = {"type": "text", "content": ""}
    
    for token, label in token_labels:
        if label == "O" and current_segment["type"] == "text":
            current_segment["content"] += token + " "
        elif label in ["B-MATH", "I-MATH"] and current_segment["type"] == "math":
            current_segment["content"] += token + " "
        else:
            if current_segment["content"]:
                current_segment["content"] = current_segment["content"].strip()
                segments.append(current_segment)
            current_segment = {
                "type": "math" if label in ["B-MATH", "I-MATH"] else "text",
                "content": token + " "
            }
    
    if current_segment["content"]:
        current_segment["content"] = current_segment["content"].strip()
        segments.append(current_segment)
    
    return segments

# Example usage
if __name__ == "__main__":
    api_config = {
        'api_key': "-",
        'api_base': "-",
        'api_type': 'azure',
        'api_version': '-'
    }

    test_texts = [
        "The equation x squared plus y squared equals z squared represents a sphere",
        "We need to find the derivative of f of x with respect to x",
        "Let's consider the vector two minus one and add it to the matrix",
        "The second column is the vector three four five",
        "The sine of theta plus the cosine of phi",
        "A right triangle with angle measuring ninety degrees",
        "Solve for y when two x plus three y equals six",
        "The sequence one two three converges to infinity",
        "The complex number two plus i times three"
    ]


    try:
        for text in test_texts:
            print(f"\nInput text: {text}")
            token_labels = spoken_math_detection(text, api_config)
            print("Tokens and labels:")
            for token, label in token_labels:
                print(f"{token}: {label}")
    except Exception as e:
        print(f"Error during testing: {e}")