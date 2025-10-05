from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post
from taggit.forms import TagWidget



class SignupForm(UserCreationForm):
    email =forms.EmailField(required=True)



    class Meta:
        model = User
        fields =["username", "email", "password1", "password2"]



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # only the content field is user-editable

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == "":
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 3:
            raise forms.ValidationError("Comment is too short — please write a bit more.")
        return content
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include tags
        widgets = {
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Add tags separated by commas...',
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }