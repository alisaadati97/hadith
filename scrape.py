from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time  
from unidecode import unidecode
import os
from random import randint

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hadith.settings')
django.setup()

from scrape.models import *

class Hadithclass():
    def __init__(self):     
        self.driver = webdriver.Chrome('./chromedriver')   
    
    def start_scrape(self,id):
        self.base_id = id
        self.base_group_id = 0
        self.URL = f"https://hadith.inoor.ir/fa/hadith/{self.base_id}"
        self.hadith_page()
       
    def get_buttons(self):
        
        self.button_refrence_headers_before = self.driver.find_element_by_xpath("/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/hadith/section/div[2]/div/mat-tab-group/mat-tab-header/div[1]")
        self.button_refrence_headers_after = self.driver.find_element_by_xpath("/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/hadith/section/div[2]/div/mat-tab-group/mat-tab-header/div[3]")
    
    def get_headers(self):
        self.refrence_hedears_div = self.driver.find_element_by_class_name("mat-tab-labels")
        self.len_refrence_headers_divs = len(self.refrence_hedears_div.find_elements_by_class_name("mat-tab-label"))

    def go_to_hadith_by_header(self,i):
        div = self.driver.find_element_by_id(f"mat-tab-label-0-{i}")
        span = div.find_element_by_tag_name("span")
        span.click()  
        print("go_to_hadith_by_header")
        time.sleep(randint(2,3))
    
    def hadith_page(self):
        
        self.driver.get(self.URL)
        self.get_buttons()
        self.get_headers()

        time.sleep(randint(2,5))
        
        button_before_class = self.button_refrence_headers_before.get_attribute("class")

        cnt = 0
        while not "disabled" in button_before_class:
            self.button_refrence_headers_before.click()
            cnt += 1 
            if cnt > 10 : 
                break
        
        self.iterate_in_headers()
    
    def extract_ref(self , i ):
        div = self.driver.find_element_by_id(f"mat-tab-label-0-{i}")
        span = div.find_element_by_tag_name("span")
        
        
        refrence = span.text.split()    
        
        page = refrence.pop().replace("??","")
        volume = refrence.pop().replace("??","")
        name = " ".join(refrence)

        self.refrence_obj  = HadithReference.objects.create(
                hadith = self.hadith_obj ,
                name = name , 
                volume = volume ,
                page = page ,
                )
        span.click()       

    def get_hadith_data(self,i):
        
        hadith = self.driver.find_element_by_class_name("mat-tab-body-wrapper").find_element_by_class_name("mat-tab-body-active")
        h2s = hadith.find_elements_by_tag_name("h2")
        
        hadith_identifier = unidecode(h2s[0].text.split().pop())
        hadith_tellers_list = h2s[-1].find_element_by_tag_name("span").text.split(",")
        hadith_text = hadith.find_element_by_tag_name("hadith").text
        
        
        self.hadith_obj , created = Hadith.objects.get_or_create(
                source_identifier=hadith_identifier
                )
        print(f" createad is {created} {hadith_identifier}")
        if not created :
                print(f"step {i} {self.hadith_obj} is duplicated")
                return True

        for hadith_teller in hadith_tellers_list :
            self.teller ,created = Teller.objects.get_or_create(name=hadith_teller,)
            HadithTeller.objects.create(hadith=self.hadith_obj,
            teller=self.teller)
        
        hadith_teller_name = hadith.find_elements_by_tag_name("exporter")  
        #cannot say wich tellername is for which teller    
        for teller_name in hadith_teller_name:
            #self.teller_obj , created  = Teller.objects.get_or_create(name=teller_name.text)
            Tellername.objects.create(
                #teller = self.teller_obj, 
                name = teller_name.text ,
                hadith=self.hadith_obj,
                )
        
        if i == 0 :
            self.base_group_id = hadith_identifier
        
        self.hadith_obj.text = hadith_text
        self.hadith_obj.ingroup_by_id = self.base_group_id
        self.hadith_obj.source_url = f"https://hadith.inoor.ir/fa/hadith/{hadith_identifier}"
        self.hadith_obj.source_identifier = hadith_identifier
        self.hadith_obj.save()

        return False
    
    def get_hadith_translation(self):
        
        translation_header_div = self.driver.find_element_by_id("mat-tab-label-1-0")
        
        self.driver.execute_script("arguments[0].scrollIntoView();", translation_header_div)
        time.sleep(.5)
        translation_divs = self.driver.find_elements_by_class_name("mat-tab-body-wrapper")[-1]
        translations = translation_divs.find_elements_by_class_name("toggle-content")
        

        for translation in translations:
            translation_refrence = translation.find_element_by_tag_name("h3")
            translation_text = translation.find_element_by_tag_name("p")
            

            name = translation_refrence.text[:translation_refrence.text.find(";")]
            page = translation_refrence.text.split().pop()
            volume = translation_refrence.text.split().pop(-3)

            #print(f" ref name : {name} | vol : {volume} | page : {page} ")
            translation_text = translation_text.text

            TranslationReference.objects.create(
                hadith = self.hadith_obj ,
                text = translation_text ,
                name = name ,
                volume = volume , 
                page = page ,
            )

    def get_hadith_explaination(self):
        explaination_header_div = self.driver.find_element_by_id("mat-tab-label-1-1")
        explaination_header_div.click()
        time.sleep(.5)

        explaination_divs = self.driver.find_elements_by_class_name("mat-tab-body-wrapper")[-1]
        explainations = explaination_divs.find_elements_by_class_name("toggle-content")
        for explaination in explainations:
            explaination_refrence = explaination.find_element_by_tag_name("h3")
            explaination_text = explaination.find_element_by_tag_name("p")
            
            name = explaination_refrence.text[:explaination_refrence.text.find(";")]
            page = explaination_refrence.text.split().pop()
            volume = explaination_refrence.text.split().pop(-3)

            explaination_text = explaination_text.text

            HadithExplain.objects.create(
                hadith = self.hadith_obj ,
                text = explaination_text ,
                name = name ,
                volume = volume , 
                page = page ,
            )
                
    def iterate_in_headers(self):
        step_counter = 0
        for i in range(self.len_refrence_headers_divs):
            
            if i - step_counter > 2 :
                button_after_class = self.button_refrence_headers_after.get_attribute("class")
                if not "disabled" in button_after_class:
                    self.button_refrence_headers_after.click()
                step_counter = i
            print("before go_to_hadith_by_header")
            self.go_to_hadith_by_header(i)
            
            isduplicated = self.get_hadith_data(i)
            if isduplicated :
                #print(f"step {i} continuew occured {self.hadith_obj}")
                continue
            print(f"step {i} ########### source id : {self.hadith_obj}")
            time.sleep(randint(2,5))
            self.extract_ref(i)
            time.sleep(randint(1,3))            
            self.get_hadith_translation()
            #time.sleep(randint(1,3))
            self.get_hadith_explaination()
            #time.sleep(randint(1,3))
            print("")

        #self.driver.close()    

#id start 48113
#48129 problem
#48158 problem
hadithobj = Hadithclass()
for id in range(48167 , 500000):
    hadithobj.start_scrape(id)
