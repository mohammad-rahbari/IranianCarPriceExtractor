import requests 
from bs4 import BeautifulSoup 
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont ,Image ,ImageDraw


def putText(image, text,location ,font_size,anchor,  title=False,color=(255,255,255)):
    if not title:
        fontFile = "files/IRANSANSWEB(FANUM)_LIGHT.TTF"
    else:
        fontFile = "files/KAGHAZ.OTF"

    font = ImageFont.truetype(fontFile, font_size)


    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)   

    draw = ImageDraw.Draw(image)
    draw.text(location, bidi_text, color, font=font,anchor=anchor)
    draw = ImageDraw.Draw(image)
    return image


def get_price(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
 
    print(url)
    try: 
        r = requests.get(url, allow_redirects=False, timeout=10, headers=headers)
    except requests.exceptions.Timeout as err: 
        print(err)
        print("__________________________")


    soup = BeautifulSoup(r.content, 'html5lib')  
    
    price_box = soup.find_all("div", attrs={"class":"legend"})[0]


    result = []
    temp={}

    title = soup.find("div",attrs={"class":"content"}).find("h1",attrs={"class":"title"}).text
    title = title.replace("  ","")
    title =title.split('''\n''')

    temp_text= ""
    for i in  price_box.find_all("div", attrs={"class":"detail"}):
        if "قیمت بازار" in str(i):
            try:
                temp["type"]=i.find("span",attrs={"class":"trim-fa"}).text
            except:
                temp["type"]= title[2]
            try:
                temp_text= i.find("span",attrs={"class":"class-name"}).text
            except:
                temp_text = " "

            temp_text= temp_text.replace("-","  ")
            temp_text= temp_text.replace("ایران خودرو"," ")
            temp_text= temp_text.replace("سایپا"," ")
            temp["detail"]= temp_text.replace("ترمر","ترمز")



            temp["price"]=i.find("span",attrs={"class":"price"}).text

            temp["price"]=temp["price"].replace(" ","")
            temp["price"]=temp["price"].replace('''\n''',"")

            temp["model-year"]=i.find("span",attrs={"class":"model-year"}).text
            temp["all"]=i.find("span",attrs={"class":"subtitle"}).text


            result.append(temp.copy())
        
    return result
    


    



cars_list=[
    {'url': 'https://bama.ir/price/peugeot_207', 'title': ' پژو 207 '},
    {'url': 'https://bama.ir/price/peugeot_206ir', 'title': ' پژو 206 '},
    {'url': 'https://bama.ir/price/respect_prime', 'title': ' ریسپکت پرایم'},
    {'url': 'https://bama.ir/price/haima_s5', 'title': ' هایما S5 '}, 
    {'url': 'https://bama.ir/price/peugeot_pars', 'title': ' پژو پارس'}, 
    {'url': 'https://bama.ir/price/jac_s5', 'title': 'دنا پلاس'}, 
    {'url': 'https://bama.ir/price/dena_plus', 'title': 'جک S5'}, 
    {'url': 'https://bama.ir/price/dignity_prestige', 'title': 'دیگنیتی پرستیژ'}, 
    {'url': 'https://bama.ir/price/respect_prime', 'title': ' ریسپکت پرایم'}, 
    {'url': 'https://bama.ir/price/saina_manuals', 'title': 'ساینا S'}, 
    {'url': 'https://bama.ir/price/samand_soren', 'title': 'سمند سورن'}, 
    {'url': 'https://bama.ir/price/shahin_g', 'title': 'شاهین G دنده ای'}, 
    {'url': 'https://bama.ir/price/fidelity_prime', 'title': 'فیدلیتی پرایم'}, 
    {'url': 'https://bama.ir/price/haima_8s', 'title': 'هایما 8S'}, 
    {'url': 'https://bama.ir/price/quick_manual', 'title': 'کوییک دنده ای'}]

for i in cars_list:
    print(i)
    lst = get_price(i["url"])
    image = Image.open("files/frame.jpg")

    image = putText(image,i['title'],(1005, 320),120, "rs", True, color=(10,10,10))
    origin_y = 590

    price_location = (160,550)
    detali_location = (510,550)
    model_location = (930,550)

    w, h = 0, 530
    shape = [(w, h), (w + 1080, h + 100)] 
    image1 = ImageDraw.Draw(image)  
    image1.rectangle(shape, fill ="#442c7a") 
    flag = True
    for i in range(len(lst)):
        y = 100 * i
        shape = [(w, h+y), (w + 1080, h + y + 100)] 
        if flag:
            image1.rectangle(shape, fill ="#442c7a") 
        flag = not flag

        image = putText(image,lst[i]["type"] +"  "+ lst[i]["model-year"] ,(920, origin_y + y),25, "ms", False)
        image = putText(image,lst[i]["detail"] ,(540, origin_y + y),25, "ms", False)
        image = putText(image,lst[i]["price"] ,(160, origin_y + y),25, "ms", False)

    image =image.save(f"{i['title']}.jpg")
    # image.show()

