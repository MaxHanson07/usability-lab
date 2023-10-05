from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class UsabilityTest(models.Model):
    product_name = models.CharField(max_length=100)
    moderator = models.CharField(max_length=100, null=True)
    test_date = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('theater-detail')

class UsabilityTestVideo(models.Model):
    usability_test = models.ForeignKey(UsabilityTest, on_delete=models.CASCADE,
                                       related_name='videos')
    file= models.FileField(upload_to='theater/', null=True, verbose_name="")

class TestNotes(models.Model):
    usability_test = models.ForeignKey(UsabilityTest, on_delete=models.CASCADE,
                                       related_name='notes')
    brief = models.CharField(max_length=100)
    description = models.TextField(null=True)
    timestamp = models.TimeField(null=True)

class Transcript(models.Model):
    usability_test = models.ForeignKey(UsabilityTest, on_delete=models.CASCADE,
                                       related_name='transcript')
    utterances = models.TextField()

class SentimentAnalysis(models.Model):
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE,
                                       related_name='sentiment')
    text = models.TextField()
    start = models.IntegerField()
    end = models.IntegerField()
    sentiment = models.CharField(max_length=100)
    confidence = models.FloatField()
    speaker = models.CharField(max_length=50)
