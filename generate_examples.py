from google import genai
import os
import re
import pandas as pd

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def convert_text_to_reword_format(text):
    text = text.split('\n***\n')
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


# Чтение данных из файла filtered.csv
df = pd.read_csv('filtered.csv')

# Создание новой колонки EXAMPLES_RUS
df['EXAMPLES_RUS'] = df.apply(lambda row: make_request(clean_word(row['WORD']), row['RUS']), axis=1)

# Сохранение обновленного DataFrame в новый CSV файл
df.to_csv('filtered_with_examples.csv', index=False)

df = pd.read_csv('filtered_with_examples.csv')
df['EXAMPLES_RUS'] = df['EXAMPLES_RUS'].apply(convert_text_to_reword_format)
df.to_csv('filtered_with_examples_fixed.csv', index=False)
