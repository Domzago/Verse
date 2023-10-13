from django.contrib import admin

from chat.models import Item, Chat, Chatext, Profile

admin.site.register(Item)
admin.site.register(Chat)
admin.site.register(Chatext)
admin.site.register(Profile)
