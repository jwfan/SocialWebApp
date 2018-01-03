from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import grumblr.views

urlpatterns = [
    url(r'^$', grumblr.views.index, name='index'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^profile/(?P<username>.*?)$', grumblr.views.profile, name='profile'),
    url(r'^newpost$', grumblr.views.newpost, name='newpost'),
    url(r'^newcomment$', grumblr.views.newcomment, name='newcomment'),
    url(r'^editprofile', grumblr.views.editprofile, name='editprofile'),
    url(r'^edituser', grumblr.views.edituser, name='edituser'),
    url(r'^login$', auth_views.LoginView.as_view(template_name='grumblr/Login.html'), name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^profileimage/(?P<username>.*?)$',grumblr.views.getprofileimage,name='getimage'),
    url(r'^validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', grumblr.views.registeration_confirm, name='confirm-email'),
    url(r'^password/reset/$',auth_views.password_reset,{'post_reset_redirect':'resetdone'},name="password_reset"),
    url(r'^password/reset/done/$',auth_views.password_reset_done,name='resetdone'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm,{'post_reset_redirect':'resetcomplete'},name='reset-confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,name='resetcomplete'),
    url(r'^follow_unfollow/', grumblr.views.follow_unfollow,name='follow_unfollow'),
    url(r'^get-changes/(?P<time>.*?)$',grumblr.views.get_changes,name='get-changes'),
    url(r'^get-followchanges/(?P<time>.*?)$',grumblr.views.get_followchanges,name='get-followchanges'),
    url(r'^get-comments/(?P<time>.*?)$', grumblr.views.get_comments, name='get-comments'),
    url(r'^get-followcomments/(?P<time>.*?)$', grumblr.views.get_comments, name='get-comments'),
    url(r'^.*?$', auth_views.LoginView.as_view(template_name='grumblr/Login.html'))

]
