from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'FBForUs'

urlpatterns = [
    # 로그인, 로그아웃, 회원가입
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # 축구소식
    path('news_create/', views.news_create, name='news_create'),
    path('newslist/', views.news_list, name='news_list'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),

    # 마이페이지
    path('userlist/', views.user_list, name='user_list'),
    path('userlist/delete/<int:news_id>/', views.user_delete, name='user_delete'),

    # 축구소식 검색
    path('search/', views.news_search, name='news_search'),

    # 축구소식 수정, 삭제
    path('news/modify/<int:news_id>/', views.news_modify, name='news_modify'),
    path('news/delete/<int:news_id>/', views.news_delete, name='news_delete'),


    # 축구소식 댓글
    path('comment/create/<int:news_id>/', views.comment_create, name='comment_create'),

    # 축구소식 댓글 수정, 삭제
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),

    # 대댓글
    path('reply/create/<int:comment_id>/', views.reply_create, name='reply_create'),

    # 대댓글 수정, 삭제
    path('reply/modify/<int:reply_id>/', views.reply_modify, name='reply_modify'),
    path('reply/delete/<int:reply_id>/', views.reply_delete, name='reply_delete'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
