## -*- coding: utf-8 -*-


import sys, re,string
from telnetlib import Telnet
import time
import os
import random
import subprocess

def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)

class Mozrepl(object):
    def __init__(self, ip="127.0.0.1", port=4242):
        self.ip = ip
        self.port = port
        self.prompt = b"repl>"

    def __enter__(self):
        self.t = Telnet(self.ip, self.port)
        intro = self.t.read_until(self.prompt, 1)
        if not intro.endswith(self.prompt):
            self.prompt = re.search(br"repl\d+>", intro).group(0)
            print("Waited due to nonstandard prompt:", self.prompt.decode())
        return self

    def __exit__(self, type, value, traceback):
        self.t.close()
        del self.t

    def js(self, command):
        self.t.write(command.encode() + b"\n")
        return self.t.read_until(self.prompt)[2:-7].decode()


def Translate(mozrepl):
    if mozrepl.js("document.getElementsByClassName('ytp-subtitles-button ytp-button')[0].getAttribute('aria-pressed')") == 'false':
        mozrepl.js("document.getElementsByClassName('ytp-subtitles-button ytp-button')[0].click()")
        print("Включены субтитры")
    else:
        print("Субтитры уже включены")
    
    # настройки class=ytp-button ytp-settings-button       atr  aria-expanded="true"-значит включено  если атрибута нет то настроки выключены
    #print(mozrepl.js("document.getElementsByClassName('ytp-button ytp-settings-button')[0].hasAttribute('aria-expanded')"))
    if mozrepl.js("document.getElementsByClassName('ytp-button ytp-settings-button')[0].hasAttribute('aria-expanded')") =="als":
        mozrepl.js("document.getElementsByClassName('ytp-button ytp-settings-button')[0].click()")
    #один из пунктов меню    ytp-menuitem
    #Перевод(3)
    
    #print(mozrepl.js("document.getElementsByClassName('ytp-menuitem')[3].firstChild.lastChild.textContent"))
    notTranslate=False

    for i in range(0,15):
            #print(mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].textContent"))
            #print(mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].firstChild.lastChild.textContent") )
            if "Субтитры" in mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].firstChild.lastChild.textContent"):
                #print(mozrepl.js("document.getElementsByClassName('ytp-menuitem')[3].lastChild.textContent"))                if " >> Русский" in 
                if " >> Русский" in mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].lastChild.textContent"):
                    notTranslate=True 
                    mozrepl.js("document.getElementsByClassName('ytp-button ytp-settings-button')[0].click()") 
                    break;
                else:
                    mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].click()") 
                    print("Настройки-->Субтитры")
                    break;

    if notTranslate==False:
        time.sleep(0.5)    
        for i in range(0,15):
            #print(mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].textContent"))
            if mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].textContent") == "Перевести":
                mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].click()")
                print("Настройки-->Субтитры->Перевести")
                break;

        time.sleep(0.5)
        for i in range(0,150):
            #print(mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].textContent"))
            if mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].textContent") == "Русский":
                mozrepl.js("document.getElementsByClassName('ytp-panel-menu')[0].children["+i.__str__()+"].click()")
                print("Настройки-->Субтитры->Перевести-->Русский")
                break;
        time.sleep(3)
        mozrepl.js("document.getElementsByClassName('ytp-button ytp-settings-button')[0].click()")




with Mozrepl() as mozrepl:    

    
    mozrepl.js("repl.enter(content)")

    for i in range(1000):
        #print(mozrepl.js("document.readyState"))
        if mozrepl.js("document.readyState") == "complete":
            print ("good")
            time.sleep(0.5) 
            break
    

   
    Translate(mozrepl)

    #captions-text  Сами субтитры
    import os
    lastText=''

    lastTab=mozrepl.js("document.title")

    delay=3000

    subprocess.Popen("rm aa & rm bb", shell=True)
    # if  mozrepl.js("document.getElementById('action-panel-transcript').style")=="display: none;": 
    mozrepl.js("document.getElementById('action-panel-overflow-button').click()")
    mozrepl.js("document.getElementsByClassName('yt-ui-menu-item has-icon yt-uix-menu-close-on-select action-panel-trigger action-panel-trigger-transcript')[0].click()")        
    time.sleep(2)

    import os.path
    import subprocess

    
    text=mozrepl.js("document.getElementsByClassName('caption-line caption-line-highlight')[0].lastChild.textContent")
    text2=text.replace("...","").replace(">"," больше").replace("<"," меньше")
    # Обычный режим
    # print(text[2:-2])           
    # command = "echo '"+text2[2:-2]+"' | festival --tts --language russian ; sudo mv -f /tmp/aa /tmp/cc"             
    # subprocess.run(command, shell=True)

    # ЯндексГолос  -------------------------------------------
    command='curl "https://tts.voicetech.yandex.net/generate?&speed=1.5&format=wav&lang=ru-RU&speaker=omazh&emotion=evil&key=bc032ff5-11f0-47be-a637-78233099c1c1" -G --data-urlencode "text='+text2+'" > cc.wav'
    subprocess.run(command, shell=True)

    import re
    reg = re.compile('[^a-zA-Zа-яА-Я0-9_]')

    print("---------------------------------------------")
    

    while True:
        #text=mozrepl.js("document.getElementsByClassName('captions-text')[0].firstChild.textContent")
        text=mozrepl.js("document.getElementsByClassName('caption-line caption-line-highlight')[0].lastChild.textContent")      
        #print("textNext: " + textNext)

        if text != lastText and "TypeError:" not in text:
            
            # if lastTab != mozrepl.js("document.title"):
            #     Translate(mozrepl)
            # lastTab=mozrepl.js("document.title")



            #print("stop") 
            #mozrepl.js("document.getElementsByClassName('ytp-play-button ytp-button')[0].click()")

            #mozrepl.js("function func() {document.getElementsByClassName('ytp-play-button ytp-button')[0].click()} ; setTimeout(func, "+delay.__str__()+");") 
            

            #output=subprocess.check_output("cp aa bb", shell=True)

            

            
            
            ## ОбычныйРежим ++++++++++++++++++++++++++++++++++++++++
            # subprocess.run("killall aplay ; sudo mv -f /tmp/bb /tmp/cc", shell=True) 

            # ЯндексГолос  -------------------------------------------
            subprocess.run("killall aplay ; sudo mv -f bb.wav cc.wav", shell=True) 


            # if os.path.exists("cc"):
            
                # time.sleep(0.5)  
            print(text)  
            ## ОбычныйРежим ++++++++++++++++++++++++++++++++++++++++          
            # subprocess.Popen("aplay -q -f S16 -r24000 /tmp/cc", shell=True)
            # ЯндексГолос  -------------------------------------------
            subprocess.Popen("aplay -q -f S16 -r24000 cc.wav", shell=True)
                    #print("nowText")
                    

            textNext=mozrepl.js("document.getElementsByClassName('caption-line caption-line-highlight')[0].nextSibling.lastChild.textContent")

            ## ОбычныйРежим ++++++++++++++++++++++++++++++++++++++++
            # # subprocess.run("", shell=True) « »
            # text2=reg.sub('', textNext).replace("enter","энтэр").replace("shift","шифт").replace("ctrl","контрол")
            # #text2=textNext.swapcase().replace("...","").replace(">"," больше").replace("<"," меньше").replace("&"," имперсанд").replace(",","").replace("enter","энтэр").replace("shift","шифт").replace("ctrl","контрол")
            # command = "echo '"+text2+"' | festival --tts --language russian ; sudo mv -f /tmp/aa /tmp/bb" 
            

            # женские голоса: jane, oksana, alyss и omazh;
            # мужские голоса: zahar и ermil.

            # ЯндексГолос  -------------------------------------------
            speaker='omazh'
            key='bc032ff5-11f0-47be-a637-78233099c1c1'
            command='curl "https://tts.voicetech.yandex.net/generate?&speed=1.5&format=wav&lang=ru-RU&speaker='+speaker+'&emotion=good&key='+key+'" -G --data-urlencode "text='+textNext+'" > bb.wav'
            subprocess.run(command, shell=True)    



            # if not os.path.exists("bb"):
            #     print("файл bb не найден")
                
            #     subprocess.run("mv aa bb ; mv bb cc", shell=True)
            #     # subprocess.run("rm cc ; rm bb", shell=True)


            

            lastText=text
            
            # if len(text)<20:
            #     time.sleep(1)            
            # else:
            #      time.sleep(0.5)
            

            #print(output)
            # if "LTS_Ruleset" in output.__str__():
            #     f = open('text.txt', 'a')
            #     f.write(command + '\n')
            #     f.close()

            #print("play") 
            #mozrepl.js("document.getElementsByClassName('ytp-play-button ytp-button')[0].click()")                       
            
            #ytp-play-button ytp-button    -- play

            
        time.sleep(0.1)


