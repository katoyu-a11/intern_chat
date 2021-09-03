from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class ImageModel(models.Model):
    image = models.ImageField(upload_to='media')
    image_user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='image_user')

class TalkModel(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    talkname = models.ForeignKey(User,on_delete=models.CASCADE,related_name='talkname')
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)



