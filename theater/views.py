import os
from django.shortcuts import redirect, render, get_object_or_404
import requests
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from .models import UsabilityTest, UsabilityTestVideo, TestNotes, Transcript, SentimentAnalysis


def home(request):

    context = {
        'usability_test': UsabilityTest.objects.all(),
        'usability_test_video': UsabilityTestVideo.objects.all(),
        'test_notes': TestNotes.objects.all()
    }

    return render(request, 'theater/theater.html', context)


class TestView(DetailView):
    model = UsabilityTest
    template_name = 'theater/theater.html'

# class TestJsonDetailView(View):
#     def get(self, *args, **kwargs):
#         test = UsabilityTest.objects.get(self.kwargs["pk"])
#         data = serialize('json', [test])
#         return JsonResponse(data, safe=False)


class VideoCreateView(CreateView):
    model = UsabilityTestVideo
    fields = ['file']

    def form_valid(self, form):
        form.instance.usability_test_id = self.kwargs["pk"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('theater-detail', kwargs={'pk': self.kwargs["pk"]})
    
class VideoDeleteView(DeleteView):
    model = UsabilityTestVideo
     
    def get_success_url(self):
        return reverse('theater-detail', kwargs={'pk': self.kwargs["pk_alt"]})

class NoteListView(ListView):
    model = TestNotes
    template_name = 'theater/theater.html'
    context_object_name = 'notes'

class NoteCreateView(CreateView):
    model = TestNotes
    fields = ['brief', 'description']

    def form_valid(self, form):
        form.instance.usability_test_id = self.kwargs["pk"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('theater-detail', kwargs={'pk': self.kwargs["pk"]})


class NoteUpdateView(UpdateView):
    model = TestNotes
    template_name = 'theater/testnotes_form.html'
    fields = ['brief', 'description']

    def form_valid(self, form):
        form.instance.usability_test_id = self.kwargs["pk_alt"]
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('theater-detail', kwargs={'pk': self.kwargs["pk_alt"]})

class NoteDeleteView(DeleteView):
    model = TestNotes
     
    def get_success_url(self):
        return reverse('theater-detail', kwargs={'pk': self.kwargs["pk_alt"]})
     
def TranscriptCreate(request, pk):
    # Display some HTML content
    html_content = "<html><body><h1>Creating transcript and analysis. This can take several minutes</h1></body></html>"
    response = HttpResponse(html_content)


    # Replace YOUR_API_KEY with your actual API key
    api_key = '70daa183740242a4a88459be789bc3dc'

    usability_test = get_object_or_404(UsabilityTest, id=int(pk))

    # Replace video_path with the local path of the video file you want to transcribe
    video_path = 'media/' + usability_test.videos.first().file.name
    print(video_path)
    # video_path = 'media/theater/WIN_20230301_22_10_09_Pro_Trim.mp4'

    # Set the API endpoint URL
    endpoint = 'https://api.assemblyai.com/v2/transcript'

    # Set the headers for the API request
    headers = {
        'authorization': api_key,
        'content-type': 'application/json'
    }


    # Upload the video file to AssemblyAI
    with open(video_path, 'rb') as f:
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                 headers={'authorization': api_key},
                                 data=f)
        media_url = response.json()['upload_url']


    # Set the data for the API request
    data = {
        'audio_url': media_url,
        # 'media_type': 'video',
        'speaker_labels': True,
        "auto_chapters": True,
        "sentiment_analysis": True
        # 'format_text': True
    }

    # Send the API request
    response = requests.post(endpoint, json=data, headers=headers)
    print(response.json())

    # If the request was successful, return the transcription
    if response.ok:
        transcript_id = response.json()['id']
        transcript_endpoint = f'{endpoint}/{transcript_id}'
        while True:
            response = requests.get(transcript_endpoint, headers=headers)
            status = response.json()['status']
            if status == 'completed':

                # Utterances
                utterance_response = requests.get(transcript_endpoint, headers=headers)
                utterance_response = utterance_response.json()

                speaker_text = ""

                for utter in utterance_response['utterances']:
                    speaker_text += "Speaker " + utter['speaker'] + ": " + utter['text'] + '\n'

                usability_test = get_object_or_404(UsabilityTest, id=int(pk))
                transcript = Transcript(usability_test=usability_test, utterances=speaker_text)
                transcript.save()
                

                # Auto notes
                # chapters_response = requests.get(trans_endpoint, headers=header)
                chapters_response = requests.get(transcript_endpoint, headers=headers)
                chapters_response = chapters_response.json()
                for chapter in chapters_response['chapters']:
                    note = TestNotes(usability_test=usability_test, brief=chapter['gist'], description=chapter['summary'])
                    note.save()

                # Sentiment Analysis
                sent_response = requests.get(transcript_endpoint, headers=headers)
                sent_response = sent_response.json()
                for sentiment in sent_response['sentiment_analysis_results']:
                    if sentiment['sentiment'] != 'NEUTRAL':
                        sentiment = SentimentAnalysis(transcript=transcript, text=sentiment['text'],
                                                    start=sentiment['start'], end=sentiment['end'],
                                                    sentiment=sentiment['sentiment'], confidence=sentiment['confidence'],
                                                    speaker=sentiment['speaker'])
                        sentiment.save()


                url = reverse('theater-detail', kwargs={'pk': pk})
                return redirect(url)

                # return speaker_text
            elif status == 'error':
                return JsonResponse({'error': response.json()['message']})
    # If the request failed, return an error message
    else:
        return JsonResponse({'error': response.json()['message']})
