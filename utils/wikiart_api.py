
from utils.rq import rq
import pandas as pd
import string
from bs4 import BeautifulSoup
import re


def parse_artist_text_list(soup: BeautifulSoup):
    html_table = soup.find("div", {"class": "masonry-text-view masonry-text-view-all"})
    html_rows = html_table.find_all("li")

    data = []

    for row in html_rows:
        spans = row.findAll('span')


        # Some artists (3 off) do not have birth info
        if len(spans) == 2:
            spans = [
                spans[0].contents[0][2:],
                spans[1].contents[0][2:]
            ] 
        else:
            print("Error only one span found: ")
            print(spans)
            print("Will successfully catch if type <span>, n artworks</span> \n")
            spans = [
                None, 
                spans[0].contents[0][2:]
            ]
        
        row = [
            row.find('a').contents[0],
            row.find('a')['href'],
            spans[0],  
            spans[1],          
        ]
        data.append(row)

    df = pd.DataFrame(data, columns=['artist', 'artist_href', 'life', 'num_artworks'])

    #Convert num-art to int
    df['num_artworks'] = df['num_artworks'].str.split().str[0].astype(int)

    return df


def get_artist_list() -> pd.DataFrame:
    combined = pd.DataFrame()

    #Itterate though alphabet
    for c in string.ascii_lowercase:
        html = f'https://www.wikiart.org/en/Alphabet/{c}/text-list'
        r = rq.get(html, proxies=False, delay=1)
        soup = BeautifulSoup(r.text, 'html.parser')
        df = parse_artist_text_list(soup)

        combined = combined.append(df, ignore_index=True)
        
    return combined



def parse_artist_artworks_text_list(soup: BeautifulSoup):
    html_table = soup.find("div", {"class": "view-all-works"})
    html_rows = html_table.find_all("li")

    data = []

    for row in html_rows:
        span = row.find('span')

        if span is not None:
            span = span.contents[0][2:]

        a = row.find('a')

        al = [None, None]

        if a is not None:
            al = [
                row.find('a').contents[0],
                row.find('a')['href']
            ]
    
        row = [
            al[0],
            al[1],
            span         
        ]
        data.append(row)

    df = pd.DataFrame(data, columns=['artwork', 'artwork_href', 'date'])
    return df

def get_artist_artworks(artist_href: str):
    html = f'https://www.wikiart.org{artist_href}/all-works/text-list'
    r = rq.get(html, proxies=False, delay=0.5)
    soup = BeautifulSoup(r.text, 'html.parser')
    return parse_artist_artworks_text_list(soup)


def parse_artwork_data(soup: BeautifulSoup):
    max_res = soup.find("span", {"class": "max-resolution"}).contents[0]
    img_url = soup.find("img", {"itemprop": "image"})['src']


    tags = soup.findAll("a", {"class": "tags-cheaps__item__ref"})

    # Get string and remove whitespace
    tags_str = []
    if len(tags) > 0:
        tags_str = [re.sub('\s+','',tag.contents[0]) for tag in tags]

    d = {
        'max_res' : max_res,
        'img_url' : img_url,
        'tags' : [tags_str]
    }

    for dict in soup.findAll("li", {"class": "dictionary-values"}):
        name = dict.find("s").contents[0][0:-1]

        cont = []
        if name == "Genre":
            for t in dict.findAll('span', {"itemprop": "genre"}):
                cont.append(t.contents[0])
            pass
        else:
            for t in dict.findAll('a'):
                cont.append(t.contents[0])

        d[name] = [cont]

    return pd.DataFrame(d)

def get_artwork_data(artwork_href: str):
    html = f'https://www.wikiart.org{artwork_href}'
    r = rq.get(html, proxies=False, delay=0.5)
    soup = BeautifulSoup(r.text, 'html.parser')
    return parse_artwork_data(soup)

