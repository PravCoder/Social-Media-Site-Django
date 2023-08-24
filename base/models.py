from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from cloudinary.models import CloudinaryField

"""class MediaFile(models.Model):
    image = CloudinaryField("image")"""

class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    biography = models.TextField(null=True)
    posts = models.ManyToManyField("Post", related_name="posts", blank=True)
    profile_pic = models.FileField(upload_to='media-images', null=True)

    following = models.ManyToManyField("User", related_name="+", blank=True) # the people that this user is following
    followers = models.ManyToManyField("User", related_name="+", blank=True) # the people that are following this user
    num_followers = models.IntegerField(default=0,null=True,blank=True) # number of people following this user
    num_following = models.IntegerField(default=0,null=True,blank=True) # number of people that this user is follwing
    liked_posts = models.ManyToManyField("Post", related_name="liked_posts", blank=True)
    # when user clicks dm it add dmc-obj to this for that user, when the other user sends a message 
    direct_message_chats = models.ManyToManyField("DirectMessageChat", related_name="direct_message_chats", blank=True)

    public_id_profile_image = models.CharField(max_length=100, null=-True)

    @property
    def get_num_followers(self):
        count = 0
        for x in self.followers.all():
            count += 1
        return count
    @property
    def get_num_following(self):
        count = 0
        for x in self.following.all():
            count += 1
        return count
    
    @property
    def get_profile_pic(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/default_profile.png"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

class Post(models.Model):
    content = models.CharField(max_length=10000, null=True)
    varitey = models.CharField(max_length=100, null=-True)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="author",blank=True)  # image, text, video
    likes = models.IntegerField(default=0,null=True,blank=True)
    posted_date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.FileField(upload_to='media-images', null=True, blank=True)

    video = models.FileField(upload_to="videos/", null=True, blank=True)

    comments = models.ManyToManyField("Comment", related_name="comments", blank=True)
    public_id_image = models.CharField(max_length=100, null=-True)
    
    @property
    def get_num_comments(self):
        count = 0
        for x in self.comments.all():
            count += 1
        return count
    
    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/static/missing_post.jpg"

class Comment(models.Model):
    content = models.CharField(max_length=10000, null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="user",blank=True)
    likes = models.IntegerField(default=0,null=True,blank=True)



class DirectMessageChat(models.Model):
    messages = models.ManyToManyField("DirectMessage", related_name="messages", blank=True)
    initiated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="initiated_by",blank=True) # one user in chat
    to_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="to_user",blank=True) # other user in chat

class DirectMessage(models.Model):
    sent_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="sent_by",blank=True)
    chat = models.ForeignKey(DirectMessageChat,on_delete=models.SET_NULL,null=True, related_name="chat",blank=True)
    content =  models.CharField(max_length=10000, null=True)














