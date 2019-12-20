from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
# Create your models here.

class Album(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    artist = models.CharField(max_length= 500,null= True, blank=True )
    album_title = models.CharField(max_length= 500,null= True, blank=True)
    genre = models.CharField(max_length= 500,null= True, blank=True)
    album_logo = models.FileField(null= True,validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])] )
    def __str__(self):
        return self.album_title + ' by ' + self.artist
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete= models.CASCADE)
    file_type = models.CharField(max_length=10, null= True, blank=True)
    song_title = models.CharField(max_length=250, null= True, blank=True)
    is_favorite = models.BooleanField(default= False, null= True )
    audio_file = models.FileField(null= True, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    def __str__(self):
        return self.song_title + '-' + self.album.album_title

    
    



