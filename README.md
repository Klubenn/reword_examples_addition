# RE-WORD examples enricher
This tiny project is meant to extract all words of specified category, that are not yet learned and that don't have an example for Russian-German version of Reword app. The extracted table would then get updated with examples with the help of AI. After that the examples are entered in the database and the file could be used by the app as a source.

## Prerequisites
To generate examples with the help of AI get the Gemini API key and follow the instructions [here](https://ai.google.dev/gemini-api/docs/api-key#linuxmacos---bash). The use of API is free, although it is subject to limitations such as the number of requests per minute and per day (15 / 1500).

## Usage
1. Launch `1_filter_empty.py` to get the file with words that have no examples.
2. Run `2_generate_examples.py` to get the examples with the help of AI.
3. Execute `3_update_db.py` to update the values in the database.

## Additional notes
Note that the name of the category, database and other variable parameters should be reviewed and changed if needed in the code. The script is not interactive and is practically a one-time use tool, so I don't feel like investing much time in it as soon as it fulfilled all my needs totally. However if you have questions/suggestions feel free to create new issue