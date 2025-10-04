from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import(ListView,DeleteView,DetailView,CreateView,UpdateView)
from .models import post 
from django.urls import reverse_lazy
from  django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# Create your views here.

def home(request):
    return render(request, "blog/home.html")

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
            return redirect("profile")
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
    model = post 
    template_name ="blog/Listview.html"
    context_object_name ="post"
    ordering =['-published_date']


# 2. creating a post 
class CreatePostView(CreateView):
    model = post
    fields = ['title', 'content' ]
    template_name ="blog/Createview.html"


    def form_valid(self, form):
        form.instance.author =self.request.user
        return super().form_valid(form)

# 3. details of a post 
class DetailPostView(DetailView):
    model = post
    template_name = 'blog/Detailview.html'


# 4. update a blog post 

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):


    model = post 
    fields =["title", "content"]
    template_name ="blog/updatepost.html"



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post =self.get_object()
        return self.request.user==post.author



class DeletePostView(DeleteView):
    model = post
    template_name = "blog/Deleteview.html"
    success_url = reverse_lazy('listblogPost')
