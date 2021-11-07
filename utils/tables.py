
import os, sys
import pandas as pd


if getattr(sys, 'frozen', False):
    __CUR_DIR__ = os.path.dirname(sys.executable)
# or a script file (e.g. `.py` / `.pyw`)
elif __file__:
    __CUR_DIR__ = os.path.dirname(os.path.dirname(__file__))


class TableFunc:
    @staticmethod
    def check_duplicate(df: pd.DataFrame, col_name: str, content) -> bool:
        series = df[col_name]
        return content in set(series)

    @staticmethod
    def lin_norm_column(df: pd.DataFrame, col_name: str):
        return (df[col_name]-df[col_name].min())/(df[col_name].max()-df[col_name].min())

    @staticmethod
    def add_lin_norm_column(df: pd.DataFrame, col_name: str, norm_col_name: str = None):
        if norm_col_name is None:
            norm_col_name = "lin_norm_" + col_name

        df[norm_col_name] = TableFunc.lin_norm_column(df, col_name)
        return df

class TableManger:
  def __init__(self, file_path: str, ext: str= "csv", load=True):

    self.file_path = file_path
    self.ext = ext
    self.df = pd.DataFrame()
    
    if load:
      self.df = TableManger.load(self, ext)


  def load(self, ext: str ="csv", **kwargs) -> pd.DataFrame or None:

    print("Loading data: " + self.file_path + "." + ext)
    self.df = pd.DataFrame()

    try:
      if ext == "csv":
        self.df = pd.read_csv(self.file_path+".csv", sep=",", header=0, index_col=False, **kwargs)
      elif ext == "json":
        self.df = pd.read_json(self.file_path+".json", orient='index', **kwargs)
      elif ext == "xlsx":
        self.df = pd.read_excel(self.file_path+".xlsx", engine='openpyxl', **kwargs)
      elif ext == "pkl":
        self.df = pd.read_pickle(self.file_path+".pkl")
    except Exception as e:
      print("Pandas Load Exception: " + str(e))

    print("Load Complete")
    return self.df

  def get(self) -> pd.DataFrame:
    return self.df

  def save(self, df: pd.DataFrame, ext="csv", file_path=None, **kwargs) -> None:

    print("Saving data: " + self.file_path + "." + ext)

    self.df = df
    if file_path is not None:
      self.file_path = file_path

    if ext == "csv":
      df.to_csv(self.file_path+".csv", sep=",", header=True, index=False, **kwargs)
    elif ext == "json":
      df.to_json(self.file_path+".json", orient='index', indent=2, **kwargs)
    elif ext == "xlsx":
      writer = pd.ExcelWriter(self.file_path+".xlsx", engine='openpyxl', **kwargs)
      df.to_excel(writer, index=False)
      writer.save()
    elif ext == "pkl":
      df.to_pickle(self.file_path+".pkl", **kwargs)

    print("Save Complete")

  def append_to_save(self, df: pd.DataFrame, ext="csv", file_path=None, **kwargs) -> None:
    if file_path is not None:
      self.file_path = file_path

    #Can directly append to CSV
    if ext == "csv":
      self.save(df, ext, file_path, mode='a', header=False, **kwargs)
    else:
      self.df = pd.concat([self.df, df], ignore_index=True)
      self.save(self.df, ext, file_path, **kwargs)
