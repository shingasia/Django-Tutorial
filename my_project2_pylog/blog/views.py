from django.shortcuts import render
from blog.models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all() # 각 인덱스에 blog.models.Post타입의 객체들이 들어있는 QuerySet
    
    context = {
        "posts" : posts,
    }
    return render(request, '../templates/posts/post_list.html', context)

