from django import forms
from .models import News, Comment, Reply

class RegisterForm(forms.Form) :
    email = forms.EmailField(label='이메일', error_messages={'invalid' : '유효한 이메일 주소를 입력해주세요.'})
    password = forms.CharField(label='비밀번호', min_length=6, max_length=20, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='비밀번호 확인', min_length=6, max_length=20, widget=forms.PasswordInput)
    fullname = forms.CharField(label='이름', min_length=2, max_length=5)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm :
            raise forms.ValidationError({
                "password_confirm" : ["2개의 비밀번호가 일치하지 않습니다."]
            })

        return cleaned_data
    #clean 함수의 return 값은 무조건 cleaned_data를 꼭 해줘야함

class LoginForm(forms.Form) :
    email = forms.EmailField(label='이메일', error_messages={'invalid': '유효한 이메일 주소를 입력해주세요.'})
    password = forms.CharField(label='비밀번호', min_length=6, max_length=20, widget=forms.PasswordInput,
                               error_messages={'invalid':'비밀번호가 일치하지 않습니다.'})

class NewsForm(forms.ModelForm) :
    class Meta :
        model = News
        fields = ['title', 'content_image', 'content']
        labels = {
            'title' : '제목',
            'content' : '내용',
            'content_image' : '소식 첨부파일'
        }

class CommentForm(forms.ModelForm) :
    class Meta :
        model = Comment
        fields = ['content']
        labels = {
            'content' : '댓글 내용'
        }

class ReplyForm(forms.ModelForm) :
    class Meta :
        model = Reply
        fields = ['content']
        labels = {
            'content' : '대댓글 내용'
        }
