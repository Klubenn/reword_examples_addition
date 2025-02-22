import time
from google import genai
import os
import re
import pandas as pd


filename = 'filtered.csv'
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def convert_text_to_reword_format(text):
    text = [t.strip('\n') for t in text.split('\n***\n')]
    print(text)
    if len(text) == 4:
        line = '[{{"o":"{text0}","t":"{text1}"}},{{"o":"{text2}","t":"{text3}"}}]'
        return line.format(text0=text[0], text1=text[1], text2=text[2], text3=text[3])
    

def make_request(word, translation):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"Write 2 sentences in German with the word {word} with the meaning {translation} and translate them to Russian. The word {word} should be surrounded by # signs attached to the word both in original and translation. Sentences and translations should be separated by a *** sequence. The order should be sentence1 *** translation1 *** sentence2 *** translation2. Don't write anything else in your response except the sentences and translations.",
    )
    return(convert_text_to_reword_format(response.text))


def clean_word(word):
    pattern = r'\(die \w+\)'
    return re.sub(pattern, '', word).strip()


while True:
    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        try:
            if pd.isna(row['EXAMPLES_RUS']):
                cleaned_word = clean_word(row['WORD'])
                example = make_request(cleaned_word, row['RUS'])
                df.at[index, 'EXAMPLES_RUS'] = example
                time.sleep(1)
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            # Save intermediate results
            df.to_csv(filename, index=False)
            time.sleep(10)
            break
    else:
        # Save the final DataFrame to a new CSV file
        df.to_csv(filename, index=False)
        break
