from fastapi import FastAPI , Request, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List
from PromptValidator import ValidatePrompt

app = FastAPI()
validator = ValidatePrompt()


class GenerateNotesResponse(BaseModel):
    notes: List[str]
    grade: int

@app.get("/")
def read_root():
    return {" Hello": "World"}

@app.post("/generate_notes")
async def generate_notes(request: Request):
    try:
        data = await request.json()
        if not validator.validate(data.get("prompt")):
            raise HTTPException(status_code=400, detail="Invalid prompt.") 
        else:
             return validator.validate(data.get("prompt"))
        
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    

if __name__ == " __main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




