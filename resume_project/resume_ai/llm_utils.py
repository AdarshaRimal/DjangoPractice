from huggingface_hub import InferenceClient
from decouple import config


HUGGING_FACE_TOKEN = config('HUGGING_FACE_TOKEN')

client = InferenceClient(api_key=HUGGING_FACE_TOKEN)



def analyze_resume_skills(text):
    try:
        response = client.text_generation( 
            model="mistralai/Mistral-7B-Instruct-v0.2",
            prompt=f"""
            Extract key skills from this resume. Return them as a bullet list:
            ----
            {text}
            ----
            """,
            max_new_tokens=200,
            temperature=0.1,
            stop_sequences=["\n\n"]  
        )
        
        return [line.strip("- ") for line in response.split('\n') if line.startswith('-')]
    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")
        return []

def generate_cover_letter(skills, job_description):
    try:
        response = client.text_generation(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            prompt=f"""
            Write a professional cover letter using these skills: {', '.join(skills)}
            For this job description: {job_description}
            """,
            max_new_tokens=500,
            temperature=0.7
        )
        return response.strip()
    except Exception as e:
        print(f"Error generating cover letter: {str(e)}")
        return "Error generating cover letter. Please try again."