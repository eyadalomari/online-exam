from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Exam)
admin.site.register(models.Skill)
admin.site.register(models.E_Skill)
admin.site.register(models.Question_Type)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Student_Exam)
admin.site.register(models.Student_Answer)