from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import UserModel, answerModel, bookModel, readBooksModel, questionModel, languagesModel, junresModel
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import time
from django.db.models import Q
from django.db.models import Sum
from django.core import serializers
import json

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
                user_object = UserModel.objects.create(user=user)
                return redirect('setProfile', user_object.pk) ################################################################ login後どこに行くか
            except IntegrityError:
                return render(request, 'signup.html', {'error': 'このmailは既に使われています'})
    else:
        return render(request, 'signup.html', {})


@login_required
def profileView(request, pk=0):
    if request.method == "POST":
        isbn = request.POST.get('isbn')
        return redirect('impressions', isbn)
    else:
        if pk == 0 or UserModel.objects.get(pk=pk).user == request.user:
            profile = UserModel.objects.get(user=request.user)
            read_book = readBooksModel.objects.filter(reader=profile)
            if profile.languages is None:
                languages = ""
            else:
                languages = list(profile.languages.split())
            if profile.junres is None:
                junres = ""
            else:
                junres = list(profile.junres.split())
            junre_loadmap = dict()
            language_loadmap = dict()
            for book in read_book:
                print(book.book.junre, book.book.language)
                if book.book.junre == "none":
                    pass
                elif book.book.junre in junre_loadmap:
                    junre_loadmap[book.book.junre].append(book)
                else:
                    junre_loadmap[book.book.junre] = [book]
                if book.book.language == "none":
                    pass
                elif book.book.language in language_loadmap:
                    language_loadmap[book.book.language].append(book)
                else:
                    language_loadmap[book.book.language] = [book]
            return render(request, 'profile.html', {"profile": profile, "languages": languages, "junres": junres, "read_book": read_book, "junre_loadmap": junre_loadmap, "language_loadmap": language_loadmap, "set_profile": "ok"})
        elif pk > 0:
            profile = UserModel.objects.get(pk=pk)
            read_book = readBooksModel.objects.filter(reader=profile)
            if profile.languages is None:
                languages = ""
            else:
                languages = list(profile.languages.split())
            if profile.junres is None:
                junres = ""
            else:
                junres = list(profile.junres.split())
            junre_loadmap = dict()
            language_loadmap = dict()
            for book in read_book:
                if book.book.junre == "none":
                    pass
                elif book.book.junre in junre_loadmap:
                    junre_loadmap[book.book.junre].append(book)
                else:
                    junre_loadmap[book.book.junre] = [book]
                if book.book.language == "none":
                    pass
                elif book.book.language in language_loadmap:
                    language_loadmap[book.book.language].append(book)
                else:
                    language_loadmap[book.book.language] = [book]

                return render(request, 'profile.html', {"profile": profile, "languages": languages, "junres": junres, "read_book": read_book, "junre_loadmap": junre_loadmap, "language_loadmap": language_loadmap})
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
        if 'name' in data:
            profile.name = data['name'][0]
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
            languages = list(str(languagesModel.objects.get().language).split())
            junres = list(str(junresModel.objects.get().junres).split())
            return render(request, 'setProfile.html', {'profile': profile, 'languages': languages, 'junres': junres})
        else:
            return redirect('loginOrSignUp')
    

@login_required
def setReadBookView(request):
    if request.method == 'POST':
        request_type = request.POST.get('type')
        if request_type == 'searchBookTitle':
            REQUEST_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
            APP_ID="1005734387313658318"
            serch_keyword = request.POST.get('bookTitle')

            serch_params = {
                "format" : "json",
                "title" : serch_keyword,
                "applicationId" : [APP_ID],
                "hits" : 10,
                "page" : 1
            }

            response = requests.get(REQUEST_URL, serch_params)
            result = response.json()

            books_data = {'titles':[], 'isbns':[], 'image_urls':[]}
            for item in result['Items']:
                books_data['titles'].append(item['Item']['title'])
                books_data['isbns'].append(item['Item']['isbn'])
                books_data['image_urls'].append(item['Item']['largeImageUrl'])

            time.sleep(1)
            return JsonResponse(books_data)
        else:
            # 本が選択されたされた
            ibsn = request.POST.get('selectBook')
            title = request.POST[ibsn+"_title"]
            imageUrl = request.POST[ibsn+"_imageUrl"]
            try:
                book_object = bookModel.objects.get(ibsn=ibsn)
            except ObjectDoesNotExist:
                # 登録されていない本
                return redirect('setBook', ibsn)
            return redirect('recordBook', ibsn)
    else:
        return render(request, 'searchBook.html', {})


@login_required
def setBookView(request, ibsn):
    if request.method == 'POST':
        language = request.POST.get('language')
        junre = request.POST.get('junre')
        title = request.POST.get('title')
        imageUrl = request.POST.get('imageUrl')
        try:
            book = bookModel.objects.get(ibsn=ibsn)
        except ObjectDoesNotExist:
            bookModel.objects.create(
                name = title,
                ibsn = ibsn,
                image = imageUrl,
                language = language,
                junre = junre
            )
        return redirect('recordBook', ibsn)
    else:
        REQUEST_URL = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
        APP_ID="1005734387313658318"

        serch_params = {
            "format" : "json",
            "isbn" : ibsn,
            "applicationId" : [APP_ID],
            "hits" : 1,
            "page" : 1
        }

        response = requests.get(REQUEST_URL, serch_params)
        result = response.json()

        title = result['Items'][0]['Item']['title']
        imageUrl = result['Items'][0]['Item']['largeImageUrl']
        languages = list(str(languagesModel.objects.get().language).split())
        junres = list(str(junresModel.objects.get().junres).split())
        return render(request, 'setBook.html', {'title': title, 'imageUrl': imageUrl, 'ibsn': ibsn, 'languages': languages, 'junres': junres})


@login_required
def recordBookView(request, isbn):
    if request.method == 'POST':
        thoughts = request.POST.get('thoughts')
        value = request.POST.get('value_value')
        lower_diff = request.POST.get('lower_diff_value')
        upper_diff = request.POST.get('upper_diff_value')
        reader = UserModel.objects.get(user=request.user)
        book = bookModel.objects.get(ibsn=isbn)
        try:
            read_book_object = readBooksModel.objects.get(reader=reader, book=book)
        except ObjectDoesNotExist:
            order_language = readBooksModel.objects.filter(reader=reader, book__language=book.language).count()
            order_junre = readBooksModel.objects.filter(reader=reader, book__junre=book.junre).count()
            readBooksModel.objects.create(
                reader = reader,
                book = book,
                thoughts = thoughts,
                value = value,
                lower_diff = lower_diff,
                upper_diff = upper_diff,
                order_language = order_language,
                order_junre = order_junre
            )
            
            lower = int(lower_diff)
            upper = int(upper_diff)
            if lower <= 1 <= upper:
                book.diff1 += 1
            if lower <= 2 <= upper:
                book.diff2 += 1
            if lower <= 3 <= upper:
                book.diff3 += 1
            if lower <= 4 <= upper:
                book.diff4 += 1
            if lower <= 5 <= upper:
                book.diff5 += 1
            book.save()
        return redirect('profile')
    else:
        book_objects = bookModel.objects.get(ibsn=isbn)
        title = book_objects.name
        image = book_objects.image
        language = book_objects.language
        junre = book_objects.junre
        return render(request, 'recordBook.html', {'title':title, 'image':image, 'language':language, 'junre':junre})
    

@login_required
def bookRankingView(request):
    if request.method == 'POST':
        request_type = request.POST.get('type')
        if request_type == 'booksSearch':
            returns = 20

            search_text = request.POST.get('search_text')
            lower_sample = int(request.POST.get('lower_sample'))
            diff = int(request.POST.get('diff'))
            candidate_books = bookModel.objects.filter(Q(language=search_text)|Q(junre=search_text))
            
            if len(candidate_books) == 0:
                return JsonResponse({"error": "選択された言語またはジャンルには本がありません"})

            candidate_books_dict = dict()
            diffs = [0,0,0,0,0,0]
            for candidate_book in candidate_books:
                sample = candidate_book.readBookOf.all().count()
                diffs[1] = candidate_book.diff1
                diffs[2] = candidate_book.diff2
                diffs[3] = candidate_book.diff3
                diffs[4] = candidate_book.diff4
                diffs[5] = candidate_book.diff5
                
                # diffの判定甘い
                if sample >= lower_sample and diffs[diff] > 0:
                    candidate_books_dict[candidate_book] = round(readBooksModel.objects.filter(book=candidate_book).aggregate(sum_value=Sum('value'))['sum_value']/sample, 1)
            
            candidate_books_dict = sorted(candidate_books_dict.items(), reverse=True,  key=lambda x:x[1])
            
            names, isbns, images, languages, junres, values, samples = [], [], [], [], [], [], []
            for (book, value) in candidate_books_dict[:returns]:
                names.append(book.name)
                isbns.append(book.ibsn)
                images.append(book.image)
                languages.append(book.language)
                junres.append(book.junre)
                values.append(value)
                samples.append(book.readBookOf.all().count())
            
            d = {"names": names, "isbns": isbns, "images": images, "languages": languages, "junres": junres,  "values": values, "samples": samples}
            return JsonResponse(d)
        else:
            isbn = request.POST.get('isbn')
            return redirect('impressions', isbn)
    else:
        languages = list(str(languagesModel.objects.get().language).split())
        junres = list(str(junresModel.objects.get().junres).split())
        return render(request, 'bookRanking.html', {"language_and_junre": languages + junres})


@login_required
def impressionsView(request, isbn):
    print(isbn)
    if request.method == "POST":
        if "jump_name_btn" in request.POST:
            return redirect('profile', pk=request.POST.get('jump_name_btn'))
        if "jump_img_btn" in request.POST:
            return redirect('profile', pk=request.POST.get('jump_img_btn'))
    else:
        book = bookModel.objects.get(ibsn=isbn)
        read_objects = readBooksModel.objects.filter(book=book)
        value1 = read_objects.filter(value=1).count()
        value2 = read_objects.filter(value=2).count()
        value3 = read_objects.filter(value=3).count()
        value4 = read_objects.filter(value=4).count()
        value5 = read_objects.filter(value=5).count()
        value = round((value1*1 + value2*2 + value3*3 + value4*4 + value5*5)/read_objects.count(), 1)
        count = read_objects.count()
        return render(request, 'impressions.html', {"book": book, "readers": read_objects, "count": count, "value": value, "value1": value1, "value2": value2, "value3": value3, "value4": value4, "value5": value5})


@login_required
def booksImpressionsView(request):
    if request.method == 'POST':
        if 'bookTitle' in request.POST:
            search_text = request.POST.get('bookTitle')
            books = bookModel.objects.filter(name__contains=search_text)
            if books.count() == 0:
                return JsonResponse({"error": "ヒットしませんでした. 登録されていない本の可能性があります"})
            elif books.count() > 9:
                return JsonResponse({"error": "候補が多すぎます"})
            else:
                names, ibsns, images, languages, junres, values, samples = [], [], [], [], [], [], []
                for book in books:
                    sample = book.readBookOf.all().count()
                    value = round(readBooksModel.objects.filter(book=book).aggregate(sum_value=Sum('value'))['sum_value']/sample, 1)
                    names.append(book.name)
                    ibsns.append(book.ibsn)
                    images.append(book.image)
                    languages.append(book.language)
                    junres.append(book.junre)
                    values.append(value)
                    samples.append(sample)
                return JsonResponse({"error": "", "names": names, "isbns": ibsns, "images": images, "languages": languages, "junres": junres, "values": values, "samples": samples})
        elif 'selectBook' in request.POST:
            isbn = request.POST.get('selectBook')
            return redirect('impressions', isbn)
        elif 'isbn' in request.POST:
            isbn = request.POST.get('isbn')
            return redirect('impressions', isbn)
    else:
        return render(request, 'booksImpressions.html')


@login_required
def questionRoomsView(request):
    if request.method == "POST":
        if 'select_language' in request.POST:
            room = request.POST.get('select_language')
        elif 'my_question' in request.POST:
            room = request.POST.get('my_question')
        return redirect('questions', room)
    else:
        languages = list(str(languagesModel.objects.get().language).split())
        return render(request, 'questionRooms.html', {"languages": languages})


@login_required
def questionsView(request, room):
    if request.method == 'POST':
        print(request.POST)
        if 'jump_img_btn' in request.POST:
            profile_pk = request.POST.get('jump_img_btn')
            return redirect('profile', profile_pk)
        elif 'QandA_room' in request.POST:
            question  = request.POST.get('QandA_room')
            return redirect('qAndARoom', question)
        elif 'post_user' in request.POST:
            post_user = UserModel.objects.get(pk=request.POST.get('post_user'))
            question = request.POST.get('question_text')
            questionModel.objects.create(
                profile = post_user,
                room = room,
                question = question
            )
            return redirect('questions', room)
    else:
        user = UserModel.objects.get(user=request.user)
        if room == 'my_question':
            questions = questionModel.objects.filter(profile=user).order_by('pk').reverse()
            room = user.name
        else:
            questions = questionModel.objects.filter(room=room).order_by('pk').reverse()
        return render(request, 'questions.html', {"room": room, "questions": questions, "post_user": user})


@login_required
def qAndARoomView(request, pk):
    if request.method == 'POST':
        print(request.POST)
        if 'jump_img_btn' in request.POST:
            profile_pk = request.POST.get('jump_img_btn')
            return redirect('profile', profile_pk)
        elif 'post_user' in request.POST:
            post_user_pk = request.POST.get('post_user')
            post_user = UserModel.objects.get(pk=post_user_pk)
            answer_text = request.POST.get('answer_text')
            question = questionModel.objects.get(pk=pk)
            answerModel.objects.create(
                profile = post_user,
                response_to = question,
                answer = answer_text
            )
            return redirect('qAndARoom', pk)
    else:
        question = questionModel.objects.get(pk=pk)
        user = UserModel.objects.get(user=request.user)
        answers = answerModel.objects.filter(response_to=question).order_by('pk')
        return render(request, 'qAndARoom.html', {"question": question, "post_user": user, "answers": answers})