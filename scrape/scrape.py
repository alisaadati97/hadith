from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time  



class Hadith():
    def __init__(self):
        
        self.driver = webdriver.Chrome('./chromedriver')
        base_id = 48113
        self.source_id = 48113
        self.URL = f"https://hadith.inoor.ir/fa/hadith/{base_id}"
        
        self.hadith_page()
    
    def get_buttons(self):
        self.button_refrence_headers_before = self.driver.find_element_by_xpath("/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/hadith/section/div[2]/div/mat-tab-group/mat-tab-header/div[1]")
        self.button_refrence_headers_after = self.driver.find_element_by_xpath("/html/body/app-root/div/mat-sidenav-container/mat-sidenav-content/hadith/section/div[2]/div/mat-tab-group/mat-tab-header/div[3]")
    
    def get_headers(self):
        self.refrence_hedears_div = self.driver.find_element_by_class_name("mat-tab-labels")
        self.len_refrence_headers_divs = len(self.refrence_hedears_div.find_elements_by_class_name("mat-tab-label"))

    def hadith_page(self):
        
        self.driver.get(self.URL)
        self.get_buttons()
        self.get_headers()

        time.sleep(1)
        
        button_before_class = self.button_refrence_headers_before.get_attribute("class")

        while not "disabled" in button_before_class:
            self.button_refrence_headers_before.click()
        
        self.iterate_in_headers()
    
    def extract_ref(self , i ):
        div = self.driver.find_element_by_id(f"mat-tab-label-0-{i}")
        span = div.find_element_by_tag_name("span")
        
        
        refrence = span.text.split()    
        
        page = refrence.pop().replace("ص","")
        volume = refrence.pop().replace("ج","")
        name = " ".join(refrence)
        
        print(f" ref name : {name} | vol : {volume} | page : {page} ")

        span.click()       

    def get_hadith_data(self):
        
        hadith = self.driver.find_element_by_class_name("mat-tab-body-wrapper").find_element_by_class_name("mat-tab-body-active")
        h2s = hadith.find_elements_by_tag_name("h2")
        
        hadith_identifier = h2s[0].text.split().pop()
        hadith_teller = h2s[-1].text.split().pop()
        hadith_text = hadith.find_element_by_tag_name("hadith").text

        hadith_tellers = hadith.find_elements_by_tag_name("exporter")
        for teller in hadith_tellers:
            print(teller.text)
  
    def get_hadith_translation(self):
        
        translation_header_div = self.driver.find_element_by_id("mat-tab-label-1-0")
        
        self.driver.execute_script("arguments[0].scrollIntoView();", translation_header_div)
        time.sleep(2)
        translation_divs = self.driver.find_elements_by_class_name("mat-tab-body-wrapper")[-1]
        translations = translation_divs.find_elements_by_class_name("toggle-content")
        
        for translation in translations:
            translation_refrence = translation.find_element_by_tag_name("h3")
            translation_text = translation.find_element_by_tag_name("p")
            print(translation_refrence.text)
    
    def get_hadith_explaination(self):
        explaination_header_div = self.driver.find_element_by_id("mat-tab-label-1-1")
        explaination_header_div.click()
        time.sleep(2)

        explaination_divs = self.driver.find_elements_by_class_name("mat-tab-body-wrapper")[-1]
        explainations = explaination_divs.find_elements_by_class_name("toggle-content")
        for explaination in explainations:
            explaination_refrence = explaination.find_element_by_tag_name("h3")
            explaination_text = explaination.find_element_by_tag_name("p")
            print(explaination_refrence.text)
        
    def iterate_in_headers(self):
        step_counter = 0
        for i in range(self.len_refrence_headers_divs):
            if i - step_counter > 4 :
                button_after_class = self.button_refrence_headers_after.get_attribute("class")
                if not "disabled" in button_after_class:
                    self.button_refrence_headers_after.click()
                step_counter = i
            #TODO check if the hadith data is not duplicated
            self.extract_ref(i)
            time.sleep(3)
            self.get_hadith_data()
            time.sleep(3)
            self.get_hadith_translation()
            time.sleep(3)
            self.get_hadith_explaination()
            time.sleep(3)

        self.driver.close()    


Hadith()
# with open("test.txt",'a',encoding = 'utf-8') as f:
#     print(f"------------ iterate {i}")
#     f.write(f" ref name : {name} | vol : {volume} | page : {page} \n ")
#     f.write(f" hadith_identifier : {hadith_identifier} | hadith_teller : {hadith_teller}  \n ")
#     f.write(f" hadith_text : {hadith_text}  \n ")
