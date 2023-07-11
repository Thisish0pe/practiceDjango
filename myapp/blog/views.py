from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm

### Post
class List(View):
    def get(self, request):
        post_objs = Post.objects.all()
        context = {
            "title": "Blog_alone",
            "posts": post_objs
        }
        return render(request, 'blog/post_list.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        hashtags = HashTag.objects.filter(post=post)
        comment_form = CommentForm()
        hashtag_form = HashTagForm()

        context = {
            "title": "Blog_alone",
            "post": post,
            "comments": comments,
            "hashtags": hashtags,
            "comment_form": comment_form,
            "hashtag_form": hashtag_form,
        }
        return render(request, 'blog/post_detail.html', context)


class Write(View):
    def get(self, request):
        form = PostForm()
        context = {
            "title": "Blog_alone",
            "form": form
        }
        return render(request, 'blog/post_form.html', context)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data ['title']
            content = form.cleaned_data['content']
            post = Post.objects.create (title=title, content=content)
            return redirect('blog:list')


class Update(View):
    def get(self, request, pk): # pk = post_id
        #get은 에러 발생 가능성 높기 때문에 방지해야함
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        #수정이기 때문에 기존의 글이 작성되어 있는 상태로 화면에 렌더링 되어야 함
        form = PostForm(initial={'title': post.title, 'content': post.content})
        context = {
            "title": "Blog_alone",
            "form": form,
            "post": post,
        }
        return render(request, 'blog/post_edit.html', context)

    def post(self, request, pk): # pk = post_id
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post dose not exist.', str(e))
        
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:detail', pk=pk)
        context = {
            "title": "Blog_alone",
            "form": form,
        }
        return render(request, 'blog/post_edit.html', context)
    

class Delete(View):
    def post(self, request, pk): # pk=post_id
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist', str(e))

        post.delete()
        return redirect('blog:list')
    

### Comment
class CommentWrite(View):
    # DetailView 에서 화면 렌더링이 되기 때문에 get 필요없음
    def post(self, request, pk): # post_id
        form = CommentForm(request.POST)
        # 댓글에 해당하는 게시글 가져오기
        try:
            post = Post.objects.get (pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist', str(e))

        if form.is_valid():
            content = form.cleaned_data['content']
            try:
                comment = Comment.objects.create(post=post, content=content)
            except ObjectDoesNotExist as e:
                print('Post does not exist', str(e))

            except ValidationError as e:
                print('validation error occurred.', str(e))

            return redirect('blog:detail', pk=pk)
        
        hashtag_form = HashTagForm()
        context = {
            "title": "Blog_alone",
            "post": post,
            "comments": post.comment_set.all(),
            "hashtags": post.hashtag_set.all(),
            "comment_form": form,
            "hashtag_form": form
        }
        return render(request, 'blog/post_detail.html', context)


class CommentDelete(View):
    def post(self, request, pk): # pk=comment_id
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist as e :
            print('Post does not exist', str(e))
        
        post_id = comment.post.id # 역참조
        comment.delete()
        return redirect ('blog:detail', pk=post_id)
    

### Hashtag
class HashTagWrite(View):
    def post(self, request, pk): # post_id
        form = HashTagForm(request.POST)
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist', str(e))
        
        if form.is_valid ():
            name = form.cleaned_data['name']
            try:
                hashtag = HashTag.objects.create(post=post, name=name)
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))

            except ValidationError as e:
                print('Validation error occurred', str(e))
            
            return redirect('blog:detail', pk=pk)
        
        comment_form = CommentForm()
        context = {
            "title":"Blog_alone",
            "post": post,
            "comments": post.comment_set.all(),
            "hashtags": post.hashtag_set.all(),
            "comment_form": comment_form,
            "hahstag_form": form,
        }
        return render(request, 'blog/post_detail.html', context)
    

class HashTagDelete(View):
    def post(self, request, pk): # pk=comment_id
        try:
            hashtag = HashTag.objects.get(pk=pk)
        except ObjectDoesNotExist as e :
            print('Post does not exist', str(e))
        
        post_id = hashtag.post.id # 역참조
        hashtag.delete()
        return redirect ('blog:detail', pk=post_id)

