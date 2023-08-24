from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("create-post/", views.create_post, name="create-post"),
    path("profile/<str:pk>", views.profile_page, name="view-profile"),
    path("view-post/<str:pk>", views.view_post, name="view-post"),
    path("direct-messages/", views.view_direct_messages, name="view-direct-messages"),
    path("direct-message-chat/<str:pk>", views.view_direct_message_chat, name="view-direct-message-chat"),
    path("logout/", views.logout_user, name="logout")
]



# path(string-typed-in-path, file-name.func-name-to-call-pass, name='func-name or url short name to access')
# Whenever "some-url-is-typed-in-path" it calls/passes the function in views
# Dynamic Urls: <data-type:name>