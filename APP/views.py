from unittest import result
from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

# BASE
def base(request):
    return render(request, 'base.html')

# AJAX/API SCRAPPER
def scrapp(request):
    option = request.GET.get('o') 
    url = request.GET.get('u')
    
    # condition if there is an empty input 
    if option != 'o' and url != '':
        result = {'code':0, 
                  'status': 'OK', 
                  'result': scrapper_action(url, option)} # result from scrapping data
        
    elif option == 'o' and url != '':
        result = {'code':1, 
                  'status': 'ERROR', 
                  'result': 'Choose Your Option'}
        
    elif option == 'o' and url != '':
        result = {'code':1, 
                  'status': 'ERROR', 
                  'result': 'URL cant be empty'}
    
    else:
        result = {'code':1, 
                  'status': 'ERROR', 
                  'result': 'You must choose your option and fill URL'}
        
    return JsonResponse(result)

# library for scrapping data
import requests
from bs4 import BeautifulSoup
import json

# SCRAPPER HELPER
def scrapper_action(u, o):
    if o == 'titip':
        try:
            payloa = {"url":u,"version":"V2"} # key to scrapping/payload
            
            res = requests.post('https://scraper.titipbeliin.com/api/scrap', json=payloa) # get from api scrapping
            
            sou = BeautifulSoup(res.content,'html.parser') # get content using bs4

            json_ = json.loads(sou.text.strip()) # build json from content
            
            # result
            code = 0
            source = 'titipbeliin.com'
            title = json_['NAME']
            image = json_['IMAGE_URLS']
            price = json_['PRICE']
            
        except:
            code = 1
            teks = 'Scrapping Failed from titipbeliin.com, please use another option'
        
    if o == 'amazon':
        # try:
        url = u
        HEADERS = ({'authority': 'www.amazon.com',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'dnt': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',})

        pag = requests.get(url, headers = HEADERS)

        sou = BeautifulSoup(pag.content,'html.parser')

        # get title
        job_title = sou.find_all('span', id='productTitle') # find product title in HTML
        title = job_title[0].text.strip() # retrieve title from HTML

        # get image
        job_elem = sou.find_all('div', id='altImages') # find image element in HTML
        
        # retrieve image
        list_img = []
        for i in job_elem[0].find_all('img'):
            i = i['src']
            if i.find('_AC_') != -1:
                c = i.split('_AC_')
                i = str(c[0]) + '_AC_UX500_' + str(c[1].split('_')[-1:][0])
                
            list_img.append(i)
            
        # result image
        img = list_img

        # get price
        price_all = sou.find_all('span', class_='apexPriceToPay') # find price element in HTML
        price_result = price_all[0].find_all('span')[0].text.strip() # break price to result
        
        # result
        source = 'amazon.com'
        title = title
        image = img
        price = price_result.split('$')[1]
        code = 0
            
        # except:
        #     code = 1
        #     teks = 'Scrapping Failed from amazon.com, please use another option'
    
    if o == 'ebay':
        try:
            pag = requests.get(u) # get url response

            sou = BeautifulSoup(pag.content,'html.parser') # get content using bs4

            job = sou.find_all('div', id='vi_main_img_fs') # get img content
            
            # build image's result
            list_img = job[0].find_all('img')
            list_all_img = []
            for i in list_img:
                img = i['src']
                if img.find('s-l64'):
                    img = img.replace('s-l64', 's-l500')

                list_all_img.append(img)

            images = list_all_img
            
            # build title's result
            tit = sou.find_all('h1', id='itemTitle')[0].text.strip()    
            l = tit.split('  ')
            title = ''
            if len(l[1:]) > 1:
                for i in l[1:]:
                    title += f"{i} "
            else:
                title = l[1]
            
            # build price's result
            price = sou.find_all('span', id='prcIsum')[0].text.strip()
            price = price.split('$')[1]
            
            # result
            source = 'ebay.com'
            title = title
            image = images
            price = price
            code = 0
        except:
            code = 1
            teks = 'Scrapping Failed from ebay.com, please use another option'
    # summary to output
    
    if code == 0:
        result = {'source':source,
                'title':title,
                'image':image,
                'price':price,
                'id_price':group(float(price)*15104),
                'code': code}
        
    else:
        result = {'code':code, 'text':teks}
    
    return result

# break for price
def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))