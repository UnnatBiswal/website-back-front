from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from markdownx.fields import MarkdownxFormField

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2',)  # Add other fields here if needed

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # You can add additional validation logic for the email field here if needed
        return email
    
class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

class MarkdownField(MarkdownxFormField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['class'] = 'markdown-input'
        self.widget.attrs['rows'] = 10  # Adjust rows as needed
