from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(autor=self).aggregate(result=Sum('rating')).get('result')
        comments_rating = Comment.objects.filter(user=self.user).aggregate(result=Sum('rating')).get('result')
        comment_post = Comment.objects.filter(post__autor__user=self.user).aggregate(result=Sum('rating')).get('result')

        self.rating = 3 * posts_rating + comments_rating + comment_post
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    news = 'NW'
    arcticle = 'AR'

    TYPE = [
        (news, 'Новость'),
        (arcticle, 'Статья')
    ]

    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,
                                 choices=TYPE,
                                 default=arcticle)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, length=124):
        return f"{self.text[:length]}..." if len(self.text) > length else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()