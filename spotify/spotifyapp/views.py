from django.shortcuts import render
from .models import CategoryCards,Playlist,Genre,Song
# Create your views here.


def home(request):
    category_cards  = CategoryCards.objects.all()
    playlists = Playlist.objects.all()
    context = {
        'category_cards':category_cards,
        'playlists':playlists,
    }
    return render(request,'index.html',context)

def login_page(request):
    return render(request,'login.html')

def register_page(request):
    return render(request,'signup.html')

def dashboard(request,id):
    playlist_songs = Playlist.objects.get(id=id)
    songs = playlist_songs.songs.all()
    total_songs  = songs.count()
    total_duration_seconds = sum([int(song.duration.split(':')[0]) * 60 + int(song.duration.split(':')[1]) for song in songs])
    total_hours, remaining_minutes = divmod(total_duration_seconds, 3600)
    total_minutes = remaining_minutes // 60

    if total_hours > 0:
        total_duration_formatted = f"about {total_hours}hr {total_minutes}min"
    else:
        total_duration_formatted = f"about {total_minutes}min"
        
    context = {
        'total_songs':total_songs,
        'playlist': playlist_songs,
        'songs': songs,
        'total_duration_formatted':total_duration_formatted,
    }
    return render(request,'dashboard.html',context)

def phone_number_login(request):
    return render(request,'phone_number_login.html')


def verifications(request):
    return render(request,'verification.html')

def forget_password_page(request):
    return render(request,'forget_password.html')


def signup_playlists(request):
    return render(request,'playlist_signup.html')