from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views import View
from django.urls import reverse_lazy
from .models import Post,Comment,Fav
from .owner import OwnerListView,OwnerCreateView,OwnerDetailView,OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import PostCreateForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

class PostListView(OwnerListView):
    model=Post
    template_name = "myblog/post_list.html"
    def get(self,request):
        post_list=Post.objects.all()
        favorite=list()
        if request.user.is_authenticated:
            rows=request.user.favorite_posts.values('id')
            favorite=[row['id'] for row in rows]
        cntx={'post_list':post_list,'favorite':favorite}
        return render(request,self.template_name,cntx)


class PostDetailView(OwnerDetailView):
    model=Post
    template_name = "myblog/post_detail.html"
    def get(self,request,pk):
        post=Post.objects.get(id=pk)
        comments=Comment.objects.filter(post=post).order_by('-updated_at')
        form=CommentForm()
        cntx={'post':post,'comments':comments,'form':form}
        return render(request,self.template_name,cntx)



class PostCreateView(LoginRequiredMixin,View):
    template_name="myblog/post_create_form.html"
    success_url=reverse_lazy("blog:post_list")

    def get(self,request,pk=None):
        form=PostCreateForm()
        cntx={'form':form}
        return render(request,self.template_name,cntx)

    def post(self,request,pk=None):
        form=PostCreateForm(request.POST,request.FILES or None)

        if not form.is_valid():
            cntx={'form':form}
            return render(request,self.template_name,cntx)

        post=form.save(commit=False)
        post.owner=self.request.user
        post.save()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin,View):
    def post(self,request,pk):
        post=get_object_or_404(Post,id=pk)
        comment=Comment(text=request.POST['text'],owner=request.user,post=post)
        comment.save()
        return redirect(reverse('blog:post_detail',args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "myblog/delete_confirm.html"
    def get_success_url(self):
        post=self.object.post
        return reverse("blog:post_detail",args=[post.id])

@method_decorator(csrf_exempt,name="dispatch")
class AddFavoriteView(LoginRequiredMixin,View):
    def post(self,request,pk):
        post=get_object_or_404(Post,id=pk)
        fav=Fav(user=request.user,post=post)
        try:
            fav.save()
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt,name="dispatch")
class DeleteFavoriteView(LoginRequiredMixin,View):
    def post(self,request,pk):
        post=get_object_or_404(Post,id=pk)
        try:
            fav=Fav.objects.get(user=request.user,post=post).delete()
        except Fav.DoesNotExist as e:
            pass
        return HttpResponse()



def stream_file(request,pk):
    post=get_object_or_404(Post,id=pk)
    response = HttpResponse()
    response['Content-Type'] = post.content_type
    response['Content-Length'] = len(post.picture)
    response.write(post.picture)
    return response