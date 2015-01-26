from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    
class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )

class LinkAdmin(admin.ModelAdmin): 
    pass

class VoteAdmin(admin.ModelAdmin): 
    pass

admin.site.register(Link, LinkAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)