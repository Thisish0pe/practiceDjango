from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy

### Post
class List(View):
    def get(self, request):
        post_objs = Post.objects.all()
        context = {
            "posts" : post_objs
        }
        return render(request, 'blog/post_list.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        context = {
            "post" : post
        }
        return render(request, 'blog/post_detail.html', context)


# class Write(View):
#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data ['title']
#             content = form.cleaned_data['content']
#             post = Post.objects.create (title=title, content=content)
#             return redirect('blog:list')


class Write(CreateView):
    model = Post # 모델 
    form_class = PostForm # 어떤 폼을 사용할꺼야?
    success_url = reverse_lazy('blog:list')


class Update(View):
    def post(self, request):
        fields = ['title', 'content']

    def get_initial(self):
        initial = super().get_initial()

