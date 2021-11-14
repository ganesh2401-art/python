from selenium import webdriver
import urllib.request
import os
import time
import zipfile
import yagmail
from flask import Flask, render_template, request

#Divided the URL as prefix and postfix
Url_prefix = "https://www.google.com.sg/search?q="
Url_postfix = "&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjyoMaU7ofyAhVNeH0KHfDYAfcQ_AUoAXoECAEQAw&biw=1366&bih=625"
#To_download = input("Enter the Keyword of image to be Downloaded: ")


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("form.html")

@app.route("/call",methods=["GET","POST"])
def call():

    A_Keyword = request.form.get("Keyword")
    A_Count = int(request.form.get("count"))
    A_Mail = request.form.get("mail")
    A_Type = request.form.get("type")
    print(A_Keyword)
    print(A_Count)
    print(A_Mail)
    print(A_Type)
    To_download=A_Keyword
    #To save the Downloaded Images inside the Folder
    save_folder = 'Downloaded-Images-'+To_download
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    #imagedownload()
    #function to take KEY-WORD,Which is to be Downloaded
    #To_download = input("Enter the Keyword of image to be Downloaded: ")
    Num_images = A_Count
    Format_Type = A_Type
    Sender_Email = A_Mail
    search_url = Url_prefix+To_download+Url_postfix
    print(search_url)
    path = r'D:/chromedriver/chromedriver.exe'
    driver = webdriver.Chrome(path)
    driver.get(search_url)
    value = 0
    for i in range(3):
        driver.execute_script("scrollBy("+ str(value) +",+1000);")
        value += 1000
        time.sleep(1)
    elem1 = driver.find_element_by_id('islmp')
    sub = elem1.find_elements_by_tag_name('img')
    #To Download the Images For the Given Count
    count=0
    for j,i in enumerate(sub):
        if j < Num_images:
            src = i.get_attribute('src')                         
            try:
                if src != None:
                    src  = str(src)
                    print(src)
                    urllib.request.urlretrieve(src, os.path.join(save_folder, To_download+str(count)+Format_Type))
                    count = count+1
                else:
                    raise TypeError
            except Exception as e:              
                print(f'fail with error {e}')
#To create Zip file of the used directory
    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))
    zipf = zipfile.ZipFile(save_folder+'.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('./'+save_folder, zipf)
    zipf.close()
    try:
#initializing the server connection
        yag = yagmail.SMTP(user='Sender Email', password='Password')
#sending the email
        yag.send(to= Sender_Email, subject='UPDATE@IMAGE-DOWNLOADING', contents='PROCESS COMPLETED!please click on the attach URL to download the file')
        print("Email sent successfully")
    except:
        print("Error, email was not sent")
    driver.close()
    return render_template("form.html")
