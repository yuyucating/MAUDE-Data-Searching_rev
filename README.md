_**設計理念:**_  
  
_醫療器材產業為了滿足上市後監督等作業會在 FDA MAUDE 資料庫進行搜尋，搜尋相似品/競品的 incident、recall 等資料，且為了有完整的分析，(如果有能力的話)能分析越多的資料越好。<br>
透過 MAUDE 的搜尋介面可以輸入很多的案件關鍵字，像是廠商名稱、產品名稱等等，我稱之為「關鍵字」，當關鍵字越來越多，每一次搜尋的動作就會增加，都是依些沒必要的人力，但透過 Python 爬蟲就可以節省這些人力。_  
_參考資源: <[MAUDE database](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfMAUDE/search.CFM)>_
  
_**設計優點:**_  
* 減少人力
* 同時可以做其他作業
* 固定蒐集關鍵字 (可以無負擔的慢慢累積!!)

---
### 主程式: Searching_Main_vX.py 
  - GUI設計
    - 關鍵字 excel 輸 input
    - 選擇執行副程式
    - 日期選擇 (選擇將覆蓋關鍵字 excel 日期設定 / 不選擇將引用關鍵字 excel)

### 副程式: (1) my510k (2) recall (3) incident
  - [副程式標題]_Searching.py : 爬蟲編譯內容
  - [副程式標題]_KEY : 從關鍵字 excel 將關鍵字取出 (並回傳給 _Searching.py 進行爬蟲)
