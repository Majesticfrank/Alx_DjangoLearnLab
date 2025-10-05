from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Post, Comment
from django.db.models import Q
from taggit.models import Tag  # ✅ import from taggit
from .forms import PostForm, CommentForm

# ------------------------------
# Authentication Views
# ------------------------------

def home(request):
    return render(request, "base.html")


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("listblogPost")
        else:
            return render(request, "blog/login.html", {"error": "Invalid credentials"})
    return render(request, "blog/login.html")


@login_required
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request, "blog/profile.html", {"user": request.user})


def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------------------
# Post CRUD
# ------------------------------

class ListPostView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ['-published_date']


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm  # ✅ include tags
    template_name = "blog/editing.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy('listblogPost')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# ------------------------------
# Comments CRUD
# ------------------------------

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment posted successfully.")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form_inline.html', {'form': form, 'post': post})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form_inline.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_edit.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
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
        obj = self.get_object()
        post_url = obj.post.get_absolute_url()
        messages.success(request, "Comment deleted successfully.")
        response = super().delete(request, *args, **kwargs)
        return redirect(post_url)


# ------------------------------
# Tag and Search Views (taggit)
# ------------------------------

def search_posts(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})


def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags__name__iexact=tag.name)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Retrieve the tag slug from the URL
        tag_slug = self.kwargs.get('tag_slug')
        # Get the tag object or return 404 if not found
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        # Return all posts with this tag
        return Post.objects.filter(tags__slug=self.tag.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context