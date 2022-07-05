from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from .forms import LoginForm, RegisterForm, NewsForm, CommentForm, ReplyForm
from django.utils import timezone
from django.contrib.auth.models import User #유저 데이터 저장을 위해 선언
from .models import News, Comment, Reply
from django.core.paginator import Paginator

#로그인, 로그아웃, 회원가입

def login(request) :
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=email, password=password)
            if user:
                auth.login(request, user)
                return redirect('FBForUs:news_list')
            else :
                messages.error(request, '아이디 또는 비밀번호가 틀렸습니다!')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'pages/login.html', context)

def logout(request) :
    auth.logout(request)
    return redirect('/FBForUs')

def signup(request) :
    if request.method == 'POST' :
        form = RegisterForm(request.POST)
        if form.is_valid() :
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, '사용 중인 아이디 입니다.')
                return render(request, 'pages/signup.html')
            else :
                User.objects.create_user(email, email, password)
                messages.success(request, '회원가입이 성공적으로 완료되었습니다!')
            return redirect('FBForUs:login')
    else :
        form = RegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'pages/signup.html', context)

# 축구 소식 news
def news_create(request) :
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            try :
                news.content_image = request.FILES["content_image"]
            except :
                pass
            news.create_date = timezone.now()
            news.author = request.user
            news.save()
            return redirect('FBForUs:news_list')
    else:
        form = NewsForm()
    context = {
        'form': form
    }
    return render(request, 'pages/news_create.html', context)

def news_modify(request, news_id) :
    news = get_object_or_404(News, pk=news_id)
    if request.method == "POST" :
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid() :
            news = form.save(commit=False)
            news.author = request.user
            news.modify_date = timezone.now()
            try :
                news.content_image = request.FILES["content_image"]
            except :
                pass
            news.save()
            return redirect('FBForUs:news_detail', news_id=news.id)
    else :
        form = NewsForm(instance=news)
    context = {
        'form' : form
    }
    return render(request, 'pages/news_create.html', context)

def news_delete(request, news_id) :
    news = News.objects.get(id=news_id)
    news.delete()
    return redirect('FBForUs:news_list')

max_list_count = 12
max_page_count = 3

def news_list(request) :
    page = request.GET.get('page', 1)
    news_list = News.objects.order_by('-create_date')
    paginator = Paginator(news_list, max_list_count)
    page_obj = paginator.get_page(page)

    # 전체 페이지 마지막 번호
    last_page_num = 0

    for last_page in paginator.page_range:
        last_page = last_page_num + 1

    # 현재 페이지가 몇번째 블럭인지
    current_block = (( int(page) - 1 ) / max_page_count ) + 1
    current_block = int(current_block)

    # 페이지 시작번호
    page_start_number = ((current_block - 1) * max_page_count) + 1

    # 페이지 끝 번호
    page_end_number = page_start_number + max_page_count - 1

    context = {
        'news_list' : page_obj,
        'last_page_num' : last_page_num,
        'page_start_number' : page_start_number,
        'page_end_number' : page_end_number
    }
    return render(request, 'pages/news_list.html', context)

def user_list(request) :
    page = request.GET.get('page', 1)
    news_list = News.objects.order_by('-create_date')
    paginator = Paginator(news_list, max_list_count)
    page_obj = paginator.get_page(page)

    # 전체 페이지 마지막 번호
    last_page_num = 0

    for last_page in paginator.page_range:
        last_page = last_page_num + 1

    # 현재 페이지가 몇번째 블럭인지
    current_block = ((int(page) - 1) / max_page_count) + 1
    current_block = int(current_block)

    # 페이지 시작번호
    page_start_number = ((current_block - 1) * max_page_count) + 1

    # 페이지 끝 번호
    page_end_number = page_start_number + max_page_count - 1

    context = {
        'news_list': page_obj,
        'last_page_num': last_page_num,
        'page_start_number': page_start_number,
        'page_end_number': page_end_number
    }
    return render(request, 'pages/user_list.html', context)

def user_delete(request, news_id) :
    news = News.objects.get(id=news_id)
    news.delete()
    return redirect('FBForUs:user_list')

def news_search(request) :
    news = News.objects.all().order_by('-create_date')
    q = request.POST.get('q', '')

    if q:
        news = news.filter(title__icontains=q)
        return render(request, 'pages/news_search.html', {'news': news, 'q': q})

    else:
        return render(request, 'pages/news_search.html')

def news_detail(request, news_id) :
    # news = News.objects.get(id=news_id)
    news =  get_object_or_404(News, pk=news_id)
    try :
        news.content_image = request.FILES["news.content_image"]
        context = {'news': news, 'news.content_image': news.content_image}
    except :
        pass
        context = { 'news' : news }
    return render(request, 'pages/news_detail.html', context)

# 축구 소식 comment
def comment_create(request, news_id) :
    news = get_object_or_404(News, pk=news_id)
    # news = News.objects.get(id=news_id)
    if request.method == "POST" :
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() :
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.news = news
            comment.save()
            return redirect('FBForUs:news_detail', news_id=news.id)
        else :
            messages.warning(request, '반드시 1글자 이상 기입해주세요.')
    else :
        comment_form = CommentForm()
    context = {
        'comment_form' : comment_form, 'news' : news
    }
    return render(request, 'pages/news_detail.html', context)

def comment_modify(request, comment_id) :
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST' :
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid() :
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('FBForUs:news_detail', news_id=comment.news.id)
    else :
        form = CommentForm(instance=comment)
    context = {
        'form' : form, 'comment' : comment
    }
    return render(request, 'pages/comment_modify.html', context)

def comment_delete(request, comment_id) :
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('FBForUs:news_detail', news_id=comment.news.id)

def reply_create(request, comment_id) :
    # news = get_object_or_404(News, pk=news_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    # comment = Comment.objects.get(id=comment_id)
    if request.method == "POST" :
        form = ReplyForm(request.POST)
        if form.is_valid() :
            reply = form.save(commit=False)
            reply.author = request.user
            reply.create_date = timezone.now()
            reply.comment = comment
            reply.save()
            return redirect('FBForUs:news_detail', news_id=reply.comment.news.id)
    else :
        form = ReplyForm()
    context = {
        'form' : form
    }
    return render(request, 'pages/reply_form.html', context)

def reply_modify(request, reply_id) :
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.method == "POST" :
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid() :
            reply = form.save(commit=False)
            reply.modify_date = timezone.now()
            reply.save()
            return redirect('FBForUs:news_detail', news_id = reply.comment.news.id)
    else :
        form = ReplyForm(instance=reply)
    context = {
        'form' : form
    }
    return render(request, 'pages/reply_form.html', context)

def reply_delete(request, reply_id) :
    reply = get_object_or_404(Reply, pk=reply_id)
    reply.delete()
    return redirect('FBForUs:news_detail', news_id = reply.comment.news.id)