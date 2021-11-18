from django.urls import path
from . import views

urlpatterns = [
    path('user', views.user, name="user"),
    path('user-signup', views.userSignup, name="user-signup"),
    path('login', views.userLogin, name="login"),
    path('request-consult', views.requestConsult, name="request-consult"),
    path('request-quote', views.requestQuote, name="request-quote"),
    path('request-proposal', views.requestProposal, name="get-proposal"),
    path('get-quote', views.getQuote, name="get-quote"),
    path('get-proposal', views.getProposal, name="get-proposal"),
    path('upload-image', views.uploadImage, name="upload"),
    path('feedback', views.feedback, name="feedback"),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('check-active/<str:email>/<str:token>', views.checkActive, name="check-active"),
    path('set-password', views.setPassword, name="set-password"),
    path('profile-update', views.profileUpdate, name="profile-update"),
]
