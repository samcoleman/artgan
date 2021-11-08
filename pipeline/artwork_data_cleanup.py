import pandas as pd
from utils.tables import TableManger

def cleanup(df: pd.DataFrame):
    res_cols = df['max_res'].str[:-2].str.split(pat="x", expand=True)
    df = df.drop("max_res", axis=1)

    df.columns= df.columns.str.strip().str.lower()

    df["res_x"] = res_cols[0]
    df["res_y"] = res_cols[1]

    df["downloaded"] = False

    df['img_url'] = df['img_url'].str.lower()
    df['img_url'] = df['img_url'].str.replace('!large.jpg' ,'')
    df['img_url'] = df['img_url'].str.replace('!large.jpeg' ,'')
    df['img_url'] = df['img_url'].str.replace('!large.png' ,'')

    return df