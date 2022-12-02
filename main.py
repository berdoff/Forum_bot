import requests
from bs4 import BeautifulSoup
import json
import subprocess
import os
import vk_api
import imaplib
import time
from pymongo import MongoClient
import certifi
import datetime
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import tok,mongo,mail,passs,mail_pass,seraph_token

print(3)
cluster=MongoClient(mongo,tlsCAFile=certifi.where())
db=cluster["UsersData"]
collection=db["logs"]
print(4)
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.2.1501 Yowser/2.5 Safari/537.36'}
sess=requests.session()
xsrf=collection.find_one({"type":"token"})["session"]
print(xsrf)
sess.cookies.update({"laravel_session":xsrf,"XSRF-TOKEN":xsrf})


def chat_sender(text):
    id_be=1
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                vk_session.method('messages.send', {'chat_id': id_be, 'message': b, 'disable_mentions': 1, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'chat_id': id_be, 'message': b, 'disable_mentions': 1, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'chat_id': id_be, 'message': text, 'disable_mentions': 1, 'random_id': 0})


def send_to_user(idd,text):
    a=text.split("\n")
    b = ""
    if len(text) > 1200:
        for i in a:
            b += i + "\n"
            if len(b) > 1200:
                vk_session.method('messages.send', {'user_id': idd, 'message': b, 'disable_mentions': 1, 'random_id': 0})
                b = ""
        vk_session.method('messages.send', {'user_id': idd, 'message': b, 'disable_mentions': 1, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'user_id': idd, 'message': text, 'disable_mentions': 1, 'random_id': 0})

vk_session = vk_api.VkApi(token = tok)
longpoll = VkBotLongPoll(vk_session,212965717)
def get_xf(a):
    print(str(a.text).split("csrf=\"")[1].split("\"")[0])
    return str(a.text).split("csrf=\"")[1].split("\"")[0]

def login():
    print(1)
    time.sleep(5)
    session = requests.Session()
    session.headers.update(header)
    a = session.get("https://forum.arizona-rp.com/forums/338/", headers=header,timeout=5)
    #print(a.text)
    b = requests.post("https://seraphtech.site/api/v2/forum.getreact", data={"html": a.text})
    TOKEN = json.loads(b.text.split(">")[-1])["response"]["cookie"].strip()
    session.cookies.update({"R3ACTLAB-ARZ1":TOKEN})
    time.sleep(5)
    a=session.post("https://forum.arizona-rp.com/")
    xf_csrf=a.cookies["xf_csrf"]
    session.cookies.update({"R3ACTLAB-ARZ1":TOKEN,"xf_csrf":xf_csrf})
    time.sleep(3)
    b=session.post("https://forum.arizona-rp.com/login/login",data={"login":mail,"password":passs,"remember":"1","_xfRedirect":"https://forum.arizona-rp.com/","_xfToken":get_xf(a)})
    time.sleep(7)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(mail, mail_pass)
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
    time.sleep(5)
    b=session.get("https://forum.arizona-rp.com/forums/338/")
    cook={"R3ACTLAB-ARZ1":TOKEN,"xf_csrf":xf_csrf,"xf_tfa_trust":a.cookies["xf_tfa_trust"],"xf_user":a.cookies["xf_user"],"xf_session":a.cookies["xf_session"]}
    cook=json.dumps(cook)
    print(cook)
    if "Регистрация" not in b.text:
        print("+")
        collection.update_one({"type":"token"},{"$set":{"forum":cook}})
        jb()
        return "Cookies update"
    else:
        print("-")






def jb():
    global sess
    print(2)
    d=""
    cook=json.loads(collection.find_one({"type":"token"})["forum"])
    print(cook)
    a=requests.get("https://forum.arizona-rp.com/forums/338/",cookies=cook,headers=header,timeout=15)

    print(5)
    if  "Создать тему" in a.text:
        xf=get_xf(a)
        print("Успешно вошло\n\n\n\n")
        time.sleep(5)
        a=requests.get("https://forum.arizona-rp.com/forums/2136/",cookies=cook,headers=header)
        ne_zakrep=BeautifulSoup(a.text,"lxml").find("div",class_="structItemContainer-group js-threadList").find_all("div")
        for i in ne_zakrep:
            if i["class"][0].strip()=="structItem":
                time.sleep(1)
                title=i.find("div",class_="structItem-title").find_all("a")[-1].text
                thread_id=i.find("div",class_="structItem-title").find_all("a")[-1]["href"]
                thread_id=thread_id.replace("unread","")
                if len(i.find_all("i",class_="structItem-status structItem-status--locked"))==0:
                    try:
                        a=requests.get(f"https://forum.arizona-rp.com/{thread_id}",cookies=cook,headers=header)
                        nick=a.text.split("Ваш игровой ник")[1].split("*")[0].strip()
                        nick_adm=a.text.split("Игровой ник администратора:")[1].split("Причина наказания:")[0].strip()
                        xf=get_xf(a)
                        nick_adm="_".join(nick_adm.split())
                        print(nick_adm)
                        print(title)
                        logs=sess.get(f"https://arizonarp.logsparser.info/?server_number=21&type%5B%5D=ban&type%5B%5D=mute&type%5B%5D=jail&type%5B%5D=kick&type%5B%5D=warn&sort=desc&player={nick}")
                        logs=BeautifulSoup(logs.text,"lxml")
                        stroki=logs.find_all("tr")[1:5]
                        if "dell" in title.lower().split():
                                chat_sender("CLOSED: "+title+"\nhttps://forum.arizona-rp.com"+thread_id)
                                a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":"17","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","title":title},cookies=cook,headers=header)
                                time.sleep(4)
                                a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":"<p>Приветствую.</p><p>Извиняемся за возможную задержку  проверку жалобы.</p><p>Жалоба удалена.</p><p>Закрыто.</p>","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                                time.sleep(10)
                        else:
                            if not "взлом" in a.text.lower() or "продан" in i.text.lower() or "продан" in title.lower():

                                peredacha=""
                                print("+")
                                for i in stroki:
                                    if nick_adm.lower() in i.text.lower() or ((nick_adm[0]+"."+nick_adm.split("_")[1]).lower() in i.text.lower()) or nick_adm.replace("_","").lower() in i.text.lower():
                                        nakazanie=" ".join(i.text.split("I:")[0].strip().split())
                                        if "(offline)" in nakazanie:
                                            nakazanie=nakazanie.replace("(offline)","")
                                        print(nakazanie+"\n")
                                        time.sleep(4)
                                        if "/ " in nakazanie or ("//") in nakazanie:
                                            nakazanie=nakazanie.replace("//","/")
                                            peredacha=nakazanie.split("/")[-1].strip()
                                        elif "|" in nakazanie:
                                            nakazanie=nakazanie.replace("||","|")
                                            peredacha=nakazanie.split("|")[-1].strip()
                                        elif " x " in nakazanie:
                                            peredacha=nakazanie.split()[-1].strip()
                                        elif " х " in nakazanie:
                                            peredacha=nakazanie.split()[-1].strip()
                                        elif "&" in nakazanie:
                                            peredacha=nakazanie.split("&")[-1].strip()
                                        else:
                                            peredacha=nakazanie.split()[3].strip()
                                        print(peredacha)
                                        g=json.loads(requests.get(f"https://seraphtech.site/api/v2/forum.getAdmins?nick={peredacha}&token={seraph_token}&server=21").text)    
                                        if len(g["response"])==0:
                                            peredacha=nick_adm
                                            g=json.loads(requests.get(f"https://seraphtech.site/api/v2/forum.getAdmins?nick={peredacha}&token={seraph_token}&server=21").text)    
                                        print(g["response"])
                                        p_id=g["response"][0]["vk"]
                                        if int(g["response"][0]["lvl"])<=2 or peredacha.lower()=="queenbot":
                                            prefix_id=0
                                            if peredacha.lower()=="queenbot":
                                                prefix_id=15
                                                p_id="178391887"
                                        else:
                                            prefix_id=15
                                        print(prefix_id)
                                        
                                        chat_sender(f"Жалоба передана @id"+str(g["response"][0]["vk"])+f"({peredacha})\nСсылка: https://forum.arizona-rp.com{thread_id}\nЛоги: {nakazanie}")
                                        send_to_user(p_id,f"Привет, ответь на жалобу)\nhttps://forum.arizona-rp.com{thread_id}\n\n Жалоба передана ботом\nЕсли это ошибка, отправь жалобу нужному администратору: https://vk.com/topic-212965717_48817319\n")
                                        a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":prefix_id,"discussion_open":"1","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","sticky":"1","title":title},cookies=cook,headers=header) 
                                        time.sleep(4)
                                        a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":f"""<p>Приветствую.<br>Извиняемся за возможную задержку в проверке жалобы.<br>Ваша жалоба передана администратору, ожидайте его ответа в течение 24 часов.</p><p>[GROUPS=75]</p><p>{nakazanie}</p><p>[/GROUPS]</p>""","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                                        
                                        break
                                

                                if peredacha=="":
                                    peredacha=nick_adm
                                    g=json.loads(requests.get(f"https://seraphtech.site/api/v2/forum.getAdmins?nick={peredacha}&token={seraph_token}&server=21").text)    
                                    if int(g["response"][0]["lvl"])<=2:
                                        prefix_id=0
                                    else:
                                        prefix_id=15
                                    chat_sender(f"Жалоба передана @id"+str(g["response"][0]["vk"])+f"({peredacha})\nСсылка: https://forum.arizona-rp.com{thread_id}\nСтрока в логах не найдена")
                                    send_to_user(g["response"][0]["vk"],f"Привет, ответь на жалобу)\nhttps://forum.arizona-rp.com{thread_id}\n\n Жалоба передана ботом\nЕсли это ошибка, отправь жалобу нужному администратору: https://vk.com/topic-212965717_48817319\n")
                                    a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":prefix_id,"discussion_open":"1","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","sticky":"1","title":title},cookies=cook,headers=header) 
                                    time.sleep(4)
                                    a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":f"""<p>Приветствую.<br>Извиняемся за возможную задержку в проверке жалобы.<br>Ваша жалоба передана администратору, ожидайте его ответа в течение 24 часов.</p><p>[GROUPS=75]</p><p>Строка не найдена</p><p>[/GROUPS]</p>""","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                                        

                            else:
                                chat_sender("CLOSED: "+title+"\nhttps://forum.arizona-rp.com"+thread_id)
                                a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":"17","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","title":title},cookies=cook,headers=header)
                                time.sleep(4)
                                a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":"<p>[CENTER][SIZE=3][B]Здравствуйте, [COLOR=rgb(84, 172, 210)]уважаемый игрок.[/COLOR][/B][/SIZE]</p><p>[B][SIZE=3]В случае если вас [COLOR=rgb(84, 172, 210)]взломали[/COLOR], вы [COLOR=rgb(84, 172, 210)]забыли пароль[/COLOR] или вас [COLOR=rgb(84, 172, 210)]забанили за взломан/до выяснений[/COLOR] [URL='https://forum.arizona-rp.com/threads/4420559/']следуйте инструкции по взлому[/URL]</p><p>Спасибо за обращение, закрыто.[/SIZE][/B][/CENTER]</p>","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                                time.sleep(10)



                    except:
                        pass
                    time.sleep(4)



        a=requests.get("https://forum.arizona-rp.com/forums/2136/",cookies=cook,headers=header)
        zakrep=BeautifulSoup(a.text,"lxml").find("div",class_="structItemContainer-group structItemContainer-group--sticky").find_all("div")
        xf=get_xf(a)
        jb_zakrep={}
        for i in zakrep:
            if i["class"][0].strip()=="structItem":
                author=i["data-author"]
                title=i.find("div",class_="structItem-title").find_all("a")[-1].text
                thread_id=i.find("div",class_="structItem-title").find_all("a")[-1]["href"]
                thread_id=thread_id.replace("unread","")
                jb_zakrep[author]={"title":title,"thread_id":thread_id}
                if "dell" in title.lower().split():
                    chat_sender("CLOSED: "+title+"\nhttps://forum.arizona-rp.com"+thread_id)
                    a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":"17","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","title":title},cookies=cook,headers=header)
                    time.sleep(4)
                    a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":"<p>Приветствую.</p><p>Извиняемся за возможную задержку  проверку жалобы.</p><p>Жалоба удалена.</p><p>Закрыто.</p>","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                    time.sleep(10)
        



        ne_zakrep=BeautifulSoup(a.text,"lxml").find("div",class_="structItemContainer-group js-threadList").find_all("div")
        for i in ne_zakrep:
            if i["class"][0].strip()=="structItem":
                time.sleep(1)
                author=i["data-author"]
                #print(author)
                title=i.find("div",class_="structItem-title").find_all("a")[-1].text
                thread_id=i.find("div",class_="structItem-title").find_all("a")[-1]["href"]
                thread_id=thread_id.replace("unread","")
                if author in jb_zakrep:
                    #print(author)
                    #print(title)
                    if title==jb_zakrep[author]["title"]:
                        if len(i.find_all("i",class_="structItem-status structItem-status--locked"))==0:
                            #print(title)
                            main_thread_id=jb_zakrep[author]["thread_id"]
                            #print(thread_id)
                            a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":"17","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","title":title},cookies=cook,headers=header)
                            time.sleep(4)
                            a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":f"""<div data-xf-p="1">Здравствуйте, уважаемый игрок.</div><div data-xf-p="1">Извиняемся за возможную задержку в проверке жалобы.</div><div data-xf-p="1">Ожидайте ответа в прошлой жалобе [URL]https://forum.arizona-rp.com{main_thread_id}[/URL]</div><div data-xf-p="1">Закрыто</div><div data-xf-p="1"><br></div><div data-xf-p="1">[SIZE=2]ps. ответ дан ботом, если это другая жалоба, пересоздайте жалобу с другим заголовком[/SIZE]</div>""","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                            time.sleep(10)
        







        a=BeautifulSoup(a.text,"lxml").find("div",class_="structItemContainer-group js-threadList").find_all("div",class_="structItem-cell structItem-cell--main")
        for i in a:
            thread=i.text
            if thread.split()[0]!="Закрыта":
                if "взлом" in thread.split("Изменить")[0].lower().strip() and (not "взломщик" in thread.split("Изменить")[0].lower().strip()):
                    time.sleep(5)
                    thread_id=i.find_all("a")[-1]["href"]
                    thread_title=i.find("div",class_="structItem-title").find_all("a")[-1].text
                    #print(thread_id)
                    chat_sender("CLOSED: "+thread_title+"\nhttps://forum.arizona-rp.com"+thread_id)

                    a=requests.post(f"https://forum.arizona-rp.com{thread_id}edit",data={"_xfRequestUri":thread_id,"_xfWithData":"1","_xfToken":xf,"_xfResponseType":"json","prefix_id":"17","_xfSet[discussion_open]":"1","_xfSet[sticky]":"1","title":thread_title},cookies=cook,headers=header)
                    time.sleep(4)
                    a=requests.post(f"https://forum.arizona-rp.com{thread_id}add-reply",data={"message_html":"<p>[CENTER][SIZE=3][B]Здравствуйте, [COLOR=rgb(84, 172, 210)]уважаемый игрок.[/COLOR][/B][/SIZE]</p><p>[B][SIZE=3]В случае если вас [COLOR=rgb(84, 172, 210)]взломали[/COLOR], вы [COLOR=rgb(84, 172, 210)]забыли пароль[/COLOR] или вас [COLOR=rgb(84, 172, 210)]забанили за взломан/до выяснений[/COLOR] [URL='https://forum.arizona-rp.com/threads/4420559/']следуйте инструкции по взлому[/URL]</p><p>Спасибо за обращение, закрыто.[/SIZE][/B][/CENTER]</p>","_xfResponseType":"json","_xfToken":xf},cookies=cook,headers=header)
                    time.sleep(10)
            


        return "Все жалобы на взлом закрыты"

    else:
        print(login())



print(jb())



