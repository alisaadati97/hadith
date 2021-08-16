from django.contrib import admin

from django.apps import apps

from .models import * 

class  hadithAdmin(admin.ModelAdmin):
    list_display=('source_identifier','group_id','source_url')

class  hadithReferenceAdmin(admin.ModelAdmin):
    list_display=('hadith','name',"volume",'page')




class  tellerAdmin(admin.ModelAdmin):
    list_display=('name','order','qael_id','qaelroleid',)

class  tellernameAdmin(admin.ModelAdmin):
    list_display=('name','hadith')
class  hadithTellerAdmin(admin.ModelAdmin):
    list_display=('teller','hadith')

class  translationAdmin(admin.ModelAdmin):
    list_display=('hadith','text')
class  translationReferenceAdmin(admin.ModelAdmin):
    list_display=('hadith','shorttitle',"volume",'page')

class  hadithExplanationAdmin(admin.ModelAdmin):
    list_display=('hadith','text')
class  hadithExplanationReferenceAdmin(admin.ModelAdmin):
    list_display=('hadithexplain','maintitle','volume','page')



admin.site.register(Hadith, hadithAdmin)
admin.site.register(HadithReference, hadithReferenceAdmin) 


admin.site.register(Teller, tellerAdmin)
admin.site.register(Tellername, tellernameAdmin)  
admin.site.register(HadithTeller, hadithTellerAdmin)  
 
admin.site.register(HadithTranslation, translationAdmin)
admin.site.register(HadithTranslationReference, translationReferenceAdmin)  

admin.site.register(HadithExplanation, hadithExplanationAdmin)  
admin.site.register(HadithExplanationReference, hadithExplanationReferenceAdmin)  

