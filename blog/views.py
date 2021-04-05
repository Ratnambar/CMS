from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from blog.forms import ContactForm
from blog.forms import PostForm
from django.views import View
from blog.models import Post, Category, ContactUs
from account.models import User,Profile
from django.views.generic import ListView,CreateView, DetailView,FormView, UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse


def like_post(request,sno):
    likes = get_object_or_404(Post, sno=request.POST.get('post_sno'))
    p = Post.objects.get(sno=request.POST.get('post_sno'))
    # post = Post()
    print(p.title)
    p.likes.add(request.user)
    # return HttpResponse("ok",{"title":p.title})
    return HttpResponseRedirect(reverse('post-detail',args=[int(request.POST.get('post_sno'))]))

def indexPage(request,*args,**kwargs):
    posts = Post.objects.all()
    return render(request, "blog/index.html", context={"posts": posts})
    # posts = Post.objects.filter(status="D")
    # post_titles = [post.title for post in posts]
    # title_str = ("\n\n").join(post_titles)
    # return HttpResponse(title_str)


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # context['author'] = Author.objects.all()
        return context


class PostFormView(LoginRequiredMixin,CreateView):
    login_url = 'login'
    # model = Post
    template_name = 'blog/post.html'
    form_class = PostForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     user = User.objects.get(username= self.request.user)
    #     kwargs.update({'initial':{'author': user}})
    #     return kwargs
    #
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


def search_code(request):
    search_term = ""
    articles = []
    if 'search' in request.GET:
        search_term = request.GET.get('search')
        posts = Post.objects.all()
        for post in posts:
            if search_term.lower() in post.title.lower() or search_term in post.title.lower():
                print(search_term)
                print(post.title)
                articles.append(post)
        # articles = Post.objects.filter(title=search_term)
        # print(articles)
        # print(search_term)
        return render(request, "blog/search.html", context={'articles': articles})
    else:
        return render(request, "blog/search.html")


def view_by_cat_button(request, id,*args,**kwargs):
    category = Category.objects.all()
    posts = Post.objects.filter(category__id=id)
    # print(posts)
    context = {
        'category': category,
        'posts': posts
        }
    return render(request, 'blog/cat_views.html', context)


class BtnBlogDetails(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Post
    template_name = "blog/btn-details.html"


def post_details_view(request, sno):
    post = Post.objects.filter(sno=sno).first()
    # comments = BlogComment.objects.filter(post=post, parent=None)
    # replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    # replyDict = {}
    # for reply in replies:
    #     if reply.parent.sno not in replyDict.keys():
    #         replyDict[reply.parent.sno] = [reply]
    #     else:
    #         replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'user': request.user}
    return render(request, 'blog/details.html', context)


# def like_post(request):
#     post = get_object_or_404(Post, request.POST.get('post_id'))
#     post.likes.add(request.user)
#     return HttpResponseRedirect(post.get_absolute_url())


# def postComment(request):
#     if request.method == 'POST':
#         comment = request.POST.get("comment")
#         user = request.user
#         postSno = request.POST.get("postSno")
#         parentSno = request.POST.get("parentSno")
#         post = Post.objects.get(sno=postSno)
#         if parentSno == "":
#             comment = BlogComment(comment=comment, user=user, post=post)
#             comment.save()
#         else:
#             parent = BlogComment.objects.get(sno=parentSno)
#             comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
#             comment.save()
#         # messages.success(request, "your message has been post successfully!.")
#         return redirect(f"/blogs/{post.slug}")


class PostFormUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    # success_url = "contact"
    template_name = "blog/post.html"

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     user = Profile.objects.get(username=self.request.user)
    #     kwargs.update({'initial': {'author': user}})
    #     return kwargs
    #
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


class PostFormDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('profile')
    template_name = "blog/confirm-delete.html"


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form)
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect('contact/')
        return render(request, 'blog/contact.html', context={"form": form})
    return render(request, 'blog/contact.html', context={"form": ContactForm})


    # def form_valid(self, form):
    #     return super().form_valid(form)


def Trending_Posts(request,*args,**kwargs):
    trending_posts = Trending_Posts.objects.all()
    print(trending_posts)
    return render(request, "blog/index.html", context={"trending_posts": trending_posts})


def post_edit_form_view(request,id,*args,**kwargs):
    try:
        post = Post.objects.get(id=id)
    except:
        return HttpResponse("Invalid Post ID")

    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, "blog/post.html", context={"form": form})
    else:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponse("welcome")

        return render(request, "blog/post.html", context={"form": form})
    return render(request, "blog/post.html", context={"form": form})


# def post_details(request,id,*args,**kwargs):
#     try:
#         post = Post.objects.get(id=id)
#         post_str = "{} \n\n {}".format(post.title,post.content)
#         return HttpResponse(post_str)
#     except:
#         return HttpResponse("Invalid Id")


# def contact_view(request,*args,**kwargs):
#     # print(request.method)
#     if request.method == "GET":
#         form = ContactForm()
#         return render(request, "blog/contact.html", context={"form": form})
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             return HttpResponse("thank you")
#         else:
#             return render(request, "blog/contact.html", context={"form": form})
#
#     form = ContactForm()
#     return render(request, "blog/contact.html", context={"form": form})
