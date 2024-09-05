import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

class GenerateNote:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")
    def generate_note(self, lecture_text, year, field_of_study, module, notes_style):
        prompt = PromptTemplate.from_template(
            """
            ### UNIVERSITY LECTURE :
            {lecture_text}

            ###INSTRUCTIONS:
            This lecture is from {year}, focused on {field_of_study} for the upcoming module: {module}.
            
            Your job is to extract concise and relevant notes from this lecture, adhering to the format: {notes_style}.
                        
            Return them in JSON format containing the following keys:lecture title,notes:
            
            Ensure the response contains only the JSON object with the required keys: "lecture_title" and "notes".

            Focus on extracting the most important concepts and key points from the lecture.
            
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt | self.llm
        res = chain_extract.invoke(input={"lecture_text": lecture_text,
                                    "year": year,
                                    "field_of_study": field_of_study,
                                    "module": module,
                                    "notes_style": notes_style})
        print("Raw response content:", res.content)  # Log the raw response
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException as e:
            print("Parsing error:", str(e))  # Log parsing errors
            raise
        return res if isinstance(res, list) else [res]
        
        