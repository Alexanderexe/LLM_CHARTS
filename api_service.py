import openai
import json
import time
from config import OPENAI_API_KEY, OPENAI_MODEL, TEMPERATURE, MAX_TOKENS

class APIService:
    def __init__(self):
        """Initialize the API service with the OpenAI API key."""
        openai.api_key = OPENAI_API_KEY
        
    def analyze_documentation(self, system_prompt, user_prompt):
        """
        Send a request to the OpenAI API to analyze medical documentation.
        
        Args:
            system_prompt (str): The system prompt to guide the AI.
            user_prompt (str): The user prompt containing the medical documentation.
            
        Returns:
            dict: The API response or None if an error occurred.
        """
        try:
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            return response
        except Exception as e:
            print(f"API Error: {e}")
            # Implement exponential backoff for rate limits
            if "rate limit" in str(e).lower():
                wait_time = 10
                print(f"Rate limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                return self.analyze_documentation(system_prompt, user_prompt)
            return None
            
    def parse_response(self, response):
        """
        Parse the API response to extract answers to the medical questions.
        
        Args:
            response (dict): The API response from OpenAI.
            
        Returns:
            dict: A dictionary of answers to the medical questions.
        """
        if response is None:
            return {}
            
        try:
            answer_text = response.choices[0].message.content
            
            # Extract answers to each question
            answers = {
                "mental_status_exam": self._extract_answer(answer_text, "1.", "2."),
                "suicide_homicide_assessment": self._extract_answer(answer_text, "2.", "3."),
                "diagnosis": self._extract_answer(answer_text, "3.", "4."),
                "diagnosis_supported": self._extract_answer(answer_text, "4.", "5."),
                "appropriate_medication": self._extract_answer(answer_text, "5.", "6."),
                "medication_details": self._extract_answer(answer_text, "6.", "7."),
                "comments": self._extract_answer(answer_text, "7.", "8."),
                "controlled_substances": self._extract_answer(answer_text, "8.", "9."),
                "drug_screening": self._extract_answer(answer_text, "9.", "10."),
                "vital_signs": self._extract_answer(answer_text, "10.", None)
            }
            
            return answers
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {}
            
    def _extract_answer(self, text, start_marker, end_marker):
        """
        Extract text between markers.
        
        Args:
            text (str): The text to extract from.
            start_marker (str): The starting marker.
            end_marker (str): The ending marker (can be None for last answer).
            
        Returns:
            str: The extracted text.
        """
        try:
            start_pos = text.find(start_marker)
            if start_pos == -1:
                return ""
                
            start_pos += len(start_marker)
            
            if end_marker is None:
                return text[start_pos:].strip()
                
            end_pos = text.find(end_marker, start_pos)
            if end_pos == -1:
                return text[start_pos:].strip()
                
            return text[start_pos:end_pos].strip()
        except Exception:
            return "" 