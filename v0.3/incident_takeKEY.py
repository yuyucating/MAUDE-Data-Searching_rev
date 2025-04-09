import pandas as pd
import numpy as np # 為了處理資料 'nan'

def run(Link):

    myTable = pd.read_excel(Link, sheet_name="Incident", engine='openpyxl')

    # key = myTable.iloc[num].replace({np.nan: ""}).tolist()

    # print(type(key))
    # print(key)

    return(myTable)