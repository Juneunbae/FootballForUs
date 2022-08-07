# FootballForUs
축구 커뮤니티

```
축구에 대한 얘기를 할 수 있는 축구 커뮤니티 사이트입니다.
만든 이와 다른 다양한 축구 의견을 들으려 만들어졌습니다.
또, 가입 등급에 따라 글을 쓰거나 읽는 권한이 없어 누구나 회원가입과 로그인을 하시면, 자유롭게 소통할 수 있습니다.
```

간단한 기능 소개

* 회원가입
```
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
    
  1. 요청 방식이 POST이고, 회원가입 폼이 유효하다면
  2. email과 password cleaned data에 저장
  3. 만약 User 데이터에 중복 이메일이 있으면, 에러
  4. User 데이터에 중복 이메일이 존재하지 않으면 회원가입 성공
```
* 로그인
```
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
    
  1. 요청 방식이 POST이고, 로그인 폼이 유효하다면
  2. cleaned data에 email, password를 저장
  3. username과 password를 user에 넣어 검사하기
  4. 만약 유저이면 로그인
  5. 유저가 아닐 시, 에러처리
```
* 로그아웃
```
  def logout(request) :
    auth.logout(request)
    return redirect('/FBForUs')
    
  1. 로그아웃 요청 시, 로그아웃 처리
```
***
* 축구 소식
> News 모델은 author(글쓴이), title(제목), content(내용), content_image(글 사진), create_date(쓴 날짜), modify_date(수정 날짜)로 구성
```
  class News(models.Model) :
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_news')
   title = models.CharField(max_length=100, null=False)
   content_image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
   content = models.TextField()
   create_date = models.DateTimeField()
   modify_date = models.DateTimeField(null=True, blank=True)
   
  + author는 User모델을 외래 키로 받았으며, models.CASCADE를 사용함으로써, 글쓴이가 사라지면 쓴 글도 같이 사라지게 설정하였다.
  + title은 CharField를 통하여 제목을 받게 설정했으며, 제목이 비어있으면 안되므로, Null=False 설정을 주었다.
  + content_image는 ImageField를 통하여 설정하였는데, 사진이 없는 글도 작성할 수 있게 null 과 blank의 값을 True로 설정해주었다.
    그리고 사진이 업로드 될때 년/월/일 로 저장되게 upload_to 기능을 사용하였다.
  + content는 TextField로 글을 쓰는데 글 수의 제한이 없게 하기위해 TextField로 사용하였다.
  + create_date는 DateTimeField를 설정함으로써 글을 쓴 날짜를 입력받게 하였다.
  + modify_date는 create_date와 마찬가지로 설정하였지만, 수정하지 않은 글도 있을 수 있으므로, null과 blank값을 True로 설정해주었다.
```
 - 등록하기
 - 수정하기
 - 삭제하기
***
* 댓글 
> Comment 모델은 news(게시글), author(작성자), content(내용), create_date(쓴 날짜), modify_date(수정 날짜) 로 구성
```
  class Comment(models.Model) :
   news = models.ForeignKey(News, null=True, blank=True, on_delete=models.CASCADE)
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField()
   create_date = models.DateTimeField()
   modify_ date = models.DateTimeField(blank = True, null = True)
   
 + news는 News 의 외래키 즉, 댓글을 달 글의 외래키로 설정하였고, 댓글을 달지 않을 수 있으므로, null 과 blank를 True로 설정하였다.
  그리고 글이 없어지면 댓글도 같이 없어져야 하므로, models.CASCADE 조건을 달았다.
 + author는 회원가입-로그인 한 유저의 정보를 외래키로 받았으며, 작성자의 정보가 없어지면 작성자가 쓴 글도 없어져야 하므로 models.CASCADE 조건을 달았다.
 + content는 댓글의 글자 수 제한을 하지 않기위해 TextField로 받았다.
 + create_date 는 쓴 날짜이므로 DateTimeField로 받았다.
 + modify_date는 수정 날짜이므로 수정하지 않았을때도 생각해야 하므로, blank 와 null 값을 True로 받았다.
```
* 작성하기
* 수정하기
* 삭제하기
***
* 대댓글
> Reply 모델은 comment(댓글), author(작성자), content(내용), create_date(작성날짜), modify_date(수정날짜) 로 구성
```
  class Reply(models.Model) :
   comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.CharField(max_length=100)
   create_date = models.DateTimeField()
   modify_date = models.DateTimeField(blank=True, null=True)
   
  + comment는 댓글 Comment의 외래키이다. 댓글이 존재해야 대댓글을 쓸 수 있으므로, 댓글을 외래키로 설정하였다.
    그리고 댓글 데이터가 삭제될 시, 같이 삭제되기 위한 조건으로 models.CASCADE를 선언해주었다.
  + author는 작성자이므로, 회원가입-로그인에 성공한 유저를 외래키로 받았으며, 작성자의 정보가 없어지면 작성자가 쓴 글도 사라지게 하기위해 models.CASCADE를 선언해주었다.
  + comment는 대댓글의 내용이므로, 100자 이상 필요하다고 생각하지 않아서, TextField 대신 CharField를 선언해주었다.
  + create_date는 작성날짜이며, 날짜 데이터를 저장하기 위해 DateTimeField를 선언해주었다.
  + 마찬가지로 수정이 되었으면 수정날짜를 기록하기 위해 DateTimeField를 선언해주었으며, 수정이 되지 않았을 때를 대비해 blank와 null을 True로 선언해주었다.
```
  * 작성하기
  * 수정하기
  * 삭제하기

