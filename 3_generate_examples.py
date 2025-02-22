import time
from google import genai
import os
import re
import pandas as pd
import yaml

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

filename = 'filtered.csv'
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def convert_text_to_reword_format(text):
    text = [t.strip(' \n') for t in text.split('***')]
    if len(text) == 4:
        line = '[{{"o":"{text0}","t":"{text1}"}},{{"o":"{text2}","t":"{text3}"}}]'
        return line.format(text0=text[0], text1=text[1], text2=text[2], text3=text[3])
    

def make_request(word_translation_pairs):
    contents = f"Here is the list of tuples where the first element is the {config['target_language']} word and the second is it's {config['native_language']} translation and meaning you should take into consideration: {word_translation_pairs}. For each of the pairs write 2 sentences in {config['target_language']} and translate them to {config['native_language']}. The {config['target_language']} word from the tuple as well as it's translation should be surrounded by # signs attached to the word.  Sentences and translations should be separated with this combination of three characters: ***. The order should be: sentence1 *** translation1 *** sentence2 *** translation2. The sequences corresponding to tuples should be separated from each other with this combination of three characters: $$$. Don't write anything else in your response except the sentences and translations collected into sequences."
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=contents,
    )
    return [convert_text_to_reword_format(text) for text in response.text.split('$$$')]


def clean_word(word):
    pattern = r'\(die \w+\)'
    return re.sub(pattern, '', word).strip()


while True:
    df = pd.read_csv(filename)
    word_translation_pairs = []
    indices = []
    for index, row in df.iterrows():
        try:
            if pd.isna(row[config['examples_column']]):
                print(f"Processing row {index}")
                cleaned_word = clean_word(row['WORD'])
                word_translation_pairs.append((cleaned_word, row[config['translation_column']]))
                indices.append(index)
                if len(word_translation_pairs) == 10:
                    examples = make_request(word_translation_pairs)
                    for i, example in zip(indices, examples):
                        df.at[i, config['examples_column']] = str(example)
                    word_translation_pairs = []
                    indices = []
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            # Save intermediate results
            df.to_csv(filename, index=False)
            time.sleep(10)
            break
    else:
        # Process any remaining words
        if word_translation_pairs:
            examples = make_request(word_translation_pairs)
            for i, example in zip(indices, examples):
                df.at[i, config['examples_column']] = str(example)
        # Save the final DataFrame to a new CSV file
        df.to_csv(filename, index=False)
        break
