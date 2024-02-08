from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author_name = models.CharField(max_length=50)
    publish_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
