from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd
import my510k_takeKEY

def run(dataLink, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo):
    downloadFolder = os.path.abspath("C:/Users/Administrator/Downloads/510(k)")
    os.makedirs(downloadFolder, exist_ok=True)  # 若資料夾不存在則建立
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": downloadFolder,  # 設定下載路徑
        "download.prompt_for_download": False,       # 不彈出下載提示
        "download.directory_upgrade": True,          # 自動將下載目錄升級
        "safebrowsing.enabled": True                 # 允許下載安全檔案
    })

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm")
    print("開啟 510(k) 網頁\n")

    print(dataLink)

    if dataLink.startswith("k"):
        textBox_510k = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "KNumber"))
            )
        button_submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Search']")

        textBox_510k.send_keys(dataLink)
        button_submit.click()

    else:
        print("讀取 excel，讀取資料...")

        dataNum = pd.read_excel(dataLink, sheet_name="510(k)").shape[0] #取得資料列數, 不包含標題
        # print(dataNum)

        i = 0
        n = 0
        while i< dataNum:
            key = my510k_takeKEY.run(dataLink, i)
            print("510(k) data 搜尋關鍵字", i+1, ": ", key)

            textBox_510k = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "KNumber"))
            )

            # textBox_510k = driver.find_element(By.ID, "KNumber")
            selector_Type = Select(driver.find_element(By.ID, "Type"))
            textBox_ProductCode = driver.find_element(By.NAME, "ProductCode")
            textBox_Applicant = driver.find_element(By.ID, "Applicant")
            textBox_DeviceName = driver.find_element(By.NAME, "DeviceName")
            selector_Panel = Select(driver.find_element(By.ID, "Panel"))
            dateFrom = driver.find_element(By.ID, "DecisionDateFrom")
            dateTo = driver.find_element(By.ID, "DecisionDateTo")

            textBox_510k.send_keys(key[0])
            if key[1]:
                selector_Type.select_by_value(key[1])
            textBox_ProductCode.send_keys(key[2])
            textBox_Applicant.send_keys(key[3])
            textBox_DeviceName.send_keys(key[4])
            if key[5]:
                selector_Panel.select_by_value(key[5])
            dateFrom.clear()
            if read_dateFrom:
                dateFrom.send_keys(key_dateFrom)
            else:
                dateFrom.send_keys(key[6])
            dateTo.clear()
            if read_dateFrom:
                dateTo.send_keys(key_dateTo)
            else:
                dateTo.send_keys(key[7])
            button_submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Search']")
            
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
        print("一共下載", n, "筆 510(k) 搜尋檔案")
        driver.quit()
