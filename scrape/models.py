from django.db import models

# Create your models here.
class Hadith(models.Model):
    source_identifier = models.PositiveIntegerField(null=True, blank=True)
    
    group_id = models.PositiveIntegerField(null=True, blank=True)

    text = models.TextField(null=True, blank=True) 

    source_url = models.URLField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f"{self.source_identifier}"

class HadithReference(models.Model):
    hadith = models.ForeignKey(Hadith,on_delete=models.CASCADE, null=True)
    name =  models.CharField(max_length=200,null=True, blank=True)
    volume = models.PositiveIntegerField(null=True, blank=True)
    page = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.volume} - {self.page} "


class Teller(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    order = models.CharField(max_length=200,null=True, blank=True)
    qael_id = models.CharField(max_length=200,null=True, blank=True)
    qaelroleid = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Tellername(models.Model):
    teller = models.ForeignKey(Teller,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    hadith = models.ForeignKey(Hadith,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"

class HadithTeller(models.Model):
    hadith = models.ForeignKey(Hadith,on_delete=models.CASCADE, null=True)
    teller = models.ForeignKey(Teller,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.teller}"


class HadithTranslation(models.Model):
    hadith = models.ForeignKey(Hadith,on_delete=models.CASCADE, null=True)
    language = models.CharField(max_length=200,null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    textwithoutformat = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.hadith}"

class HadithTranslationReference(models.Model):
    hadith = models.ForeignKey(Hadith,on_delete=models.CASCADE, null=True)
    shorttitle =  models.CharField(max_length=200,null=True, blank=True)
    maintitle =  models.CharField(max_length=200,null=True, blank=True)
    volume = models.PositiveIntegerField(null=True, blank=True)
    page = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.shorttitle} - {self.volume} - {self.page} "

class HadithExplanation(models.Model):
    hadith = models.ForeignKey(Hadith,on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True, blank=True)
    textwithoutformat = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.hadith} "

class HadithExplanationReference(models.Model):
    hadithexplain = models.ForeignKey(HadithExplanation,on_delete=models.CASCADE, null=True)
    maintitle =  models.CharField(max_length=200,null=True, blank=True)
    volume = models.PositiveIntegerField(null=True, blank=True)
    page = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.maintitle} - {self.volume} - {self.page} "





class Source(models.Model):
    name =  models.CharField(max_length=200,null=True, blank=True)
    source_type =  models.CharField(max_length=200,null=True, blank=True)
    domain = models.CharField(max_length=200,null=True, blank=True)
    banned = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
 
class Categories(models.Model):
    parent_id = models.PositiveIntegerField(null=True, blank=True)
    title =  models.CharField(max_length=200,null=True, blank=True)
    slug =  models.CharField(max_length=200,null=True, blank=True)
    priority = models.PositiveIntegerField(null=True, blank=True)
    status =  models.PositiveIntegerField(null=True, blank=True)
    post_count =  models.PositiveIntegerField(null=True, blank=True)
    total_view_count =  models.PositiveIntegerField(null=True, blank=True)
    keywords =  models.CharField(max_length=200,null=True, blank=True)
    description =  models.CharField(max_length=200,null=True, blank=True)
    instagram_conf =  models.CharField(max_length=200,null=True, blank=True)
   
    created_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=200,null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)