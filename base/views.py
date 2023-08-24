from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import DirectMessage, DirectMessageChat, User, Post, Comment
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import cloudinary
import cloudinary.uploader
import re  # run pip freeze


def extract_hashtags(caption):
    hashtags = re.findall(r'#\w+', caption)
    return hashtags


def home(request):
    user = request.user
    #user.followers.clear()
    #user.following.clear()
    posts = Post.objects.all()
    if request.method == "POST":
        print(request.POST)
        if request.POST.get("follow") != None:
            user_to_follow = User.objects.get(id=int(request.POST.get("follow")))
            if user != user_to_follow:
                user.following.add(user_to_follow)
                user_to_follow.followers.add(user)
        if request.POST.get("like") != None: 
            post_to_like = Post.objects.get(id=int(request.POST.get("like")))
            if post_to_like in list(user.liked_posts.all()):  # if post is in the users liked-posts, dont update the posts likes
                post_to_like.likes -= 1
                user.liked_posts.remove(post_to_like)
                user.save()
                post_to_like.save()
                context = {"user":user, "posts":posts}
                return render(request, "base/home.html", context)
            else:  # else post is not in liked-posts so update posts likes
                post_to_like.likes += 1
                user.liked_posts.add(post_to_like)
                user.save()
                post_to_like.save()
        # For pop-up create-post form
        if request.method == 'POST':
            if request.user.is_authenticated == False:
                context = {"page_name":"create-post/", "message":"Unable to create post because you haven't logged into an account."}
                return render(request, "base/login_error.html", context)
            uploaded_image = request.FILES.get('image')
            if uploaded_image:
                caption = request.POST.get("text-content")
                # CLOUDINARY
                cloudinary_response = cloudinary.uploader.upload(uploaded_image, folder="media-images")
                public_id = cloudinary_response["public_id"]
                print("PUBLIC-ID: " + str(public_id))
                p1 = Post.objects.create(content=caption, posted_date=datetime.now(), author=user, varitey="image", public_id_image=public_id)
                p1.image = cloudinary_response['secure_url']
                # CLOUDINARY
                user.posts.add(p1)
                p1.save()
                user.save()
            else:
                caption = request.POST.get("text-content")
                p1 = Post.objects.create(content=caption, posted_date=datetime.now(), author=user, varitey="text")
                user.posts.add(p1)
                p1.save()
                user.save()

    context = {"user":user, "posts":posts}
    return render(request, "base/home.html", context)

def login_page(request):
    page = "login"        # passing in the type of page either login or register
    if request.method == "POST":   # request.POST = everytime form is submitted it posts a query-dict {"input-name":"text-typed-in-input"}
        email = request.POST.get("email").lower()   # request.post.get('input-name') = text-typed
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email, password=password)  # trying to extract user-obj where username-attribute=username-entered
        except:
            messages.error(request, "User does not exist!")  # if user-obj with that username does not exist flash error

        if user is not None:   # if that user exists
            print("redir")
            login(request, user)    # logins the user
            return redirect("home")
        else:
            print("user not found")
            messages.error(request, "Username or Password does not exist!")  # if user with that username/password does not exist flash message

    context = {"page":page}
    return render(request, "base/login_register.html", context)

def logout_user(request):
    if request.user.is_authenticated == True:
        logout(request)
        print("User has been logged out")
    return redirect("home")


def register_page(request):
    page = "register"
    if request.method == "POST":
        first = request.POST.get("first-name")
        last = request.POST.get("last-name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1").lower()
        password2 = request.POST.get("password2").lower()
        if "" not in [first, last, username, email, password1, password2]:
            user = User.objects.create(first_name=first, last_name=last, username=username, email=email, password=password1)
            user.save()
            login(request, user)
            print("Valid")
            return redirect("home")
        else:
            print("Not valid")

    context = {"page":page}
    return render(request, "base/login_register.html", context)


def profile_page(request, pk):
    if request.user.is_authenticated == False:
        context = {"page_name":"Profile Page at profile/<missing:id>", "message":"Currently do not have a profile because you haven't logged into an account"}
        return render(request, "base/login_error.html", context)

    current_user = request.user
    user = User.objects.get(id=pk) # user of the profile page cur-user is viewing
    followers = user.followers.all()
    following = user.following.all()
    liked_posts = user.liked_posts.all()

    is_user_profile = False
    if user.username == request.user.username:
        is_user_profile = True
    
    image_upload = request.FILES.get("upload", False) # default false, if upload input is not given
    if request.method == 'POST':
        print(request.POST)
        if "dm" in list(request.POST.keys()):
            found = False
            for dm_chat in user.direct_message_chats.all():
                if user == dm_chat.initiated_by or user == dm_chat.to_user:
                    found = True
                    context = {"user":current_user, "other":user, "messages":dm_chat.messages.all()}
                    return render(request, "base/view_dm.html", context)
            # else this dm-chat-obj has not been created
            if found == False:
                dmc = DirectMessageChat.objects.create(initiated_by=request.user, to_user=user) 
                request.user.direct_message_chats.add(dmc)
                user.direct_message_chats.add(dmc)
                request.user.save()
                user.save()
                dmc.save()
        # UPLOAD PROFILE PICTURE
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            # CLOUDINARY
            cloudinary_response = cloudinary.uploader.upload(uploaded_image, folder="media-images")
            public_id = cloudinary_response["public_id"]
            print("PUBLIC-ID: " + str(public_id))
            user.public_id_profile_image = public_id
            user.profile_pic = cloudinary_response['secure_url']
            # CLOUDINARY
            user.save()
        if "unfollow" in list(request.POST.keys()):
            user_to_unfollow = User.objects.get(id=int(request.POST.get("unfollow")))
            current_user.following.remove(user_to_unfollow)
            user_to_unfollow.followers.remove(current_user)
            user_to_unfollow.save()
            current_user.save()
        if "edit-firstname" in list(request.POST.keys()):
            user.first_name = request.POST.get("edit-firstname")
        if "edit-lastname" in list(request.POST.keys()):
            user.last_name = request.POST.get("edit-lastname")
        if "edit-username" in list(request.POST.keys()):
            user.username = request.POST.get("edit-username")
        if "edit-bio" in list(request.POST.keys()):
            user.biography = request.POST.get("edit-bio")
        if "edit-email" in list(request.POST.keys()):
            user.email = request.POST.get("edit-email")
        if "delete-post" in list(request.POST.keys()):
            post_to_del = user.posts.get(id=int(request.POST.get("delete-post")))
            if post_to_del.varitey == "image":
                # Use public_id_image attribute of post-obj to delete
                cloudinary.uploader.destroy(post_to_del.public_id_image)
            post_to_del.delete() # deletes all relationships
            user.save()

        if request.POST.get("like") != None: 
            post_to_like = Post.objects.get(id=int(request.POST.get("like")))
            if post_to_like in list(user.liked_posts.all()):  # if post is in the users liked-posts, dont update the posts likes
                post_to_like.likes -= 1
                user.liked_posts.remove(post_to_like)
                user.save()
                post_to_like.save()
                profile_posts = [] # posts that have author of as current profile page
                for post in Post.objects.all():
                    if post.author == user:
                        profile_posts.append(post)
                context = {"user":user, "is_user":is_user_profile, "followers":followers, "following":following, "liked_posts":liked_posts, "profile_posts":profile_posts}
                return render(request, "base/profile.html", context)
            else:  # else post is not in liked-posts so update posts likes
                post_to_like.likes += 1
                user.liked_posts.add(post_to_like)
                user.save()
                post_to_like.save()
        user.save() # not using cur-user because the only way a profile-page can be editted is if its that users profile

    profile_posts = [] # posts that have author of as current profile page
    for post in Post.objects.all():
        if post.author == user:
            profile_posts.append(post)
    context = {"user":user, "is_user":is_user_profile, "followers":followers, "following":following, "liked_posts":liked_posts, "profile_posts":profile_posts}
    return render(request, "base/profile.html", context)


def create_post(request):
    if request.user.is_authenticated == False:
        context = {"page_name":"create-post/", "message":"Unable to create post because you haven't logged into an account."}
        return render(request, "base/login_error.html", context)

    user = request.user

    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            caption = request.POST.get("text-content")
            # CLOUDINARY
            cloudinary_response = cloudinary.uploader.upload(uploaded_image, folder="media-images")
            public_id = cloudinary_response["public_id"]
            p1 = Post.objects.create(content=caption, posted_date=datetime.now(), author=user, varitey="image", public_id_image=public_id)
            p1.image = cloudinary_response['secure_url']
            # CLOUDINARY
            user.posts.add(p1)
            p1.save()
            user.save()
        else:
            caption = request.POST.get("text-content")
            p1 = Post.objects.create(content=caption, posted_date=datetime.now(), author=user, varitey="text")
            user.posts.add(p1)
            p1.save()
            user.save()
    
    context = {"user":user}
    return render(request, "base/create_post.html", context)


def view_post(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        if request.user.is_authenticated == False:
            context = {"page_name":"View Posts at view-post/"+str(pk), "message":"Cannot comment on this post until you have logged in!"}
            return render(request, "base/login_error.html", context)
        caption = request.POST.get("comment-content")
        comment = Comment.objects.create(content=caption, user=user)
        post.comments.add(comment)
        comment.save()
        post.save()
    comments = post.comments
    context = {"post":post, "comments":comments.all()}
    return render(request, "base/view_post.html", context)


def view_direct_messages(request):
    if request.user.is_authenticated == False:
        context = {"page_name":"View Direct Messages at direct-messages/", "message":"Cannot your direct message chats because you haven't logged."}
        return render(request, "base/login_error.html", context)

    user = request.user
    dms = user.direct_message_chats.all()
    messages = []

    context = {"user":user, "dms":dms}
    return render(request, "base/direct_messages.html", context)

def view_direct_message_chat(request, pk):
    user = request.user # current-user
    dm_chat = DirectMessageChat.objects.get(id=pk) # extract DirectMessageChat-obj using url-id
    messages = dm_chat.messages.all() # get all DirectMessageChat from message-many field in DirectMessageChat-obj
    if user ==dm_chat.to_user:
        other = dm_chat.initiated_by
    elif user != dm_chat.to_user:
        other = dm_chat.to_user

    if request.method == "POST":
        message = DirectMessage.objects.create(chat=dm_chat, sent_by=user, content=request.POST.get("msg-content"))
        dm_chat.messages.add(message)

        dm_chat.save()
        message.save()
    context = {"user":user, "other":other, "messages":messages, "chats":user.direct_message_chats.all(), "current_chat":list(user.direct_message_chats.all())[0]}
    return render(request, "base/view_dm.html", context)



# FINISHED:
# DONE: Create current user profile at left side of navbar. 
# DONE: Delete post button on current users profile page under posts tab.
# DONE: Style dm button on user profile page
# DONE: when first time user with no account tries to access certain pages, error shows
# DONE: Logout link/button.
# DONE: add virtual environment for requirements.txt
# DONE: Static/media files not rendering. Start new project python3 manage.py collecticstatic and confiure whitenoise. For media files configure 
# cloudinary. Test in development and make sure everything is working if it is deploy!

# BUGS/ERRORS:


# FEATURES/IMRPOVEMENTS:
# TODO: Topics model created through hashtags. And each post has a list of topcs. 
# TODO: Search functionality by user, post content, hashtags.
# TODO: Bug reporting page.
# TODO: Credits page. Display number of users.
# TODO: Clean up login/register page,
# TODO: Search functionality for different categories users, posts, hashtags.
# TODO: User is verfied when someone follows them, unfollows them, likes/comments on post, uses their hashtag. 
# TODO: Style following/followers tabs on profile page


# NOTE: PostgreSQL database will expire on render on Nov.21. 
# -Make sure cloudinary amount of assests are under control.
# -Cannot deploy multiple apps on free tier on render, so try creating multiple accounts.
# -When this website gets taken down by render have to reconfigure settings so you can run it locally.