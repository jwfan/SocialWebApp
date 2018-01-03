# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
# Used to create and manually log in a user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.http import Http404, HttpResponse, JsonResponse
# Helper function to guess a MIME type from a file name
from mimetypes import guess_type
import random, json
from django.template.loader import render_to_string
from django.core.serializers import serialize

from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

# Create your views here.
from grumblr.models import *
from grumblr.forms import *


# Action for the default home page after logged-in.
@login_required
def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    followingposts = []
    for f in request.user.profile.follower.all():
        for post in Post.objects.filter(user=f):
            followingposts.append(post)
    followingposts = sorted(followingposts, key=lambda post: post.timestamp, reverse=True)

    if len(User.objects.all()) < 3:
        userlist1 = User.objects.all()
        userlist2 = {}
    else:
        userlist1 = random.sample(list(User.objects.all()), 3)
        userlist2 = random.sample(list(User.objects.all()), 3)

    context = {'postform': PostForm(), 'commentform': CommentForm(),
               'posts': posts, 'followingposts': followingposts, 'userlist1': userlist1,
               'userlist2': userlist2, 'userp': request.user}
    return render(request, 'grumblr/Globalstream.html', context)


# Action when people click register button.
@transaction.atomic
def register(request):
    context = {}

    if request.method == "GET":
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/Registration.html', context)

    form = RegistrationForm(request.POST)

    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/Registration.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['firstname'],
                                        last_name=form.cleaned_data['lastname'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        is_active=False
                                        )
    new_user.save()
    Profile(user=new_user).save()
    uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
    token = default_token_generator.make_token(new_user)
    email_body = """Welcome to Grumblr! Please click the link below to verify you 
    email address and complete the registration of your account:
    
    http://%s%s
    """ % (request.get_host(),
           reverse('confirm-email', args=(uidb64, token)))

    send_mail(subject="Verify your email address in Grumblr",
              message=email_body,
              from_email="oreoztl@gmail.com",
              recipient_list=[new_user.email])
    context['email'] = form.cleaned_data['email']
    return render(request, 'registration/needemailvalidation.html', context)


@transaction.atomic
def registeration_confirm(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=uid)[0]
    # Verify if input uidb64 corresponds to a existed user
    if not user:
        return render(request, 'grumblr/templates/registration/needemailvalidation.html', {})
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('index'))
    else:
        return render(request, 'grumblr/templates/registration/needemailvalidation.html', {})


@login_required
@transaction.atomic
def newpost(request):
    if request.method == "GET":
        return redirect(reverse('index'))
    new_post = Post(user=request.user)
    form = PostForm(request.POST, instance=new_post)
    if not form.is_valid():
        return redirect(reverse('index'))
    form.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def newcomment(request):
    if request.method == "GET":
        return redirect(reverse('index'))
    post = Post.get_from_id(request.POST['post_id'])
    new_comment = Comment(user=request.user, post=post)
    form = CommentForm(request.POST, instance=new_comment)
    if not form.is_valid() or post is None:
        raise Http404
    form.save()
    return HttpResponse("")


@login_required
def profile(request, username):
    # verify the input username
    if not username or not User.objects.filter(username=username).exists():
        raise Http404
    un = User.objects.get(username=username)
    posts = Post.get_posts(user=un)
    context = {'userp': un, 'posts': posts}
    return render(request, 'grumblr/Profile.html', context)


@login_required
def getprofileimage(request, username):
    user = request.user
    # verify the input username
    if username and User.objects.filter(username=username).exists():
        user = User.objects.filter(username__exact=username)[0]
    profile = get_object_or_404(Profile, user=user)
    if not profile.image:
        raise Http404
    content_type = guess_type(profile.image.name)
    return HttpResponse(profile.image, content_type=content_type)


@login_required
@transaction.atomic
def editprofile(request):
    context = {}
    context['userp'] = request.user
    un = request.user.username
    if request.method == "GET":
        form1 = UserForm(username=un)
        profile = Profile.objects.get(user=request.user)
        form2 = ProfileForm(instance=profile)
        context['userform'] = form1
        context['profileform'] = form2
        return render(request, 'grumblr/EditProfile.html', context)

    # Users do not need to enter every field in the form at a time.
    # Only fields filled by user should be save.
    # Fields could be empty and this is not invalid.

    new_profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=new_profile)
    if not form.is_valid():
        return redirect(reverse('editprofile'))
    form.save()
    return redirect(reverse('editprofile'))


@login_required
@transaction.atomic
def edituser(request):
    context = {}
    context['userp'] = request.user
    un = request.user.username
    if request.method == "GET":
        form1 = UserForm(username=un)
        profile = Profile.objects.get(user=request.user)
        form2 = ProfileForm(instance=profile)
        context['userform'] = form1
        context['profileform'] = form2
        return render(request, 'grumblr/EditProfile.html', context)

    form = UserForm(request.POST, username=un)
    if not form.is_valid():
        context['userform'] = form
        profile = Profile.objects.get(user=request.user)
        form2 = ProfileForm(instance=profile)
        context['profileform'] = form2
        return render(request, 'grumblr/EditProfile.html', context)

    # Users do not need to enter every field in the form at a time.
    # Only fields filled by user should be save.
    # Fields could be empty and this is not invalid.

    form.save()
    return redirect(reverse('edituser'))


@login_required
@transaction.atomic
def follow_unfollow(request):
    # verify the input username
    objectusername = request.POST.get('object')
    if not objectusername or not User.objects.filter(username=objectusername).exists():
        raise Http404()
    objectuser = User.objects.get(username=objectusername)
    if request.user.profile.follower.filter(username=objectusername):
        try:
            request.user.profile.follower.remove(objectuser)
        except ValueError:
            raise Http404()
    else:
        try:
            request.user.profile.follower.add(objectuser)
        except ValueError:
            raise Http404()
    return redirect(reverse('profile', args=[objectusername]))


@login_required
@transaction.atomic
def get_changes(request, time="1970-01-01 00:00:00.000000+00:00"):
    if not re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}').match(time):
        raise Http404
    max_time = Post.get_max_time()
    posts = Post.get_changes(time)
    return_json = {}
    return_post = []
    for post in posts:
        # return_post.append(render_to_string('grumblr/postdiv.html',{'post':post,'commentform':CommentForm()}))
        postjson = {}
        postjson['username'] = post.user.username
        postjson['content'] = post.content
        postjson['timestamp'] = post.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        postjson['profilehref'] = reverse('profile', args=[post.user.username])
        postjson['imagehref'] = reverse('getimage', args=[post.user.username])
        postjson['form'] = render_to_string('grumblr/postdiv.html', {'commentform': CommentForm()})
        postjson['id'] = post.id
        return_post.append(postjson)
    return_json["posts"] = return_post
    return_json["max_time"] = str(max_time)
    return JsonResponse(return_json)


@login_required
@transaction.atomic
def get_followchanges(request, time="1970-01-01 00:00:00.000000+00:00"):
    if not re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}').match(time):
        raise Http404
    max_time = Post.get_max_time()
    posts = Post.get_followchanges(request.user,time)

    return_json = {}
    return_post = []
    for post in posts:
        # return_post.append(render_to_string('grumblr/postdiv.html',{'post':post,'commentform':CommentForm()}))
        postjson = {}
        postjson['username'] = post.user.username
        postjson['content'] = post.content
        postjson['timestamp'] = post.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        postjson['profilehref'] = reverse('profile', args=[post.user.username])
        postjson['imagehref'] = reverse('getimage', args=[post.user.username])
        postjson['form'] = render_to_string('grumblr/postdiv.html', {'commentform': CommentForm()})
        postjson['id'] = post.id
        return_post.append(postjson)
    return_json["posts"] = return_post
    return_json["max_time"] = str(max_time)
    return JsonResponse(return_json)


@login_required
@transaction.atomic
def get_comments(request, time="1970-01-01 00:00:00.000000+00:00"):
    if not re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}').match(time):
        raise Http404
    max_time = Comment.get_max_time()
    comments = Comment.get_changes(time)
    return_json = {}
    return_comment = []
    for comment in comments:
        commentjson = {}
        commentjson['username'] = comment.user.username
        commentjson['content'] = comment.content
        commentjson['timestamp'] = comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        commentjson['profilehref'] = reverse('profile', args=[comment.user.username])
        commentjson['imagehref'] = reverse('getimage', args=[comment.user.username])
        commentjson['postid'] = comment.post.id
        return_comment.append(commentjson)
    return_json["comments"] = return_comment
    return_json["max_commenttime"] = str(max_time)
    return JsonResponse(return_json)

@login_required
@transaction.atomic
def get_followcomments(request, time="1970-01-01 00:00:00.000000+00:00"):
    if not re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}').match(time):
        raise Http404
    max_time = Comment.get_max_time()
    posts=Post.get_followchanges(request.user,time)
    comments = Comment.get_followchanges(posts,time)
    return_json = {}
    return_comment = []
    for comment in comments:
        commentjson = {}
        commentjson['username'] = comment.user.username
        commentjson['content'] = comment.content
        commentjson['timestamp'] = comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        commentjson['profilehref'] = reverse('profile', args=[comment.user.username])
        commentjson['imagehref'] = reverse('getimage', args=[comment.user.username])
        commentjson['postid'] = comment.post.id
        return_comment.append(commentjson)
    return_json["comments"] = return_comment
    return_json["max_commenttime"] = str(max_time)
    return JsonResponse(return_json)
