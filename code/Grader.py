import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

class Grader:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def grade(self, result, original_prompt):
        prompt = PromptTemplate.from_template(
            """
            ###TASK:
            Evaluate the next provided result: {result} based on the following original prompt: {original_prompt}:
            
            ###CRITERIA FOR GRADING:
            1. Adherence to Prompt: How well the result follows the instructions and requirements given in the original prompt.
            2. Relevance: How relevant the result is to the context or topic specified in the original prompt.
            3. Clarity: The clarity and readability of the result.
            4. Conciseness: Whether the result is succinct and avoids unnecessary information.
            5. Accuracy: The correctness and precision of the information (if applicable).
            
            ###INSTRUCTION:
            Grade the provided result on a scale from 0 to 100:
                    100: Perfect—fully meets all criteria and the original prompt's requirements.
                    0: Completely unsatisfactory—fails to meet the prompt’s requirements.
            ###OUTPUT:
            Return the grade as a single number (0-100) in JSON format, with no additional text, explanation, or commentary. Use the following format:
            
                "grade": <number>
            
            """
        )
        
        chain_extract = prompt | self.llm
        try:
            res = chain_extract.invoke(input={"result": result, "original_prompt": original_prompt})
            print("Raw response content:", res.content)  # Log the raw response
            if res.content.startswith("{") and res.content.endswith("}"):
                json_parser = JsonOutputParser()
                res = json_parser.parse(res.content)
            else:
                raise ValueError("Response is not in valid JSON format.")
        except OutputParserException as e:
            print("Parsing error:", str(e))  # Log parsing errors
            raise
        except Exception as e:
            print("General error:", str(e))  # Catch other errors (e.g., network issues)
            raise
        return res
