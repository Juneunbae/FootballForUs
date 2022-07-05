from django.db import models
from django.contrib.auth.models import User

class News(models.Model) :
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_news')
    title = models.CharField(max_length=100, null=False)
    content_image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    content = models.TextField(null=False)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model) :
    news = models.ForeignKey(News, null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.content

class Reply(models.Model) :
    comment = models.ForeignKey(Comment, null=True, blank= True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '댓글 {}의 대댓글 :{}'.format(self.comment, self.content)
