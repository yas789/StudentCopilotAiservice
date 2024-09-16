import json
import os
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
from NoteGenerator import GenerateNote
from Grader import Grader
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from moviepy.editor import VideoFileClip
from typing import Optional
from fastapi import BackgroundTasks
from PromptValidator import ValidatePrompt


app = FastAPI()
note_generator = GenerateNote()
grader = Grader()
validator=ValidatePrompt()

class NoteResponse(BaseModel):
    lecture_title: str
    notes: list[str]
    
# Define static values
STATIC_LECTURE_TEXT = (
    "Mechanics is a branch of physics that deals with the motion of objects and the forces that affect this motion. "
    "It is one of the foundational modules in physics, providing the tools and concepts necessary to understand how and why objects move. "
    "Mechanics covers key concepts such as motion, force, Newton's Laws of Motion, and energy. Motion refers to the change in position of an object over time, "
    "while force is a push or pull acting upon an object as a result of its interaction with another object. Newton's Laws of Motion describe the relationship between "
    "the motion of an object and the forces acting on it. Energy, the capacity to do work, includes both kinetic energy (due to motion) and potential energy (due to position). "
    "Understanding mechanics is essential for solving problems related to motion, designing mechanical systems, and analyzing forces in static and dynamic systems. "
    "Mechanics has wide-ranging applications in fields such as engineering, where it is used to design structures, vehicles, and machines, and in astronomy, where it helps "
    "us understand planetary motion and satellite orbits. In everyday life, mechanics allows us to predict the motion of cars, sports equipment, and more. "
    "This module will cover key topics such as kinematics, the study of motion without considering the forces that cause it, dynamics, the study of forces and why objects move, "
    "work and energy, understanding how forces do work on objects and how energy is conserved in mechanical systems, momentum, the quantity of motion an object has and how it is "
    "conserved in collisions, and rotational motion, the motion of objects that spin or rotate, including the concepts of angular velocity and torque. "
    "A major component of this module will be understanding and applying Newton's three laws of motion, which are fundamental to the study of mechanics."
)

STATIC_YEAR = "1st year undergraduate"
STATIC_FIELD_OF_STUDY = "Physics"
STATIC_MODULE = "Mechanics101"
STATIC_NOTES_STYLE = "bullet points"
STATIC_ORIGINAL_PROMPT = "generate notes"

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate_notes")
async def generate_notes():
    # Use static values to generate notes
    res1 = note_generator.generate_note(
        lecture_text=STATIC_LECTURE_TEXT,
        year=STATIC_YEAR,
        field_of_study=STATIC_FIELD_OF_STUDY,
        module=STATIC_MODULE,
        notes_style=STATIC_NOTES_STYLE
    )
    
    # If res1 is already a Python object, no need to use json.loads
    if isinstance(res1, str):
        data = json.loads(res1)  # Parse only if it's a JSON string
    else:
        data = res1  # Assume it's already a Python object
    
    # Extract notes from the response
    notes = data[0]['notes']
    
    # Grade the generated notes
    res2 = grader.grade(
        result=notes,
        original_prompt=STATIC_ORIGINAL_PROMPT
    )
    print("Score: ", res2)
    
    res3=validator.validate(STATIC_ORIGINAL_PROMPT)
    ##just to try the res3 of validator:
    json_boolean = json.dumps({"boolean_value":res3})
    print("Validate Prompt: ",json_boolean)
    
    return res1,res2,json_boolean
