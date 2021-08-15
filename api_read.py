import requests
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hadith.settings')
django.setup()

from scrape.models import *

headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'authorization': 'Bearer null',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://hadith.inoor.ir/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'DeviceType': 'web',
}

def get_hadith_data(hadith_id):
    print()
    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":""}'
    
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', headers=headers, data=data)
    resp = response.json()
    resp = resp["data"][0]

    hadith_id = resp["id"]
    #id in cherte
    print(f" hadith_id {hadith_id}")

    groupTogetherList = resp["groupTogetherList"]
    
    for hadith in groupTogetherList:
        
        hadith["hadithId"]
        hadith["vol"]
        hadith["pageNum"]
        hadith["sourceMainTitle"]
        hadith["groupId"]
        
        print(f"hadithId {hadith['hadithId']}")
        print(f"vol {hadith['vol']}")
        print(f"pageNum {hadith['pageNum']} ")
        print(f"sourceMainTitle {hadith['sourceMainTitle']} ")
        print(f"groupId {hadith['groupId']} ")
        

    resp["hasTranslate"]
    resp["hasExplanation"]
    resp["qaelTitleList"]
    resp["text"]
    
    print(f"hasTranslate {resp['hasTranslate']} ")
    print(f"hasExplanation {resp['hasExplanation']} ")
    print(f"qaelTitleList {resp['qaelTitleList']} ")
    print(f"text  {resp['text']}")

    return resp['hasTranslate'] , resp['hasExplanation']

def get_hadith_explanation(hadith_id):
    print()
    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":"","searchIn":"explanation"}'
    
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', headers=headers, data=data)
    resp = response.json()
    resp = resp["data"][0]

    explanationList = resp["explanationList"]

    for explanation in explanationList:

        explanation["text"]
        explanation["textWithoutFormat"]
        explanation["vol"]
        explanation["pageNum"]
        explanation["sourceMainTitle"]

        print(f"text {explanation['text']}")
        print(f"textWithoutFormat {explanation['textWithoutFormat']}")
        print(f"vol {explanation['vol']}")
        print(f"pageNum {explanation['pageNum']}")
        print(f"sourceMainTitle {explanation['sourceMainTitle']}")
    
def get_hadith_translation(hadith_id):
    print()
    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":"","searchIn":"translate"}'
    
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', headers=headers, data=data)
    resp = response.json()
    resp = resp["data"][0]

    translateList = resp["translateList"]

    for translate in translateList:

        translate["text"]
        translate["textWithoutFormat"]
        translate["vol"]
        translate["pageNum"]
        translate["sourceMainTitle"]
        translate["sourceShortTitle"]

        print(f"text {translate['text']}")
        print(f"textWithoutFormat {translate['textWithoutFormat']}")
        print(f"vol {translate['vol']}")
        print(f"pageNum {translate['pageNum']}")
        print(f"sourceMainTitle {translate['sourceMainTitle']}")
        print(f"sourceShortTitle {translate['sourceShortTitle']}")
        
    

hadith_id = 103923

t , e = get_hadith_data(hadith_id)

if t :
    get_hadith_translation(hadith_id)
if e :
    get_hadith_explanation(hadith_id)