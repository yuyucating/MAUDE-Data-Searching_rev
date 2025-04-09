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
import incident_takeKEY

def run(folder_path, dataLink, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo):

    date_string = date.today().strftime("%Y%m%d") #YYYYMMDD
    
    downloadFolder = os.path.abspath(f"{folder_path}/incident_{date_string}")
    os.makedirs(downloadFolder, exist_ok=True)  # 若資料夾不存在則建立
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": downloadFolder,  # 設定下載路徑
        "download.prompt_for_download": False,       # 不彈出下載提示
        "download.directory_upgrade": True,          # 自動將下載目錄升級
        "safebrowsing.enabled": True                 # 允許下載安全檔案
    })


    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfMAUDE/search.CFM")
    print("開啟 Incident 搜尋網頁\n")

    dataNum = pd.read_excel(dataLink, sheet_name="Incident").shape[0] #取得資料列數, 不包含標題
    print("總共有 ", dataNum, "筆數據")

    i = 0
    n = 0
    while i<dataNum:
        key = incident_takeKEY.run(dataLink)
        print("Incident 搜尋關鍵字", i+1, ": ", key.iloc[i].tolist())

        selector_productProblem = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "ProductProblem"))
                )
        selector_eventType = driver.find_element(By.ID, "EventType")
        textbox_manufacturer = driver.find_element(By.ID, "Manufacturer")
        textbox_modelNumber = driver.find_element(By.XPATH, "//input[@name='ModelNumber']")
        textbox_reportNumber = driver.find_element(By.ID, "ReportNumber")
        textbox_brandName = driver.find_element(By.XPATH, "//input[@name='BrandName']")
        textbox_productCode = driver.find_element(By.ID, "ProductCode")
        textbox_UDI = driver.find_element(By.ID, "UDIDI")
        textbox_dateFrom = driver.find_element(By.ID, "ReportDateFrom")
        textbox_dateTo = driver.find_element(By.ID, "ReportDateTo")
        textbox_510 = driver.find_element(By.ID, "PMAPMNNUM")

        button_submit = driver.find_element(By.XPATH, "//input[@type='submit' and @name='Search']")

        print(key['Product Problem'][i], type(key['Product Problem'][i]))

        if pd.notna(key['Product Problem'][i]):
            selector_productProblem.select_by_value(key['Product Problem'][i])
        if pd.notna(key['Event Type'][i]):
            selector_eventType.select_by_value(key['Even Type'][i])
        if pd.notna(key['Manufacturer'][i]):
            textbox_manufacturer.send_keys(key['Manufacturer'][i])
        if pd.notna(key['Model Number'][i]):
            textbox_modelNumber.send_keys(key['Model Number'][i])
        if pd.notna(key['Report Number'][i]):
            textbox_reportNumber.send_keys(key['Report Number'][i])
        if pd.notna(key['Brand Name'][i]):
            textbox_brandName.send_keys(key['Brand Name'][i])
        if pd.notna(key['Product Code'][i]):
            textbox_productCode.send_keys(key['Product Code'][i])
        if pd.notna(key['UDI-Device Identifier'][i]):
            textbox_UDI.send_keys(key['UDI-Device Identifier'][i])
    
        textbox_dateFrom.clear()
        if read_dateFrom:
            textbox_dateFrom.send_keys(key_dateFrom)
        else:
            if pd.notna(key['Date From'][i]):
                textbox_dateFrom.send_keys(key['Date From'][i])
        
        textbox_dateTo.clear()
        if read_dateTo:
            textbox_dateTo.send_keys(key_dateTo)
        else:
            if pd.notna(key['Date To'][i]):
                textbox_dateTo.send_keys(key['Date To'][i])
                
        if pd.notna(key['PMA/510K Number'][i]):
            textbox_510.send_keys(key['PMA/510K Number'][i])

        button_submit.click()
        
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
    print("一共下載", n, "筆 incident 搜尋資料")
    driver.quit()

# run(r'D:\Una Kuo\CR test\20250312_Recall & Incident\20250312\FDA_Searching_empty_Bone Filling System.xlsx')