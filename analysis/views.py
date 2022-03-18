from django.shortcuts import render, redirect
from django.http import HttpResponse
from monkeylearn import MonkeyLearn
import csv
import os
import sys
import pandas as pd
import random
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *

# Create your views here.
def index(request):
    #csv.field_size_limit(sys.maxsize)
    ml = MonkeyLearn('69d1bf1df8ca6ff7f1aec9a196de801ad8fb24cf')
    #ml = MonkeyLearn('658c1dc14984481c2128bac656c441fa918b4a3f')
    sentence = request.POST.get("sentence")
    submit = request.POST.get("submit")
    
    if not sentence:
        context = {'output': "What's on your mind?", 'show_table': 'False'}
        return render(request, 'analysis/index.html', context)

    model_id = 'cl_pi3C7JiL'
    sentence = [sentence]
    result = ml.classifiers.classify(model_id, sentence)
    songs_data = pd.read_csv('data.csv')
    h = songs_data[songs_data.valence > 0.7]
    tag_name = result.body[0]['classifications'][0]['tag_name']
    confidence = result.body[0]['classifications'][0]['confidence']
    h = None
    threshold = 1
    if tag_name == 'Negative':
        threshold = 1 - confidence
        h = songs_data[songs_data.valence <= threshold]
        h = h[h.energy <= threshold]
    elif tag_name == 'Positive':
        threshold = confidence
        h = songs_data[songs_data.valence >= threshold]
        h = h[h.energy >= threshold]
    elif tag_name == 'Neutral':
        h = songs_data[(songs_data.valence >= 0.4) & (songs_data.valence < 0.8)]
        h = h[(h.energy >= 0.4) & (h.energy < 0.8)]
    h = h[h.year > 1980]
    output = h.to_dict('list')
    #output = 0
    #random.shuffle(output)

    artists = []
    name = []
    year = []
    ids = []
    
    for a in output['artists']:
        artists.append(a)
    for a in output['name']:
        name.append(a)
    for a in output['year']:
        year.append(a)
    for a in output['id']:
        ids.append(a)
    output = []
    
    for i in range(len(name)):
        art = ''
        for a in artists[i]:
            art+=a
        art = art.replace('[', '')
        art = art.replace(']', '')
        art = art.replace(str(chr(39)), '')
        #print(art)
        d = {'name': name[i], 'artist': art, 'year': year[i], 'id': ids[i]}
        output.append(d)
    random.shuffle(output)
    if len(output) > 27:
        print(len(output))
        output = output[: len(output) - (len(output) - 27)]
    print(len(output))
    context={'output': tag_name + ": " + str(confidence), 'results':output, 'sentence':sentence[0]}


    return render(request, 'analysis/index.html', context)

def about(request):

    return render(request, 'analysis/about.html')

# class AuthURL(APIView):
#     def get(self, request, fornat=None):
#         scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

#         url = Request('GET', 'https://accounts.spotify.com/authorize', params={
#             'scope': scopes,
#             'response_type': 'code',
#             'redirect_uri': REDIRECT_URI,
#             'client_id': CLIENT_ID
#         }).prepare().url

#         return Response({'url': url}, status=status.HTTP_200_OK)


# def spotify_callback(request, format=None):
#     code = request.GET.get('code')
#     error = request.GET.get('error')

#     response = post('https://accounts.spotify.com/api/token', data={
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': REDIRECT_URI,
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET
#     }).json()

#     access_token = response.get('access_token')
#     token_type = response.get('token_type')
#     refresh_token = response.get('refresh_token')
#     expires_in = response.get('expires_in')
#     error = response.get('error')

#     if not request.session.exists(request.session.session_key):
#         request.session.create()

#     update_or_create_user_tokens(
#         request.session.session_key, access_token, token_type, expires_in, refresh_token)

#     return redirect('frontend:')


# class IsAuthenticated(APIView):
#     def get(self, request, format=None):
#         is_authenticated = is_spotify_authenticated(
#             self.request.session.session_key)
#         return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


# class CurrentSong(APIView):
#     def get(self, request, format=None):
#         room_code = self.request.session.get('room_code')
#         room = Room.objects.filter(code=room_code)
#         if room.exists():
#             room = room[0]
#         else:
#             return Response({}, status=status.HTTP_404_NOT_FOUND)
#         host = room.host
#         endpoint = "player/currently-playing"
#         response = execute_spotify_api_request(host, endpoint)

#         if 'error' in response or 'item' not in response:
#             return Response({}, status=status.HTTP_204_NO_CONTENT)

#         item = response.get('item')
#         duration = item.get('duration_ms')
#         progress = response.get('progress_ms')
#         album_cover = item.get('album').get('images')[0].get('url')
#         is_playing = response.get('is_playing')
#         song_id = item.get('id')

#         artist_string = ""

#         for i, artist in enumerate(item.get('artists')):
#             if i > 0:
#                 artist_string += ", "
#             name = artist.get('name')
#             artist_string += name

#         votes = len(Vote.objects.filter(room=room, song_id=song_id))
#         song = {
#             'title': item.get('name'),
#             'artist': artist_string,
#             'duration': duration,
#             'time': progress,
#             'image_url': album_cover,
#             'is_playing': is_playing,
#             'votes': votes,
#             'votes_required': room.votes_to_skip,
#             'id': song_id
#         }

#         self.update_room_song(room, song_id)

#         return Response(song, status=status.HTTP_200_OK)

#     def update_room_song(self, room, song_id):
#         current_song = room.current_song

#         if current_song != song_id:
#             room.current_song = song_id
#             room.save(update_fields=['current_song'])
#             votes = Vote.objects.filter(room=room).delete()


# class PauseSong(APIView):
#     def put(self, response, format=None):
#         room_code = self.request.session.get('room_code')
#         room = Room.objects.filter(code=room_code)[0]
#         if self.request.session.session_key == room.host or room.guest_can_pause:
#             pause_song(room.host)
#             return Response({}, status=status.HTTP_204_NO_CONTENT)

#         return Response({}, status=status.HTTP_403_FORBIDDEN)


# class PlaySong(APIView):
#     def put(self, response, format=None):
#         room_code = self.request.session.get('room_code')
#         room = Room.objects.filter(code=room_code)[0]
#         if self.request.session.session_key == room.host or room.guest_can_pause:
#             play_song(room.host)
#             return Response({}, status=status.HTTP_204_NO_CONTENT)

#         return Response({}, status=status.HTTP_403_FORBIDDEN)
