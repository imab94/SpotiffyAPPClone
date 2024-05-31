from django.contrib import admin
from .models import CustomUser, Artist, Genre, Song, Playlist, Album, Follow, CategoryCards

# Register your models here.
class SongAdmin(admin.ModelAdmin):
    readonly_fields = ['duration']
   
    
admin.site.register(CustomUser)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(Follow)
admin.site.register(CategoryCards)
admin.site.register(Song,SongAdmin)
