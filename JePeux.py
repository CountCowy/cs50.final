#named after JP

#GPT query

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def query_openai(line: str) -> str:
    prompt = """
Use these resources on scansion to guide you in the following actions
https://dcc.dickinson.edu/grammar/latin/general-rules-quantity
https://dcc.dickinson.edu/grammar/latin/quantity-final-syllables
https://dcc.dickinson.edu/grammar/latin/quantity-perfects-and-perfect-participles
https://dcc.dickinson.edu/grammar/latin/quantity-derivatives

Scan the following single line of Latin poetry in dactylic hexameter with maximum philological accuracy.

Line:
" """ + line + """ "

Do the following steps explicitly and in order:

1. Write the line with all elisions marked.
2. Divide it into syllables, paying attention to elisions and dipthongs.
3. Analyze every syllable as long or short, and justify each decision based on the conventions of dactylic hexameter and Latin grammar.
4. Divide the line of poetry into six metrical feet following the conventions of dactylic hexameter.
5. Provide the final scansion in metrical notation.
6. Then give the line again with macrons/breves applied to the syllables.

Rules to follow:
- Check with the resources given to you
- Do not guess; give specific reasons for every syllable.
- If a syllable’s length is metrically forced, say so.
- Use classical pronunciation rules, not ecclesiastical.
- Be explicit about where elision occurs (or does not occur).
- Do not translate or interpret the line.

Return only the analysis, nothing else.
"""
    #print(prompt)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are an expert in latin specializing in Latin poetry in Dactylic Hexameter, like the Aeneid. Do not be confident. Be accurate and admit to confusion. Focus on more on the information around the scansion than the final result. Do not ask follow up questions."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=2000,
            #response_format={"type": "json_object"}
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error: {e}")
        return ""
    

if __name__ == "__main__":
    print(query_openai(input("line? ")))
    
    
#vi superum saevae memorem Iunonis ob iram
#"vī superum saevae memōrem Iūnōnis ob irām" ˘ ˘ ̄ | ̄ ̄ | ˘ ˘ ̄ | ˘ ˘ ̄ | ˘ ˘ ̄ | ̄ ̄
#vī sŭpĕrūm sāevāe mĕmŏrēm Iūnōnĭs ŏb īrām
#vī sŭpĕr|ūm, saēv|aē || mĕmŏr|ēm Iūn|ōnĭs ŏb| īrăm,