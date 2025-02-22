# RE-WORD Examples Enricher
This small project is designed to extract all words of a specified category that are not yet learned and do not have an example for the Russian-German version of the Reword app. The extracted table is then updated with examples using AI. After that, the examples are entered into the database, and the file can be used by the app as a source.

## Prerequisites
1. To generate examples with the help of AI, obtain the Gemini API key and follow the instructions [here](https://ai.google.dev/gemini-api/docs/api-key#linuxmacos---bash). The use of the API is free, although it is subject to limitations such as the number of requests per minute and per day (15 / 1500).
2. Create reword backup file in the Menu section of the app and download it to the current folder. After running all stages, upload it back and use as a source to restore the data in your app.

## Usage
1. Run `1_find_tables.py` to find the name of the category for which you want to crete examples for missing words.
2. Run `2_filter_empty.py` to get the file with words that have no examples.
3. Run `3_generate_examples.py` to generate examples with the help of AI.
4. Run `4_update_db.py` to update the values in the database.

## Additional Notes
Note that the name of the category, database, and other variable parameters should be reviewed and changed if needed in the code. The script is not interactive and is practically a one-time use tool, so I don't feel like investing much time in it as soon as it has fulfilled all my needs. However, if you have questions or suggestions, feel free to create a new issue.