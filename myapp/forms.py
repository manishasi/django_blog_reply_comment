from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post,Comment,Reply

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        help_texts = {
            'username': None
        }

    # def __init__(self, args, *kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['username'].help_text = None

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','dob','place','zipcode','picture')
        

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image')

class CommentForm(forms.ModelForm):
    # parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Comment
        fields = ('comment_body',)

class ReplyForm(forms.ModelForm):
    reply_body = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 2}))
    # short_desc = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Reply
        fields = ('reply_body',)


# class Comment_LikeForm(forms.ModelForm):
#     class Meta:
#         model = LikeComment
#         fields = ('user','comment','likes')

# class CommentForm(forms.ModelForm):
#     content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows': '3','placeholder': 'Write a comment...'}))

#     class Meta:
#         model = Comment
#         fields = ('content',)





