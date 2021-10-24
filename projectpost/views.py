from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import UserModel, bookModels, readBooksModels, postModels, languagesModels, junresModels
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginOrSignupView(request):
    if request.method == "POST":
        # htmlのformの中のbuttonのname
        if "login" in request.POST:
            return redirect('login')
        elif "signup" in request.POST:
            return redirect('signup')
    else:
        return render(request, 'loginOrSignup.html', {})


def loginView(request):
    if request.method == "POST":
        if "login" in request.POST:
            mailaddress_data = request.POST.get('mailaddress_data')
            password_data = request.POST.get('password_data')
            user = authenticate(username=mailaddress_data, password=password_data)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url is None:
                    return redirect('profile') ###################################### login後どこに行くか
                else:
                    return redirect(next_url)
            else:
                return render(request, 'login.html', {'error': 'ユーザー名またはパスワードを確認してください'})
    else:
        return render(request, 'login.html', {})


def signupView(request):
    if request.method == 'POST':
        if "signup" in request.POST:
            mailaddress_data = request.POST.get('mailaddress_data')
            password_data = request.POST.get('password_data')

            try:
                User.objects.create_user(mailaddress_data, '', password_data)
                user = authenticate(request, username=mailaddress_data, password=password_data)
                login(request, user)
                object = UserModel.objects.create(user=user)
                object.save()
                return redirect('loginOrSignup') ################################################################ login後どこに行くか
            except IntegrityError:
                return render(request, 'signup.html', {'error': 'このmailは既に使われています'})
    else:
        return render(request, 'signup.html', {})


def profileView(request, pk=0):
    if pk > 0:
        profile = UserModel.objects.get(pk=pk)
        languages = list(profile.languages.split())
        junres = list(profile.junres.split())
        return render(request, 'profile.html', {"profile": profile, "languages": languages, "junres": junres})
    elif request.user.is_authenticated:
        profile = UserModel.objects.get(user=request.user)
        languages = list(profile.languages.split())
        junres = list(profile.junres.split())
        return render(request, 'profile.html', {"profile": profile, "languages": languages, "junres": junres, "set_profile": "ok"})
    else:
        print("ERROR")


@login_required
def setProfileView(request, pk):
    if request.method == 'POST':
        data = dict(request.POST)
        profile = UserModel.objects.get(pk=pk)
        # 登録
        image = request.FILES.get('image')
        if image is not None:
            profile.image = image
        if 'bio' in data:
            profile.bio = data["bio"][0]
        if 'language' in data:
            profile.languages = ""
            for language in data["language"]:
                profile.languages += language + ' '
        if 'junre' in data:
            profile.junres = ""
            for junre in data["junre"]: 
                profile.junres += junre + ' '
        profile.save()
        return redirect('profile')
    else:
        # pkとログインユーザーが一致しているか
        profile = UserModel.objects.get(pk=pk)
        if profile.user == request.user:
            languages = list(str(languagesModels.objects.get().language).split())
            junres = list(str(junresModels.objects.get().junres).split())
            return render(request, 'setProfile.html', {'profile': profile, 'languages': languages, 'junres': junres})
        else:
            return redirect('loginOrSignUp')