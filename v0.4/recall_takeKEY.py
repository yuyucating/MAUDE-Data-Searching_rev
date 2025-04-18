import pandas as pd
import numpy as np # 為了處理資料 'nan'


def run(Link, num):

    myTable = pd.read_excel(Link, sheet_name="Recall", engine='openpyxl')

    key = myTable.iloc[num].replace({np.nan: ""}).tolist()

    print(type(key))
    print(key)

    return(key)

# run(r'D:\Una Kuo\CR test\20250312_Recall & Incident\20250312\FDA_Searching_empty.xlsx', 0)
