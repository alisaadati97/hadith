import requests
import os
import re

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

def remove_html_tags(raw):
     
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw)
    return cleantext

def get_hadith_data(hadith_id):

    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":""}'
    
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', headers=headers, data=data)
    resp = response.json()
    resp = resp["data"][0]
    
    

    groupTogetherList = resp["groupTogetherList"]
    
    for hadith in groupTogetherList:

        hadith_url = f"https://hadith.inoor.ir/fa/hadith/{hadith['hadithId']}/translate"

        #write to db
        hadith_obj , created  = Hadith.objects.get_or_create(
                                source_identifier = hadith["hadithId"],
                                group_id = hadith["groupId"],
                                source_url = hadith_url
                                 )
  
        if not created:
            continue
        hadith_obj.save()
        hadithref_obj = HadithReference.objects.create( hadith = hadith_obj ,
                                        name = hadith["sourceMainTitle"] ,
                                        volume = hadith["vol"] ,
                                        page = hadith["pageNum"] ,
                                        )
        hadithref_obj.save()

    hadith_obj  = Hadith.objects.get(
                                source_identifier = hadith_id,
                                 )    
    hadith_obj.text = remove_html_tags(resp["text"])
    hadith_obj.save()

    for qael in resp["qaelList"]:
        teller_obj , created  = Teller.objects.get_or_create(
            name = qael["title"],
            order = qael["order"],
            qael_id = qael["id"],
            qaelroleid = qael["qaelRoleId"], 
        )
        HadithTeller.objects.create(hadith=hadith_obj,teller=teller_obj)

    resp["hasTranslate"]
    resp["hasExplanation"]
    resp["qaelTitleList"]

    return resp['hasTranslate'] , resp['hasExplanation']

def get_hadith_explanation(hadith_id):

    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":"","searchIn":"explanation"}'
    
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', headers=headers, data=data)
    resp = response.json()
    resp = resp["data"][0]

    hadith_obj  = Hadith.objects.get(
                                source_identifier = hadith_id,
                                 )   

    explanationList = resp["explanationList"]

    for explanation in explanationList:

        hadithexplain_obj = HadithExplanation.objects.create(hadith = hadith_obj )
        hadithexplain_obj.text = remove_html_tags(explanation["text"])
        hadithexplain_obj.textwithoutformat = explanation["textWithoutFormat"]
        hadithexplain_obj.save()

        hadithexplainref_obj = HadithExplanationReference.objects.create(hadithexplain = hadithexplain_obj )
        hadithexplainref_obj.maintitle = explanation["sourceMainTitle"]
        hadithexplainref_obj.volume = explanation["vol"]
        hadithexplainref_obj.page = explanation["pageNum"]
        hadithexplainref_obj.save()

    
def get_hadith_translation(hadith_id):

    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":"","searchIn":"translate"}'
    
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', headers=headers, data=data)
    resp = response.json()
    resp = resp["data"][0]

    hadith_obj  = Hadith.objects.get(
                                source_identifier = hadith_id,
                                 )

    translateList = resp["translateList"]

    for translate in translateList:

        hadithtranslate_obj = HadithTranslation.objects.create(hadith = hadith_obj )
        hadithtranslate_obj.language = "en"
        hadithtranslate_obj.text = remove_html_tags(translate["text"])
        hadithtranslate_obj.textwithoutformat = translate["textWithoutFormat"]
        hadithtranslate_obj.save()

        hadithtranslateref_obj = HadithTranslationReference.objects.create(hadith = hadith_obj )
        hadithtranslateref_obj.shorttitle = translate["sourceShortTitle"]
        hadithtranslateref_obj.maintitle = translate["sourceMainTitle"]
        hadithtranslateref_obj.page = translate["pageNum"]
        hadithtranslateref_obj.volume = translate["vol"]
        hadithtranslateref_obj.save()

hadith_id = 103907

t , e = get_hadith_data(hadith_id)

if t :
    get_hadith_translation(hadith_id)
if e :
    get_hadith_explanation(hadith_id)