# UzWordNet
Uzbek WordNet project is aimed at developing the analogue of Princeton WordNet and linking it with the PWN.

## Formatting PWN source files for further use
For the future UWN algorithm, the database file from PWN <em>data.noun</em> was more convenient to use with Python in tabular form. For this reason, Python along with Pandas library was used to obtained a conveniently formatted .csv file for further processing. The script called pwn_formatting is performing this task: it takes <em>data.noun</em> file as input and outputs two tabular files - <em>pwn.csv</em> and <em>pwn_unindexed.csv</em>

## Querying Google Translate API
For communicating with the API, api_translation.py script was written. The script takes <em>pwn_unindexed.csv</em> file (which is the output from pwn_formatting.py) and produces list of files as output:
* <em>dump_responses.txt</em> - used for backup of the responses from the API
* <em>uwn_repetitive.csv</em> - a modified tabular file <em>pwn_unindexed.csv</em> that was filled with translations from the API. May contain repetitions
* <em>uwn_xlsx_repetitive.xlsx</em> - same file as <em>uwn_repetitive.csv</em>, but in .xslx format
* <em>uwn.csv</em> - same as <em>uwn_repetitive.csv</em>, but with no repetitions in individual cells of translations column
* <em>uwn_xlsx.csv</em> - same file as <em>uwn.csv</em>, but in .xslx format

