import time

from bs4 import BeautifulSoup
import requests
import pandas


translation_data = []

NUM_PAGES = 42
for page in range(1, NUM_PAGES+1):
    print(f'Fetching page {page}...')
    response = requests.get(url=f'https://beninlangues.com/fongbe-phrases-audios?page={page}')
    soup = BeautifulSoup(response.text, 'html.parser')

    html_doc = soup.find(name="div", attrs={"class": "col-md-9 card main-content"})\
        .find(name="div", attrs={"class": "py-3 px-2"})

    translation_sections = html_doc.find_all(name="div", attrs={"class": "mb-4"})

    for translation_section in translation_sections:
        translation_divs = translation_section.find_all('div')
        translation_french, translation_fon = translation_divs[0], translation_divs[1]

        text_french_raw = translation_french.text
        text_french = text_french_raw[:text_french_raw.rindex(':')].strip()

        text_fongbe_raw = translation_fon.contents[0]
        text_fongbe = text_fongbe_raw.strip()

        translation_data.append({"french": text_french, "fongbe": text_fongbe})

    time.sleep(1)

dataframe = pandas.DataFrame(translation_data)
dataframe.to_csv("french_fongbe_translation.csv", index=False)
