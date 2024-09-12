from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def generate_choices(question):
    prompt = (
        f"Create six(6) choices for the following question: {question}. "
        "Generate the choices with the following structure:"
        '''
        [
            {
                "choice": "Choice description",
                "isAnswer": false
            },
            {
                "choice": "Choice description",
                "isAnswer": true
            }
        ]
            '''
        "There should only be one(1) correct answer."
        "The format must only be in JSON format."
        "Only JSON data is required. No other decoraters like ``` are needed."
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": prompt },
            {"role": "user", "content": question},
        ],
        max_tokens=1000, 
        temperature=0.7,
    )
    
    choice_text = response.choices[0].message.content

    return choice_text

