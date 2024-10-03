from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def fix_summary(paragraph: str):
    prompt = (
        f"You are going to fix the summarized text "
        f"Fix it so that it is precise to the original summary but non repeatitive. "
        "There should only be one overview summary and one detailed breakdown of everything"
        "Respond in html format only use ordered list, headings, and unordered list. Remove extras like ``` or the tag/word html and do not use markdowns elements. You may also read inline LaTex and block LaTex formulas"
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": prompt },
            {"role": "user", "content": paragraph},
        ],
        temperature=0.7,
    )
    
    title = response.choices[0].message.content
    

    return title