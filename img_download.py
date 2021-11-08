# %%
from logging import error
from utils.tables import TableManger
import pandas as pd
from pipeline.artwork_data_cleanup import cleanup
from utils.rq import rq

# %%

artwork_data_table = TableManger("data/artwork_data_backup", ext="json")
artwork_data = artwork_data_table.get()

clean_data_table = TableManger("data/clean_data", ext="json")

# %%

clean_data = cleanup(artwork_data)
clean_data_table.save(clean_data, ext="json")



# %%

for index, row in clean_data.iterrows():
    #Continue if already downloaded
    if row['downloaded'] == True:
        continue

    image_url = row["img_url"]
    artist = str(row["artist"]).replace(" ", "")
    artwork = str(row["artwork"]).replace(" ", "")

    ext = "jpg"

    if "png" in image_url:
        ext = "png"

    try:
        img_data = rq.get(image_url, proxies=False, delay=0.25).content
        with open(f"img/{artist}_{artwork}.{ext}", 'wb') as handler:
            handler.write(img_data)

        clean_data.at[index,'downloaded'] = True
        clean_data_table.save(clean_data, ext="json")
    except error as e:
        print(f"Error: {e}")
        continue

clean_data_table.save(clean_data, ext="json")
# %%
