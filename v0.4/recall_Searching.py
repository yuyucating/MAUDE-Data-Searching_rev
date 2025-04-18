from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import os
import time
import pandas as pd
import recall_takeKEY

def run(folder_path, dataLink, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo):
    
    date_string = date.today().strftime("%Y%m%d") #YYYYMMDD
    
    downloadFolder = os.path.abspath(f"{folder_path}/recall_{date_string}")
    os.makedirs(downloadFolder, exist_ok=True)  # 若資料夾不存在則建立
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": downloadFolder,  # 設定下載路徑
        "download.prompt_for_download": False,       # 不彈出下載提示
        "download.directory_upgrade": True,          # 自動將下載目錄升級
        "safebrowsing.enabled": True                 # 允許下載安全檔案
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm")
    print("開啟網頁\n")

    dataNum = pd.read_excel(dataLink, sheet_name="Recall").shape[0] #取得資料列數, 不包含標題
    # print(dataNum)

    i = 0
    n = 0
    while i<dataNum:
        key = recall_takeKEY.run(dataLink, i)
        print("Recall 搜尋關鍵字", i+1, ": ", key)

        textbox_productName = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='productdescriptiontxt']"))
            )
        
        textbox_productCode = driver.find_element(By.XPATH, "//input[@name='productcode']")
        selector_recallClass = driver.find_element(By.XPATH, "//select[@name='centerclassificationtypetext']")
        textbox_510K = driver.find_element(By.XPATH, "//input[@name='PMA_510K_Num']")
        # textbox_udi = driver.find_element(By.ID, "UDIDI")
        textbox_dateFrom = driver.find_element(By.ID, "postdatefrom")
        textbox_dateTo = driver.find_element(By.ID, "postdateto")
        textbox_recallNumber = driver.find_element(By.XPATH, "//input[@name='recallnumber']")
        
        button_submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Search']")

        textbox_productName.send_keys(key[0])
        textbox_productCode.send_keys(key[1])
        if key[2]:
            selector_recallClass.select_by_value(key[2])
        textbox_510K.send_keys(key[3])
        if read_dateFrom:
            textbox_dateFrom.send_keys(key_dateFrom)
        else:
            textbox_dateFrom.send_keys(key[4])
        if read_dateTo:
            textbox_dateTo.send_keys(key_dateTo)
        else:
            textbox_dateTo.send_keys(key[5])
        textbox_recallNumber.send_keys(key[6])

        button_submit.click()
        print('點擊送出按鈕!')

        try:
            link_download = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Export to Excel')]"))
                )
            link_download.click()
            print("點擊下載")
            link_newSearch = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'New Search')]"))
                )
            link_newSearch.click()
            n+=1
        except:
            print("沒有可下載資料")
            link_newSearch = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'New Search')]"))
                )
            link_newSearch.click()

        i+=1
    time.sleep(2)
    print("一共下載", n, "筆 recall 資料")
    driver.quit()