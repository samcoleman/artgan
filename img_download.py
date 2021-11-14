# %%
from logging import error
from utils.tables import TableManger
import pandas as pd
import os.path

from utils.rq import rq

# %%
clean_data_table = TableManger("data/clean_data", ext="json")
clean_data = clean_data_table.get()
clean_data["filepath"] = ""


#Check if image has already been downloaded
for index, row in clean_data.iterrows():
    image_url = row["img_url"]
    filename = "".join([c for c in row["artwork_href"] if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    ext = "jpg"

    if "png" in image_url:
        ext = "png"

    if os.path.isfile(f"img/{filename}.{ext}"):
        clean_data.at[index,'downloaded'] = True
clean_data_table.save(clean_data, ext="json")
    

# %%
i = 0
l = len(clean_data.index)
for index, row in clean_data.iterrows():
    i +=1
    #Continue if already downloaded
    if row['downloaded'] == True:
        continue

    image_url = row["img_url"]
    filename = "".join([c for c in row["artwork_href"] if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    ext = "jpg"

    if "png" in image_url:
        ext = "png"

    try:
        img_data = rq.get(image_url, proxies=False, delay=0.1).content
        with open(f"img/{filename}.{ext}", 'wb') as handler:
            handler.write(img_data)

        clean_data.at[index,'downloaded'] = True
        clean_data.at[index,'filepath'] = f"img/{filename}.{ext}"
        
        if i % 50 == 0:
            print(f"Completed {i*100/l}%")
            
    except Exception as e:
        print(e)
        continue
# %%
