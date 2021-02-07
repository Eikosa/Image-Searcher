import imagesearch as i
import pyautogui
import time
from PIL import Image

def search(image,istekler={}):
    print(" ╔═══*.·:·.☽✧    ✦    ✧☾.·:·.*═══╗ \n")
    settings={
        "hassasiyet":0.7,

        "hangisiVar":False,

        "tersi":False,
        #"eminsen":False, #emin değilsen -1,-1
        
        "sinirliSayidaAra":1,
        "bulanaKadarAra":False,
        "bulanaKadarHiz":0.1,
        
        "hepsiVarsa":False,
        "birisiVarsa":True,

        "solTikla":False,
        "sagTikla":False,
        "ortaTikla":False,
        "hareketEttir":False,
        "hareketHizi":0,
        
        "scrollYap":False,
        "scrollMiktari":100,

        "ortaNokta":True,
        
        "alanAra":False, #False ise tam ekran
        "x1":-1,
        "x2":-1,
        "y1":-1,
        "y2":-1,

        "info":False,
    }
    for istek in istekler:
        settings[istek]=istekler[istek]
    #print(settings)

    # ayar kontrol
    if settings["alanAra"]:
        if settings["x1"]<0 or settings["x2"]<0 or settings["y1"]<0 or settings["y2"]<0:
            raise Exception("Koordinatlar doğru değil!",settings["x1"],settings["x2"],settings["y1"],settings["y2"])
        if settings["x1"]-settings["x2"]==0 or settings["y1"]-settings["y2"]==0:
            raise Exception("x1-x2=0 veya y1-y2=0 olamaz",settings["x1"],settings["x2"],settings["y1"],settings["y2"])
    x1 = settings["x1"]
    x2 = settings["x2"]
    y1 = settings["y1"]
    y2 = settings["y2"]
    birisiVarsa = settings["birisiVarsa"]
    bulanaKadar = settings["bulanaKadarAra"]
    alanAra = settings["alanAra"]
    timesample = settings["bulanaKadarHiz"]
    precision = settings["hassasiyet"]
    
    solTikla = settings["solTikla"]
    sagTikla = settings["sagTikla"]
    ortaTikla = settings["ortaTikla"]    
    hareketEttir = settings["hareketEttir"]
    hareketHizi = settings["hareketHizi"]
    scrollYap = settings["scrollYap"]
    scrollMiktari = settings["scrollMiktari"]

    hepsiVarsa=settings["hepsiVarsa"]
    tersi=settings["tersi"]

    if tersi==True and (solTikla or sagTikla or ortaTikla or hareketEttir or scrollYap):
        raise Exception("Tersi özelliği ile her şey kullanılamaz,",solTikla, sagTikla, ortaTikla, hareketEttir, scrollYap)



    def eylemYap(x,y):
        if solTikla:
            pyautogui.click(x, y, button='left', duration=hareketHizi)
            
        if sagTikla:
            pyautogui.click(x, y, button='right', duration=hareketHizi)

        if ortaTikla:
            pyautogui.click(x, y, button='middle', duration=hareketHizi)

        if hareketEttir:
            pyautogui.moveTo(x, y, hareketHizi)
            
        if scrollYap:
            pyautogui.scroll(scrollMiktari, x, y)



    def bul(image):
        if alanAra==True and bulanaKadar==True:
            #x,y = i.imagesearcharea_loop(image,x1,y1,x2,y2, timesample, precision)
            x,y = i.imagesearcharea(image,x1,y1,x2,y2, precision)
        elif alanAra==True and bulanaKadar==False:
            x,y = i.imagesearcharea(image,x1,y1,x2,y2, precision)            
        elif alanAra==False and bulanaKadar==True:
            #x,y = i.imagesearch_loop(image, timesample, precision)
            x,y = i.imagesearch(image, precision)
        elif alanAra==False and bulanaKadar==False:
            x,y = i.imagesearch(image, precision)
        print(image,x,y)


        if bulanaKadar==False:
            #eylemYap(x,y)
            return x,y
        elif bulanaKadar==True and x!=-1 and y!=-1:
            #eylemYap(x,y)
            return x,y

    def emirVer(adamlar):
        if "dict" in str(type(adamlar)):
            for adam in adamlar.values():
                if adam[0]!=-1 and adam[1]!=-1 and adam!=None:
                    eylemYap(adam[0],adam[1])
        elif "list" in str(type(adamlar)) or "tuple" in str(type(adamlar)):
            adamlar=list(adamlar)
            if len(adamlar)==2:
                eylemYap(adamlar[0],adamlar[1])
        #elif "str" in str(type(adamlar)):
        #    eylemYap(adamlar)


    def urlToImg(url):
        import urllib.request
        #print('Beginning file download with urllib2...')
        url = url
        urllib.request.urlretrieve(url, 'url.jpg')

    def sonAdim(dondurulecek,cevap=""):
        if cevap!="":
            emirVer(cevap)
        return dondurulecek
        

    
    
    say=0
    cevapDict={}
    if "list" in str(type(image)):
        for rsm in image:
            cevapDict[rsm]=(-1,-1)
    
    while bulanaKadar or say<settings["sinirliSayidaAra"]:
        print(cevapDict)
        if "list" in str(type(image)):
            for img in image:
                if "http" in img:
                    urlToImg(img)
                    url=img
                    img="url.jpg"
                    cevap=bul(img)
                    cevapDict[url]=cevap
                else:
                    cevap=bul(img)
                    cevapDict[img]=cevap

                #im = cv2.imread(img)
                #h, w, c = im.shape
                if not hepsiVarsa:
                    if (not tersi and birisiVarsa and (cevap!=(-1,-1) and  cevap!=None)):
                        print("wdwdw")
                        return sonAdim((img,cevap),cevap)
                    elif (tersi and ((cevap==(-1,-1) or cevap==None))):
                        print("asdasd")                    
                        return sonAdim((img,cevap))
                    

            if hepsiVarsa:
                if tersi and list(cevapDict.values()).count((-1,-1))==len(list(cevapDict.values())): #tersi
                    print("kkk")
                    #if not tersi:
                    #    emirVer(cevapDict)
                    return sonAdim(cevapDict)
                elif tersi and list(cevapDict.values()).count(None)==len(list(cevapDict.values())):
                    print("wooooww")
                    return sonAdim(cevapDict)                      
                elif (not tersi and not (-1,-1) in list(cevapDict.values())) and not None in list(cevapDict.values()):#normal
                    print("hahi")
                    return sonAdim(cevapDict)                    
                elif not bulanaKadar:
                    print("zazaza")
                    return sonAdim(cevapDict)
            
        elif "str" in str(type(image)):
            #print(image)
            if "http" in image:
                urlToImg(image)
                image="url.jpg"

            #im = cv2.imread(image)
            #h, w, c = im.shape
            
            cor = bul(image)
            
            if (not bulanaKadar):
                print("faaaaa")
                return sonAdim({image:cor},cor)
            elif (not tersi and bulanaKadar and ((cor!=(-1,-1) and cor!=None))):
                print("ggffdgaaaaa")
                return sonAdim({image:cor},cor)
            elif (tersi and (cor==(-1,-1) or cor==None)):
                print("asds4a")
                return sonAdim({image:cor},cor)

        
        if bulanaKadar:
            time.sleep(timesample)
        say+=1


        

    # olmadığını söyle
    if "list" in str(type(image)):
        cevapDict={}
        for rsm in image:
            cevapDict[rsm]=(-1,-1)
        print("looool")
        return cevapDict
    elif "str" in str(type(image)):
        print("lol")
        return {image:(-1,-1)}
    print("\n ╚═══*.·:·.☽✧    ✦    ✧☾.·:·.*═══╝ ")
