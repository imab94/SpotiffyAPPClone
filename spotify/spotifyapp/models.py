from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
from django.utils import timezone
from mutagen.mp3 import MP3
from datetime import timedelta
from django.core.files import File



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128, default='')
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    mobile_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        unique=True,
        null=True,
        blank=True,
    )
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default='O')
    country = models.CharField(max_length=100, default='', blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    # Specify custom related names for the groups and user_permissions fields
    groups = models.ManyToManyField('auth.Group', verbose_name='Groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', verbose_name='User Permissions', blank=True, related_name='custom_user_permissions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists', blank=True, null=True)
    favorited_by = models.ManyToManyField(CustomUser, related_name='favorite_artists', blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    favorited_by = models.ManyToManyField(CustomUser, related_name='favorite_genres', blank=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.CharField(max_length=255, blank=True)
    release_date = models.DateField()
    duration = models.CharField(blank=True, null=True,max_length=100)
    genres = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='songs', blank=True, null=True)
    audio_file = models.FileField(upload_to='songs')
    favorited_by = models.ManyToManyField(CustomUser, related_name='favorite_songs', blank=True)
    
    def save(self, *args, **kwargs):
        try:
            audio = MP3(self.audio_file)
            duration_seconds = int(audio.info.length)
            minutes, seconds = divmod(duration_seconds, 60)
            self.duration = f"{minutes:02d}:{seconds:02d}"
        except Exception as e:
            print(f"Error processing audio file: {e}")

        super().save(*args, **kwargs)

        
    def __str__(self):
        return self.title

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255, default='', null=True, blank=True)
    image = models.ImageField(upload_to='playlists', default='', blank=False, null=False)
    songs = models.ManyToManyField(Song, blank=True)

    class Meta:
        unique_together = (('user', 'title'),)

    def __str__(self):
        return self.title

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,null=True, blank=True)
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.user} follows {self.artist}"

class CategoryCards(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cards_categories')
    color_hex_code = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural ='CategoryCards'
    
    def __str__(self):
        return self.name
