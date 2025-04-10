import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox
from pathlib import Path
import my510k_Searching
import recall_Searching
import incident_Searching
import find_downloadfolder

choose_case = 0

window = tk.Tk()
window.title('FDA 資料搜尋')
window.geometry('250x280')

checkbutton_510_var = tk.BooleanVar()
checkbutton_recall_var = tk.BooleanVar()
checkbutton_incident_var = tk.BooleanVar()

def runtest(): 
    
    downloadFolder_path = find_downloadfolder.get_download_folder()
    dataInput = "FDA_Searching_empty_Bone Filling System.xlsx"

    if datechoosen_from.get()=="尚未選擇起始日期":
        read_dateFrom = False
        key_dateFrom = ""
    else:
        read_dateFrom = True
        key_dateFrom = datechoosen_from.get()
    
    if datechoosen_to.get()=="尚未選擇結束日期":
        read_dateTo = False
        key_dateTo = ""
    else:
        read_dateTo = True
        key_dateTo = datechoosen_to.get()

    if checkbutton_510_var.get():
        my510k_Searching.run(downloadFolder_path, dataInput, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo)

    # return() # 移除、run()不需要回傳值
    if checkbutton_recall_var.get():
        recall_Searching.run(downloadFolder_path, dataInput, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo)

    if checkbutton_incident_var.get():
        incident_Searching.run(downloadFolder_path, dataInput, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo)

def run(): 
    
    downloadFolder_path = find_downloadfolder.get_download_folder()
    
    if not(dataLink.get()):
        messagebox.showinfo('showinfo', '請輸入關鍵字路徑')
    else:
        dataInput = Path(dataLink.get())
    
        if datechoosen_from.get()=="尚未選擇起始日期":
            read_dateFrom = False
            key_dateFrom = ""
        else:
            read_dateFrom = True
            key_dateFrom = datechoosen_from.get()
        
        if datechoosen_to.get()=="尚未選擇結束日期":
            read_dateTo = False
            key_dateTo = ""
        else:
            read_dateTo = True
            key_dateTo = datechoosen_to.get()

        if checkbutton_510_var.get():
            my510k_Searching.run(downloadFolder_path, dataInput, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo)

        # return() # 移除、run()不需要回傳值
        if checkbutton_recall_var.get():
            recall_Searching.run(downloadFolder_path, dataInput, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo)

        if checkbutton_incident_var.get():
            incident_Searching.run(downloadFolder_path, dataInput, read_dateFrom, key_dateFrom, read_dateTo, key_dateTo)

def dateFrom():
    def dateFromGet():
        dateFrom = calendar_from.selection_get()
        year_From = tk.StringVar()
        year_From.set(str(dateFrom.year))
        month_From = tk.StringVar()
        month_From.set(str(dateFrom.month))
        day_From = tk.StringVar()
        day_From.set(str(dateFrom.day))
        datechoosen_from.set(month_From.get()+"/"+day_From.get()+"/"+year_From.get())
        window_cal_from.destroy()
        
    window_cal_from = tk.Toplevel(window)
    window_cal_from.title("選擇起始日期")
    calendar_from = Calendar(window_cal_from, selectmode="day")
    calendar_from.pack()
    button_cal_from = ttk.Button(window_cal_from, text="確認", command=dateFromGet)
    button_cal_from.pack()

def dateTo():
    def dateToGet():
        dateTo = calendar_to.selection_get()
        year_To = tk.StringVar()
        year_To.set(str(dateTo.year))
        month_To = tk.StringVar()
        month_To.set(str(dateTo.month))
        day_To = tk.StringVar()
        day_To.set(str(dateTo.day))
        datechoosen_to.set(month_To.get()+"/"+day_To.get()+"/"+year_To.get())
        window_cal_to.destroy()
        
    window_cal_to = tk.Toplevel(window)
    window_cal_to.title("選擇結束日期")
    calendar_to = Calendar(window_cal_to, selectmode="day")
    calendar_to.pack()
    button_cal_to = ttk.Button(window_cal_to, text="確認", command=dateToGet)
    button_cal_to.pack()

def clean_dateFrom():
    datechoosen_from.set("尚未選擇起始日期")
def clean_dateTo():
    datechoosen_to.set("尚未選擇結束日期")

textbox = ttk.Label(window, text='請選擇輸入資料讀取(excel)路徑')
textbox.pack(pady=5)

dataLink = ttk.Entry(window)
dataLink.pack(fill="x", pady=5)

textbox = ttk.Label(window, text='請選擇執行項目')
textbox.pack()

checkbutton_510 = ttk.Checkbutton(window, text='搜尋 510(k) 資料', variable=checkbutton_510_var) # 觸發 checkbutton_510_var 可使用
checkbutton_510.pack(anchor="w", padx=65) # 布局加入!
# checkbutton_510.deselect()
checkbutton_recall = ttk.Checkbutton(window, text='搜尋 Recall', variable=checkbutton_recall_var)
checkbutton_recall.pack(anchor="w", padx=65) # 布局加入!
checkbutton_incident = ttk.Checkbutton(window, text='搜尋 Incident', variable=checkbutton_incident_var)
checkbutton_incident.pack(anchor="w", padx=65) # 布局加入

frame_datechoosen = tk.Frame(window)
frame_datechoosen.pack(pady=5)
label_dateFrom = ttk.Label(frame_datechoosen, text="起始日期").grid(row=0, column=0, padx=5)
datechoosen_from = tk.StringVar()
datechoosen_from.set("尚未選擇起始日期")
label_datechoosen_from = ttk.Label(frame_datechoosen, textvariable=datechoosen_from).grid(row=0, column=1, padx=2)
img_cal = Image.open(r"Img\calendar.png")
resized_img_cal = img_cal.resize((16,16), Image.LANCZOS)
btn_img_cal = ImageTk.PhotoImage(resized_img_cal) #轉成 tkinter 可以用的 image
button_date_from = ttk.Button(frame_datechoosen, text="選擇起始日期", image=btn_img_cal, command=dateFrom).grid(row=0, column=2)
button_dateFrom_clean = ttk.Button(frame_datechoosen, text="清除", width=5, command=clean_dateFrom).grid(row=0, column=3, padx=5)
label_dateFrom = ttk.Label(frame_datechoosen, text="結束日期").grid(row=1, column=0, padx=5)
datechoosen_to = tk.StringVar()
datechoosen_to.set("尚未選擇結束日期")
label_datechoosen_to = ttk.Label(frame_datechoosen, textvariable=datechoosen_to).grid(row=1, column=1, padx=2)
button_date_to = ttk.Button(frame_datechoosen, text="選擇結束日期", image=btn_img_cal, command=dateTo).grid(row=1, column=2)
button_dateTo_clean = ttk.Button(frame_datechoosen, text="清除", width=5, command=clean_dateTo).grid(row=1, column=3, padx=5)

button_run = ttk.Button(window, text='執行', command=run)
button_run.pack(side="bottom", pady=5)

button_test = ttk.Button(window, text='以預設檔案進行測試', command=runtest)
button_test.pack(side="bottom", pady=5)


window.mainloop() # 使程式持續執行