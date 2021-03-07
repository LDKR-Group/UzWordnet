# importing needed libraries
import asyncio

import aiohttp
import async_timeout
import pandas as pdd


# function to make a single Google Translate API request and return a single translation string
async def fetch(session, url):
    async with session.post(url) as response:
        resp = await response.json()
        return resp['data']['translations'][0]['translatedText'] # extracting the needed response field from the json response


"""function to fetch all the translations asynchronously from the specified url for the specified lemmas"""
async def fetch_all(url, payload, lemmas):
    async with aiohttp.ClientSession() as session:# initializing session
        target_lemmas = [] # empty array to be filled with translations
        for index,lemma in enumerate(lemmas): # traversing the english lemmas and sending requests using fetch() function
            print(index) # for logging purposes only
            payload['q'] = lemma # modifying the payload to contain the requested for translation lemmas
            target_lemma = await fetch(session, url.format(**payload)) # fetching using the payloaded url string
            target_lemmas.append(target_lemma) # saving individual responses
        return target_lemmas


"""function to write the responses array (line by line - synset by synset) to a specified file"""
def dump_responses(filename, responses):
    with open(filename, 'w+', encoding="utf-8") as f:
        for lemma in responses: # writing translations line by line (synset by synset)
            f.write(lemma + '\n')


"""function to remove repetitive strings (words) withing certain columns"""
def remove_reps(df, col_name):
    for i in range(df.shape[0]): # looping over the dataframe
        row = df.iloc[i][col_name]
        row = row.split(", ")
        df.iloc[i, df.columns.get_loc(col_name)]  = ', '.join(list(dict.fromkeys(row)))

    return df



"""main function"""
def main():
    # constructing the request url to the api (in fetch)
    url = "https://translation.googleapis.com/language/translate/v2?q={q}&target={target}&source={source}&key={key}"
    
    # parameter dict for the query string
    payload = {
        "target" : "uz",
        "source" : "en",
        "key" : "yourkeyhere", # please note: the key is private
        "q" : "none" # to be modified in fetch_all() function
    }
    
    dump_file = "./dump_responses.txt" # file to dump the responses (translations) received from the api
    df = pd.read_csv('./pwn_unindexed.csv') # reading the tabular form of PWN (output of pwn_formatting.py)\

    lemmas = list(df['Lemma(s)'].values) # getting a list of lemmas from the tabular file 
    lemmas = [str(lemma) for lemma in lemmas] # making sure all the read values are strings

    target_lemmas = asyncio.run(fetch_all(url, payload, lemmas)) # asynchronously ask Google Translate API for translations of lemmas

    dump_responses(dump_file, target_lemmas) # backup the responses

    df['Target lemma(s)'] = target_lemmas # filling the respective column with the obtained translations
    df['Target lemma(s)'] = df['Target lemma(s)'].str.replace('&#39;', "'", regex=False) # catch encoded "'" sign

    # saving the intermediary (may be of use in the future) tabular file with translations
    df.to_csv('./uwn_repetitive.csv', index=False, encoding="utf-8") # in .csv format
    df.to_excel("./uwn_xlsx_repetitive.xlsx", index=False, encoding="utf-8") # in .xlsx format

    # getting rid of repetitive words within 'Target lemma(s)' column
    df = remove_reps(df, 'Target lemma(s)')

    # saving the final (without repetitions) tabular file with translations
    df.to_csv('./uwn.csv', index=False, encoding="utf-8") # in .csv format
    df.to_excel("./uwn_xlsx.xlsx", index=False, encoding="utf-8") # in .xlsx format



# calling main function
if __name__ == "__main__":
    main()
