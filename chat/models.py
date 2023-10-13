from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.CharField(max_length=100000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items')


    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name
    
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size =(300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Chat(models.Model):
    item = models.ForeignKey(Item, related_name='chats', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.item.name}'

    


class Chatext(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.created_by.username}'
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='benz.jpg', upload_to='profile')

    def __str__(self) -> str:
        return f'{self.user.username} Profile' 

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self) -> str:
        return f'{self.user.username}'
