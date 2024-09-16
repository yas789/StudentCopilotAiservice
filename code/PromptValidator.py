class ValidatePrompt:
    def __init__(self):
        # Initialize valid_prompts as a list
         self.preset_prompts = {
            "generate_notes": "Generate concise and informative notes from the lecture transcript, focusing on key concepts, definitions, and examples.",
            "generate_flashcards": "Create flashcards from the lecture transcript, with key terms or concepts on one side and their definitions or explanations on the other.",
        }
    
    def validate(self, input_prompt):
        print ("Validating prompt")
        try:
            if input_prompt in self.preset_prompts:  # Check membership in the list
                return self.preset_prompts[input_prompt]
            else: 
                return False
        except Exception as e:
            print("General error:", str(e))
            raise
        