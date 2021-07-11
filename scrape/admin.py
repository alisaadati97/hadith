from django.contrib import admin

from django.apps import apps

from .models import * 

class  hadithAdmin(admin.ModelAdmin):
    list_display=('source_identifier','ingroup_by_id','source_url')


class  translationAdmin(admin.ModelAdmin):
    list_display=('hadith','translation_text')


class  tellerAdmin(admin.ModelAdmin):
    list_display=('name',)

class  tellernameAdmin(admin.ModelAdmin):
    list_display=('name','hadith')


class  hadithTellerAdmin(admin.ModelAdmin):
    list_display=('teller','hadith')
class  hadithReferenceAdmin(admin.ModelAdmin):
    list_display=('name','hadith',"volume",'page')


class  translationReferenceAdmin(admin.ModelAdmin):
    list_display=('name','hadith',"volume",'page')
class  hadithExplainAdmin(admin.ModelAdmin):
    list_display=('name','hadith',"volume",'page')



admin.site.register(Hadith, hadithAdmin)
admin.site.register(Translation, translationAdmin)
admin.site.register(Teller, tellerAdmin)
admin.site.register(Tellername, tellernameAdmin)  

admin.site.register(HadithTeller, hadithTellerAdmin)  
admin.site.register(HadithReference, hadithReferenceAdmin)  

admin.site.register(TranslationReference, translationReferenceAdmin)  
admin.site.register(HadithExplain, hadithExplainAdmin)  