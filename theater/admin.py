from django.contrib import admin
from .models import UsabilityTest, UsabilityTestVideo, TestNotes

admin.site.register(UsabilityTest)
admin.site.register(UsabilityTestVideo)
admin.site.register(TestNotes)