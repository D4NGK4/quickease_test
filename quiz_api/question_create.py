from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def generate_questions(paragraph):
    prompt = (
        f"Convert the following paragraph into at least 10 questions."
        '''Generate the questions with the following structure:
        [
            {
                "Question": "What is your name?"
            },
            {
                "Question": "What is your name?"
            }
    ]
        '''
        f"The format must only be in JSON format."
        f"Only JSON data is required. No other decoraters like ``` are needed."
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": prompt },
            {"role": "user", "content": paragraph},
        ],
        max_tokens=500, 
        temperature=0.7,
    )
    
    question_text = response.choices[0].message.content

    return question_text
