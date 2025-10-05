from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import(ListView,DeleteView,DetailView,CreateView,UpdateView)
from django.urls import reverse
from django.contrib import messages
from django.urls import reverse_lazy
from  django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Post, Comment
from .forms import CommentForm
# Create your views here.

def home(request):
    return render(request, "base.html")

def signup_view(request):
    if request.method == 'POST':
        form =SignupForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request, user)
            return redirect("login")
    else:

            form=SignupForm()
    return render(request, "blog/register.html", {"form":form})
    
def login_view(request):
  if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("listblogPost")
        else:
            # wrong credentials → show error
            return render(request, "blog/login.html", {"error": "Invalid credentials"})
    
    # GET request → just show the form
  return render(request, "blog/login.html")
    

@login_required
def profile_view(request):
    if request.method =="POST":
        request.user.email =request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request,"blog/profile.html", {"user":request.user})
    
def logout_view(request):
    logout(request)
    return redirect("login")



# CRUD OPERATION

# 1.Display All Post

class ListPostView(ListView):
    model = Post 
    template_name ="blog/post_list.html"
    context_object_name ="post"
    ordering =['-published_date']


# 2. creating a post 
class CreatePostView(CreateView):
    model = Post
    fields = ['title', 'content' ]
    template_name ="blog/post_form.html"


    def form_valid(self, form):
        form.instance.author =self.request.user
        return super().form_valid(form)

# 3. details of a post 
class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


# 4. update a blog post 

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):


    model = Post 
    fields =["title", "content"]
    template_name ="blog/editing.html"



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post =self.get_object()
        return self.request.user==post.author



class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('listblogPost')




#Comments CRUD

# @login_required(login_url='login')  # Optional: only required if posting comments
# def post_detail(request, pk):
#     post = get_object_or_404(post, pk=pk)
#     comments = post.comments.all().order_by('-created_at')
#     form = CommentForm()

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('post-detail', pk=post.pk)  # Reload the page

#     context = {
#         'post': post,
#         'comments': comments,
#         'form': form
#     }
#     return render(request, 'blog/post_detail.html', context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted.")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    
    return render(request, 'blog/comment_form_inline.html', {'form': form, 'post': post})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_edit.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def delete(self, request, *args, **kwargs):
        # show message and redirect to post detail
        obj = self.get_object()
        post_url = obj.post.get_absolute_url()
        messages.success(request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        # after deletion, go back to the post
        # Note: self.object no longer exists after delete(), but Django's DeleteView will call get_success_url before final redirect
        # to be safe, we track in delete() above; still provide fallback:
        return reverse('home')