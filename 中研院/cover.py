import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import os
import pandas as pd
import shutil


root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=500, bg='royalblue', relief='raised')
canvas1.pack()

filename = tk.PhotoImage(file ="bggg.gif")
canvas1.create_image(2250, 0.1, anchor=tk.NE, image=filename)

label1 = tk.Label(root, text='File Conversion Tool',  fg="black")

label1.config(font=('helvetica', 20))
canvas1.create_window(150, 60, window=label1)


def getJSON():

    import_file_path = filedialog.askdirectory()
    os.mkdir(import_file_path + "\\json2csv_success")
    # os.mkdir(import_file_path + "\\json2csv_fail")

    filename = os.listdir(import_file_path)
    for i in range(len(filename)):
        data = import_file_path+"/"+filename[i]
        try:
            read_file = pd.read_json(data,encoding='utf_8_sig')
            read_file = pd.DataFrame(read_file)
            # print(read_file)
            read_file.to_csv(import_file_path + "/json2csv_success/" + filename[i][:-4] + ".csv", index=False,encoding='utf_8_sig')
        except:
            # print("Fail")
            print("Fail", filename[i])
            # shutil.copy(data, import_file_path+"/json2csv_fail")

browseButton_JSON = tk.Button(text="     Import JSON File    ", command=getJSON, bg='Gold', fg='black',
                              font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 130, window=browseButton_JSON)


def getXML():

    import_file_path = filedialog.askdirectory()
    filename = os.listdir(import_file_path)
    # os.mkdir(import_file_path + "\\xml2csv_fail")
    os.mkdir(import_file_path + "\\xml2csv_success")
    # print(finename)
    for i in range(len(filename)):
        data = import_file_path +"/"+ filename[i]
        try:
            # print(data)
            tree = ET.parse(data)
            root = tree.getroot()
            nodee = [elem.tag for elem in root.iter()]
            nodee = sorted(set(nodee), key=nodee.index)
            # print(nodee)
            df_columns = pd.DataFrame(columns=nodee)
            no = 0
            for node in root:
                for ii in nodee:
                    try:
                        nodee_content = node.find(ii).text
                        df_columns.at[no, ii] = nodee_content
                    except:
                        pass
                no += 1
            # print(df_columns)
            df_columns.to_csv(import_file_path + "/xml2csv_success/" + filename[i][:-4] + ".csv", index=False)

        except:
            print(filename[i])
            # shutil.copy(data, import_file_path+"/xml2csv_fail")

browseButton_xml = tk.Button(text="      Import XML File     ", command=getXML, bg='Gold', fg='black',
                              font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 180, window=browseButton_xml)

root.mainloop()

#pyinstaller -F cover.py --icon=icon.ico
#pyinstaller --clean -F cover.py --exclude-module matplotlib ^ -icon=icon.ico