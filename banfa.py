import requests
from bs4 import BeautifulSoup
import json
import subprocess
import os
import imaplib
import time
from pymongo import MongoClient
import certifi
import datetime
from config import mongo


cluster=MongoClient("mongodb+srv://berdoff:anna280980@cluster0.kd286.mongodb.net/UsersData?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=cluster["UsersData"]
collection=db["logs"]

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
 #dat={"_xfRequestUri:":"/threads/3560145/","_xfWithData":"1","_xfToken":"1631461719,6a31bad264ba15f5210e9580e82cdf20","_xfResponseType":"json"}
 #cookie={"_ga":"GA1.2.797599968.1604574322","_ym_d":"1614071138","_ym_uid":"1614071138850848874","xf_tfa_trust":"R4C3qVx4tQ9XrriJ4LQeRZmTglzaixWY","xf_user":"393849%2CQ5ZDNOM25v5MgXDo2k8sep56jZzdVfQtd49MTTnY","xf_emoji_usage":"%3Alaugh%3A%2C%3Aban%3A%2C%3Alove%3A","R3ACTLB":"b628f39867d1950a74ba86e09773c3a3","xf_csrf":"cvfB6mgFsN4D5ssa","xf_session":"xPiuJg8bKsFG_MOD7cuzWyM2-HxpKSr6"}


def get_xf(a):
    return str(a.text).split("csrf=\"")[1].split("\"")[0]

def login():
    session = requests.Session()
    session.headers.update(header)
    a = session.get("https://forum.arizona-rp.com", headers=header,timeout=5)
    b = requests.post("https://seraphtech.site/api/v2/forum.getreact", data={"html": a.text})
    TOKEN = json.loads(b.text.split(">")[-1])["response"]["cookie"].strip()
    session.cookies.update({"R3ACTLAB-ARZ1":TOKEN})
    a=session.post("https://forum.arizona-rp.com/")
    xf_csrf=a.cookies["xf_csrf"]
    session.cookies.update({"R3ACTLAB-ARZ1":TOKEN,"xf_csrf":xf_csrf})
    b=session.post("https://forum.arizona-rp.com/login/login",data={"login":"hrhhhdki@gmail.com","password":"anna280980","remember":"1","_xfRedirect":"https://forum.arizona-rp.com/","_xfToken":get_xf(a)})




    time.sleep(7)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('hrhhhdki@gmail.com', 'gqpizosplmcnftst')
    mail.select("inbox")
    result, data = mail.search(None, "ALL")
    ids = data[0] # Получаем сроку номеров писем
    id_list = ids.split() # Разделяем ID писем
    latest_email_id = id_list[-1] # Берем последний ID
    result, data = mail.fetch(latest_email_id, "(RFC822)") # Получаем тело письма (RFC822) для данного ID
    raw_email = data[0][1] # Тело письма в необработанном виде
    # # включает в себя заголовки и альтернативные полезные нагрузки
    CODE=str(raw_email).split("******")[1].strip()
    CODE=CODE.replace("=","")
    CODE=CODE.replace("r","")
    CODE=CODE.replace("n","")
    CODE=CODE.replace("\\","")
    print(CODE)
    a=session.post("https://forum.arizona-rp.com/login/two-step",data={"code":CODE,"trust":"1","confirm":"1","provider":"email","remember":"1","_xfRedirect":"https://forum.arizona-rp.com/","_xfToken": get_xf(b),"_xfResponseType":"json"})
    session.cookies.update({"R3ACTLAB-ARZ1":TOKEN,"xf_csrf":xf_csrf,"xf_tfa_trust":a.cookies["xf_tfa_trust"],"xf_user":a.cookies["xf_user"],"xf_session":a.cookies["xf_session"]})
    b=session.get("https://forum.arizona-rp.com/")
    cook={"R3ACTLAB-ARZ1":TOKEN,"xf_csrf":xf_csrf,"xf_tfa_trust":a.cookies["xf_tfa_trust"],"xf_user":a.cookies["xf_user"],"xf_session":a.cookies["xf_session"]}
    cook=json.dumps(cook)
    print(cook)
    if "Администрация проекта" in b.text:
        print("+")
        collection.update_one({"type":"token"},{"$set":{"forum":cook}})
        return "Куки обновлены"
    else:
        print("-")


cook=json.loads(collection.find_one({"type":"token"})["forum"])
print(cook)
a=requests.get("https://forum.arizona-rp.com/forums/338/",cookies=cook,headers=header)
if "Регистрация" not in a.text and "Phoenix" in a.text:
    print("Успешно вошло\n\n\n\n")
    while True:
        amazing=[]
        date=datetime.datetime.now()
        a=requests.get("https://forum.arizona-rp.com/",cookies=cook,headers=header)
        xf=get_xf(a)
        time.sleep(5)
        b=requests.get(f"https://forum.arizona-rp.com/members/ip-users?ip=193.169.96.44&_xfRequestUri=%2Fforums%2F2136%2F&_xfWithData=1&_xfToken={xf}&_xfResponseType=json",cookies=cook,headers=header)
        a=str(json.loads(b.text)["html"]["content"])
        a=BeautifulSoup(a,"lxml")
        g=[]
        for i in a.find_all("span",class_="username"):
            if len(i.find_all("span",class_="username--banned"))!=0:
                pass
                g.append(i.text)
            else:
                amazing.append(i["data-user-id"])
        """
        if len(amazing)!=0:
            for i in amazing:
                a=requests.post(f"https://forum.arizona-rp.com/members/{i}/warn",data={"warning_definition_id":"0","custom_title":"Больше 3 форумников","points_enable":"1","points":"666","notes":"","filled_warning_definition_id":"0","_xfToken":xf,"_xfResponseType":"json"},cookies=cook,headers=header)
                status=json.loads(a.text)["status"]
                if status=="ok":
                    print(f"{date.hour}:{date.minute}:{date.second} Годунову снесен новый форумник: https://forum.arizona-rp.com/members/{i}/")
        else:
            print(f"{date.hour}:{date.minute}:{date.second} Годунову устал и не регнул новый форумник")
        time.sleep(595)
        """
        k=0
        print(g)
        for i in range(1,20):
            a=requests.get(f"https://forum.arizona-rp.com/forums/1592/page-{i}",cookies=cook,headers=header).text
            a=BeautifulSoup(a,"lxml")
            a=a.find_all("a")
            for i1 in g:
                if f"/members/{i1}/" in a:
                    k+=1
            print(f"Загружена страница {i}")
            time.sleep(5)
        print(k,k/2)
                    
else:
    print(login())






