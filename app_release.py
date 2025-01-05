# 重要 終端機請先執行
# py -m venv env              # 建立 env 虛擬環境
# env\Scripts\activate        # 啟動 env 虛擬環境
# (env) pip install requests  # 安裝 requests 套件
# (env) pip install beautifulsoup4    # 安裝 beautifulsoup4 套件
# (env) pip install -U beautifulsoup4 # 更新套件命令
# (env) pip install lxml html5lib     # 通常還要搭配解析網頁的模組

# (env) pip freeze >requirements.txt  # 儲存使用套件清單


# 抓取參考範例網址
# https://store.steampowered.com/app/1774580/STAR_WARS/
# https://store.steampowered.com/app/227300/Euro_Truck_Simulator_2/
# https://store.steampowered.com/app/2358720/_/
# https://store.steampowered.com/app/1091500/Cyberpunk_2077/
# https://store.steampowered.com/app/2878980/NBA_2K25/
# https://store.steampowered.com/app/1623730/Palworld/
# https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/


import re
import requests
import sqlite3
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def on_button1_click(url):
    try:
        game_name = None
        min_requirement = {'os': '', 'cpu': '', 'ram': '', 'gpu': '',
                           'directx': '', 'rom': ''}
        rec_requirement = {'os': '', 'cpu': '', 'ram': '', 'gpu': '',
                           'directx': '', 'rom': ''}

        html = requests.get(url)
        # 使用內建的解析器 html.parser
        soup = BeautifulSoup(html.text, 'html.parser')

        # 將 requests 抓回來的網頁原始碼寫入 index.html
        with open("index.html", 'w', encoding='utf-8') as f:
            f.write(html.text)
        with open("index.html", 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'lxml')

        # 爬蟲
        name = soup.find('div', id='appHubAppName', class_='apphub_AppName')
        game_name = name.get_text(strip=True)
        print(name)

        min = soup.find('strong', string='Minimum:')
        rec = soup.find('strong', string='Recommended:')

        min_find = min.find_next('ul').find('strong', string="OS:")
        if min_find:
            min_requirement["os"] = min_find.find_next_sibling(text=True)
            # text=True只抓取內文
        rec_find = rec.find_next('ul').find('strong', string="OS:")
        if rec_find:
            rec_requirement["os"] = rec_find.find_next_sibling(text=True)

        min_find = min.find_next('ul').find('strong', string="Processor:")
        if min_find:
            min_requirement["cpu"] = min_find.find_next_sibling(text=True)
        rec_find = rec.find_next('ul').find('strong', string="Processor:")
        if rec_find:
            rec_requirement["cpu"] = rec_find.find_next_sibling(text=True)

        min_find = min.find_next('ul').find('strong', string="Memory:")
        if min_find:
            pattern = re.compile(r'\s?([0-9]*\sGB)')
            match = pattern.findall(min_find.find_next_sibling(text=True))
            min_requirement["ram"] = match[0]
        rec_find = rec.find_next('ul').find('strong', string="Memory:")
        if rec_find:
            pattern = re.compile(r'\s?([0-9]*\sGB)')
            match = pattern.findall(rec_find.find_next_sibling(text=True))
            rec_requirement["ram"] = match[0]

        min_find = min.find_next('ul').find('strong', string="Graphics:")
        if min_find:
            min_requirement["gpu"] = min_find.find_next_sibling(text=True)
        rec_find = rec.find_next('ul').find('strong', string="Graphics:")
        if rec_find:
            rec_requirement["gpu"] = rec_find.find_next_sibling(text=True)

        min_find = min.find_next('ul').find('strong', string="DirectX:")
        if min_find:
            pattern = re.compile(r'\s?[A-Za-z]*\s?([0-9]*)')
            match = pattern.findall(min_find.find_next_sibling(text=True))
            min_requirement["directx"] = match[0]
        rec_find = rec.find_next('ul').find('strong', string="DirectX:")
        if rec_find:
            pattern = re.compile(r'\s?[A-Za-z]*\s?([0-9]*)')
            match = pattern.findall(rec_find.find_next_sibling(text=True))
            rec_requirement["directx"] = match[0]

        min_find = min.find_next('ul').find('strong', string="Storage:")
        if min_find:
            pattern = re.compile(r'\s?([0-9]*\sGB)')
            match = pattern.findall(min_find.find_next_sibling(text=True))
            min_requirement["rom"] = match[0]
        min_find = min.find_next('ul').find('strong', string="Hard Drive:")
        if min_find:
            pattern = re.compile(r'\s?([0-9]*\sGB)')
            match = pattern.findall(min_find.find_next_sibling(text=True))
            min_requirement["rom"] = match[0]
        rec_find = rec.find_next('ul').find('strong', string="Storage:")
        if rec_find:
            pattern = re.compile(r'\s?([0-9]*\sGB)')
            match = pattern.findall(rec_find.find_next_sibling(text=True))
            rec_requirement["rom"] = match[0]
        rec_find = rec.find_next('ul').find('strong', string="Hard Drive:")
        if rec_find:
            pattern = re.compile(r'\s?([0-9]*\sGB)')
            match = pattern.findall(rec_find.find_next_sibling(text=True))
            rec_requirement["rom"] = match[0]

        # 資料庫儲存資料
        conn = sqlite3.connect('game_info.db')
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS contacts(
                name TEXT, min_os TEXT, min_cpu TEXT, min_ram TEXT,
                min_gpu TEXT, min_directx TEXT, min_rom TEXT,
                rec_os TEXT, rec_cpu TEXT, rec_ram TEXT, rec_gpu TEXT,
                rec_directx TEXT, rec_rom TEXT)''')
        cursor.execute("INSERT OR IGNORE INTO contacts(name, min_os, min_cpu,\
                       min_ram, min_gpu, min_directx, min_rom, rec_os,\
                       rec_cpu, rec_ram, rec_gpu, rec_directx, rec_rom)\
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (game_name, min_requirement['os'],
                        min_requirement['cpu'], min_requirement['ram'],
                        min_requirement['gpu'], min_requirement['directx'],
                        min_requirement['rom'], rec_requirement['os'],
                        rec_requirement['cpu'], rec_requirement['ram'],
                        rec_requirement['gpu'], rec_requirement['directx'],
                        rec_requirement['rom']))
        # cursor.execute("SELECT * FROM contacts")
        cursor.execute('SELECT name FROM contacts')
        result_all = cursor.fetchall()
        box['values'] = result_all
        box.set('{'+game_name+'}')
        # contacts = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
    except:
        messagebox.showinfo('', '錯誤')


def on_button2_click():
    # 清空
    try:
        conn = sqlite3.connect('game_info.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts")
        conn.commit()
        cursor.close()
        conn.close()
        box['values'] = ''
        box.set('')
        listbox.delete(0, last=100)
    except:
        messagebox.showinfo('', '錯誤')


def on_button3_click(nm):
    try:
        listbox.delete(0, last=100)
        conn = sqlite3.connect('game_info.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ?",
                       (nm,))
        contacts = cursor.fetchall()
        for row in contacts:
            listbox.insert(tk.END, "最低配備: ")
            listbox.insert(tk.END, "作業系統: " + row[1])
            listbox.insert(tk.END, "處理器: " + row[2])
            listbox.insert(tk.END, "記憶體: " + row[3])
            listbox.insert(tk.END, "顯示卡: " + row[4])
            listbox.insert(tk.END, "DirectX: " + row[5])
            listbox.insert(tk.END, "儲存空間: " + row[6])
            listbox.insert(tk.END, "")
            listbox.insert(tk.END, "建議配備: ")
            listbox.insert(tk.END, "作業系統: " + row[7])
            listbox.insert(tk.END, "處理器: " + row[8])
            listbox.insert(tk.END, "記憶體: " + row[9])
            listbox.insert(tk.END, "顯示卡: " + row[10])
            listbox.insert(tk.END, "DirectX: " + row[11])
            listbox.insert(tk.END, "儲存空間: " + row[12])
        conn.commit()
        cursor.close()
        conn.close()
    except:
        messagebox.showinfo('', '錯誤')


form = tk.Tk()
form.title("抓取steam遊戲系統需求")

form.geometry("800x600")
form.resizable(0, 0)
label1 = tk.Label(text="URL輸入欄")
label1.pack(padx=10, pady=0)
entry1 = tk.Entry(width=100)
entry1.pack(padx=10, pady=0)
label2 = tk.Label(text="", height=1)
label2.pack(padx=10, pady=0)
label3 = tk.Label(text="資料庫內遊戲選擇")
label3.pack(padx=10, pady=0)
conn = sqlite3.connect('game_info.db')
cursor = conn.cursor()
try:
    cursor.execute('SELECT name FROM contacts')
    result_all = cursor.fetchall()
    box = ttk.Combobox(values=result_all, width=97, state="readonly")
except:
    box = ttk.Combobox(values="", width=97, state="readonly")

conn.commit()
cursor.close()
conn.close()
box.pack(padx=10, pady=0)

listbox = tk.Listbox()
listbox.pack(fill="both", expand=True, padx=10, pady=10)


button1 = tk.Button(form, text="爬蟲",
                    command=lambda: on_button1_click(entry1.get()), width=10,
                    height=1)
button1.pack(side="left", anchor="s", padx=10, pady=10)

button4 = tk.Button(form, text="資料庫搜索",
                    command=lambda: on_button3_click(
                        box.get().strip('{').strip('}')),
                    width=10, height=1)
button4.pack(side="left", anchor="s", padx=10, pady=10)

button2 = tk.Button(form, text="清空資料庫", command=lambda: on_button2_click(),
                    width=10, height=1)
button2.pack(side="left", anchor="s", padx=10, pady=10)

button3 = tk.Button(form, text="離開", command=form.quit, width=10, height=1)
button3.pack(side="left", anchor="s", padx=10, pady=10)


form.mainloop()
