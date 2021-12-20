#%%
from utils.wikiart_api import get_artist_list, get_artist_artworks, get_artwork_data
from utils.tables import TableManger, TableFunc
import pandas as pd
from pipeline.artwork_data_cleanup import cleanup

#%%
#artist_list = TableManger("data/artists", ext="csv", load=False)
#t = get_artist_list()
#artist_list.save(t, ext='csv')


"""
artwork_list_table = TableManger("data/artworks", ext="csv")
artworks_list = artwork_list_table.get()

artist_list = TableManger("data/artists", ext="csv")
artist_list = artist_list.get()

for index, row in artist_list.iterrows():
    #Pass if artists artworks have already been found
    if len(artworks_list.index) == 0:
        print("No data stored in data\\artworks.csv")
    elif artworks_list['artist_href'].str.contains(row['artist_href']).any():
        print(f"Already found works for {row['artist_href']}")
        continue

    artworks = get_artist_artworks(row['artist_href'])
    artworks['artist_href'] = row['artist_href']
    artworks['artist'] = row['artist']
    artworks['life'] = row['life']
    artworks['num_artworks'] = row['num_artworks']

    artworks_list = artworks_list.append(artworks, ignore_index=True)
    artwork_list_table.save(artworks_list, ext="csv")
    
print("All artist artworks linked")
"""

# %%

artwork_list_table = TableManger("data/artworks", ext="csv")
artworks_list = artwork_list_table.get()

artwork_data_table = TableManger("data/artwork_data", ext="json")
artwork_data = artwork_data_table.get()

#Drop rows where artwork_href has not been found
artworks_list = artworks_list[artworks_list['artwork_href'].notnull()]

last_artist = ""
data = pd.DataFrame()

i = 0
l = len(artworks_list.index)
for index, row in artworks_list.iterrows():
    i += 1

    #Pass if artists artworks have already been found
    if len(artwork_data.index) == 0:
        print("No data stored in data\\artwork_data.json")
    #This is so inefficient!!! at large scales
    elif artwork_data['artwork_href'].eq(row['artwork_href']).any(): #.str.contains(row['artwork_href']).any():
        #print(f"Already collected artwork data for {row['artwork_href']}")
        continue

    #Pass if artwork_href incorrect format 
    if row['artwork_href'][0:3] != "/en":
        continue

    try:
        data = get_artwork_data(row['artwork_href'])
        data['artwork'] = row['artwork']
        data['artwork_href'] = row['artwork_href']
        data['date'] = row['date']

        data['artist_href'] = row['artist_href']
        data['artist'] = row['artist']
        data['life'] = row['life']
        data['num_artworks'] = row['num_artworks']

        artwork_data = artwork_data.append(data, ignore_index=True)
        
        if row['artist'] != last_artist:
            artwork_data_table.save(artwork_data, ext="json")
            last_artist = row['artist']

            print(f"Progress: {i*100/l}%")
    except:
        continue

#%%
artwork_data_table = TableManger("data/artwork_data", ext="json")
artwork_data = artwork_data_table.get()

clean_data_table = TableManger("data/clean_data", ext="json")
clean_data = clean_data_table.get()

clean_data = cleanup(artwork_data)

clean_data["downloaded"] = False

clean_data_table.save(clean_data, ext="json")
# %%
