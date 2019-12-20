from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from music.models import Album, Song
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    #all_album = Album.objects.all()
    all_album= Album.objects.filter(user = request.user)
    return render(request,'music/index.html', {'all_album':all_album})
@login_required
def detail(request, album_id):
    try: 
        album = Album.objects.get(id= album_id)
    except Album.DoesNotExist :
        raise Http404("Album does not exist")
    if album in request.user.album_set.all():
        return render(request, 'music/detail.html',{'album':album})
    else:
        raise Http404("Album Not Yours")
@login_required
def favourite(request,album_id):
    try:
        album = Album.objects.get(id= album_id)
    except (Album.DoesNotExist) :
        return Http404("Album does not exist")
    if 'favourite' in request.POST:
        try:
            selected_song = album.song_set.get(id = request.POST['song'])
        except (KeyError, Song.DoesNotExist):
            return render(request,'music/detail.html',{'album':album,'error_message': "No song selected"})
        else:
            selected_song.is_favorite = True
            selected_song.save() 
            return render(request,'music/detail.html', {'album': album})
    if 'unfavourite' in request.POST:
        try:
            selected_song = album.song_set.get(id = request.POST['song'])
        except (KeyError, Song.DoesNotExist):
            return render(request,'music/detail.html',{'album':album,'error_message': "No song selected"})
        else:
            selected_song.is_favorite = False
            selected_song.save()
            return render(request,'music/detail.html', {'album': album})
    if 'delete' in request.POST:
        try:
            selected_song = album.song_set.get(id = request.POST['song'])
        except (KeyError, Song.DoesNotExist):
            return render(request,'music/detail.html',{'album':album,'error_message': "No song selected"})
        else:
            selected_song.delete()
            return render(request,'music/detail.html', {'album': album})
@login_required
def addSong(request,album_id):
    try: 
        album= Album.objects.get(id= album_id)
    except Album.DoesNotExist:
        return Http404("Album does not exist")
    if 'addSong'in request.POST and 'audio_file' in request.FILES :
        file_type = request.POST['file_type']
        title = request.POST['title']
        album.song_set.create(file_type= file_type,song_title= title, audio_file= request.FILES['audio_file'] )
        return render(request,'music/detail.html',{'album': album})

@login_required
def add(request):
    #all_album = Album.objects.all()
    all_album= Album.objects.filter(user = request.user)
    if 'add' in request.POST and 'logo' in request.FILES:
        artist = request.POST['artist']
        title= request.POST['title']
        genre = request.POST['genre']
        a = User.objects.get(username = request.user.username)
        print(a.username)
        a.album_set.create(artist= artist,album_title = title, genre = genre, album_logo= request.FILES['logo'])
        #a= Album(user= request.user,artist= artist,album_title = title, genre = genre, album_logo= request.FILES['logo'])
        #a.save()
    return render(request,'music/index.html', {'all_album':all_album})
@login_required
def delete(request,album_id):
    album = Album.objects.get(id = album_id)
    album.delete()
    all_album = Album.objects.all()
    return render(request,'music/index.html', {'all_album':all_album})
def register(request):
    if 'register' in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'music/register.html',{'error_message':"Username already taken"})
            elif User.objects.filter(email = email).exists():
                return render(request,'music/register.html',{'error_message':"Email already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1, email = email, first_name= first_name, last_name = last_name)
                user.save()
                return redirect('/music/login/')
        else:
            return render(request,'music/register.html',{'error_message':"Password does not match"})
    return render(request,'music/register.html')
def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            return redirect('/music/')
        else:
            return render(request, 'music/login.html', {'error_message': "Invalid Credentials"})
    return render(request, 'music/login.html')
def test(request):
    return render(request,'ayush.html')
