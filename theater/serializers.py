from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import UsabilityTest, TestNotes



class CreateNoteSerializer(serializers.Serializer):
    class Meta:
        model = TestNotes
        fields = ['brief', 'description']

    def create(self, validated_data):
        test_id = self.context['product_id']
        return TestNotes.objects.create(usability_test=test_id, **validated_data)

    
    # def save(self, **kwargs):
    #     with transaction.atomic():

    #         usability_test = UsabilityTest.objects.get(user_id=self.context['test_id'])
    #         note = TestNotes.objects.create(usability_test=usability_test)
    #         note.brief = self.validated_data['brief']
    #         note.description = self.validated_data['description']
    #         note.save()

    #         return note
        
    