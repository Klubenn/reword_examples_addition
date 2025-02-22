# RE-WORD Examples Enricher

This project extracts all words of a specified category that are not yet learned and do not have an example for the Russian-German version of the Reword app. The extracted table is then updated with examples using AI. After that, the examples are entered into the database, and the file can be used by the app as a source.

## Prerequisites

1. To generate examples using AI, obtain the Gemini API key and follow the instructions [here](https://ai.google.dev/gemini-api/docs/api-key#linuxmacos---bash). The use of the API is free, although it is subject to limitations such as the number of requests per minute and per day (15 / 1500).
2. Create a Reword backup file in the Menu section of the app and download it to the current folder. Provide the name of the file for the variable `db_name` in `config.yaml` file. After running all stages, upload it back and use it as a source to restore the data in your app.

## Usage

1. Run `1_find_tables.py` to find the name of the category for which you want to create examples for missing words, change this value in `config.yaml` for the `category` variable. This script will also show the names of the columns which you might need to change in `config.yaml` if your native language is not Russian. If that is the case, you need to change the values of `examples_column` and `translation_column`.
2. Run `2_filter_empty.py` to get the file with words that have no examples.
3. Run `3_generate_examples.py` to generate examples using AI.
4. Run `4_update_db.py` to update the values in the database.

## Additional Notes

Specify the needed parameters in the `config.yaml` file. Note that some other values might have to be changed directly in the code depending on the languages used in your app. Existing settings are proven to work with the Russian-German Reword app and haven't been tested with other languages.  
The response from AI can sometimes give inconsistent results, which might break the functionality, so it is recommended to perform an initial test on a small set, e.g., 25 items, to see if it works.  
The script is practically a one-time use tool, so I didn't invest much time in it once it fulfilled my needs. However, if you have questions or suggestions, feel free to create a new issue.