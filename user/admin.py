from django.contrib import admin 

from quiz import models
 

# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Response)
admin.site.register(models.UserQuestion)