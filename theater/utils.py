import requests
import time
# import pandas as pd


upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# Helper for `upload_file()`
def read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            print(data)
            if not data:
                break
            yield data


# Uploads a file to AAI servers
def upload_file(audio_file, header):
    upload_response = requests.post(
        upload_endpoint,
        headers=header, data=read_file(audio_file),
        
    )
    return upload_response.json()

def add_videos(videos, new_video):
    videos.append(new_video)

# Request transcript for file uploaded to AAI servers
def request_transcript(upload_url, header):
    transcript_request = {
        'audio_url': upload_url['upload_url'],
        'speaker_labels': True
    }

    transcript_response = requests.post(
        transcript_endpoint,
        json=transcript_request,
        headers=header
    )
    return transcript_response.json()

# Make a polling endpoint
def make_polling_endpoint(transcript_response):
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']
    return polling_endpoint

# Wait for the transcript to finish
def wait_for_completion(polling_endpoint, header):
    while True:
        polling_response = requests.get(polling_endpoint, headers=header)
        polling_response = polling_response.json()
        print(polling_response)

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)

    print("done")


# Get the paragraphs of the transcript
def get_paragraphs(polling_endpoint, header):
    paragraphs_response = requests.get(polling_endpoint + "/paragraphs", headers=header)
    paragraphs_response = paragraphs_response.json()

    paragraphs = []
    for para in paragraphs_response['paragraphs']:
        paragraphs.append(para)

    return paragraphs

def get_utterances(polling_endpoint, header):
    utterance_response = requests.get(polling_endpoint, headers=header)
    utterance_response = utterance_response.json()

    utterances = []
    for utter in utterance_response['utterances']:
        utterances.append(utter)

    return utterances

def get_highlights(polling_endpoint, header):
    highlights_response = requests.get(polling_endpoint, headers=header)
    highlights_response = highlights_response.json()

    highlights = []
    for utter in highlights_response['auto_highlights_result']['results']:
        highlights.append(utter)

    return highlights

def get_chapters(polling_endpoint, header):
    chapters_response = requests.get(polling_endpoint, headers=header)
    chapters_response = chapters_response.json()

    chapters = []
    for chapter in chapters_response['chapters']:
        chapters.append(chapter)

    return chapters

# def get_sent(polling_endpoint, header):
#     sent_response = requests.get(polling_endpoint, headers=header)
#     sent_response = sent_response.json()['sentiment_analysis_results']
#     sent = pd.DataFrame(sent_response)

#     return sent