import requests
import os
import re
from time import sleep
import logging
import datetime
import sys




import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hadith.settings')
django.setup()

from scrape.models import *

logging.basicConfig(filename='log.log',filemode='a',datefmt='%H:%M:%S', level=logging.DEBUG)

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

def exit_if_banned(hadith_id, date ,status_code ):
    if status_code == 429 or status_code == 430 :
        logging.error(f'hadith id : {hadith_id} {date} statuscode 429 or 430 occured and exit!')
        sys.exit()

def save_hadith_data(hadith_id,resp):
    groupTogetherList = resp["groupTogetherList"]   
    for hadith in groupTogetherList:
        hadith_url = f"https://hadith.inoor.ir/fa/hadith/{hadith['hadithId']}/translate"
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

def save_hadith_explanation(hadith_id,resp):
    hadith_obj  = Hadith.objects.get(source_identifier = hadith_id)   

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

def save_hadith_translation(hadith_id,resp):
    hadith_obj  = Hadith.objects.get(source_identifier = hadith_id,)

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

def get_response(hadith_id,date, data , data_type):
    response = requests.post('https://hadith.inoor.ir/service/api/elastic/ElasticHadithById', 
        headers=headers, data=data)
    exit_if_banned(hadith_id, date ,response.status_code )

    resp = response.json()

    if data_type == "data":
        if not resp["isSuccess"]:
            logging.error(f'hadith id : {hadith_id} {date} {data_type} notSuccess')
            return False , False
        try : 
            resp = resp["data"][0]
        except:
            logging.error(f'first exception occured !!! hadith id : {hadith_id} {date}')
    
    elif data_type == "explain":
        if not resp["isSuccess"]:      
            logging.error(f'hadith id : {hadith_id} {date} {data_type} notSuccess')
            return None 
        try : 
            resp = resp["data"][0]
        except:
            logging.error(f'second exception occured !!! hadith id : {hadith_id} {date}')

    elif data_type == "translate":
        if not resp["isSuccess"]:
            logging.error(f'hadith id : {hadith_id} {date} {data_type} notSuccess')
            return None
        try : 
            resp = resp["data"][0]
        except:
            logging.error(f'third exception occured !!! hadith id : {hadith_id} {date}')
   
    
    return resp
    

def get_hadith_data(hadith_id, date):

    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":""}'
    resp = get_response(hadith_id,date, data,'data')
    save_hadith_data(hadith_id,resp)
    return resp['hasTranslate'] , resp['hasExplanation']

def get_hadith_explanation(hadith_id, date):

    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":"","searchIn":"explanation"}'
    resp = get_response(hadith_id,date, data,'explain')
    save_hadith_explanation(hadith_id,resp)
    
def get_hadith_translation(hadith_id, date):
    data = '{"hadithId":[' + str(hadith_id) + '],"searchPhrase":"","searchIn":"translate"}'
    resp = get_response(hadith_id,date, data,'translate') 
    save_hadith_translation(hadith_id,resp)

    

if __name__ == "__main__":
    hadith_id = 48303
    logging.info(f'new run')
    while True:
        logging.info(f'')
        date = datetime.datetime.now().strftime("%Y%m%d, %H:%M:%S")
        logging.info(f'hadith id : {hadith_id} {date}')
        
        t , e = get_hadith_data(hadith_id , date)

        if t :
            get_hadith_translation(hadith_id, date)
            sleep(15)
        if e :
            get_hadith_explanation(hadith_id, date)
            sleep(15) 
        sleep(15)
        hadith_id += 1 