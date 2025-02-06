from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Comment,Scripture,Chapter
from .forms import CommentForm
from .models import Comment
from django.contrib.auth import logout
def Bhagwat_Gita(request):
    scriptures = Scripture.objects.all()
    return render(request, 'Minor.html', {'scriptures': scriptures})
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  
            send_signup_email(user.email)
            login(request, user)
            return redirect('signin') 
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form': form})

def send_signup_email(user_email):
    subject = 'Welcome to YourWebsite!'  
    message = 'Thank you for signing up. We hope you enjoy your experience.' 
    from_email = settings.EMAIL_HOST_USER  
    to_email = user_email  
    send_mail(subject, message, from_email, [to_email])  

def SignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('forgot_email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error_message': 'No user found with this email'}, status=400)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        send_mail(
            'Password Reset',
            f'Click the following link to reset your password: {request.build_absolute_uri(reset_link)}',
            settings.EMAIL_HOST_USER,  
            [email],
            fail_silently=False,
        )
        messages.success(request, 'Change the password and try signing in from the homepage again. :)')
        return HttpResponseRedirect('/')


    return render(request, 'forgot_password.html')
def logout_user(request):
    logout(request)
    return redirect('/')

from django.utils import timezone

@login_required
def post_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            if request.user.is_authenticated:
                user = request.user
                Comment.objects.create(text=text, user=user, created_at=timezone.now())
                return redirect('/')
            else:
                return redirect('signin')  
    else:
        form = CommentForm()
    return render(request, 'Minor.html', {'form': form})
@login_required
def show_minor_page(request):
    scriptures = Scripture.objects.all()
    recent_comments = Comment.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=1))
    return render(request, 'Minor.html', {'scriptures':scriptures,"comments": recent_comments})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user: 
        comment.delete()
    return redirect('/')

def display_text(request, chapter_title):
    selected_chapter = get_object_or_404(Chapter, title=chapter_title)
    return render(request, 'temp.html', {'selected_chapter': selected_chapter})

def display_pdf(request, scripture_title):
    selected_scripture = get_object_or_404(Scripture, title=scripture_title)
    # Add any additional logic here if needed
    return render(request, 'pdf_viewer.html', {'selected_scripture': selected_scripture})

def view_chapters(request, scripture_title):
    selected_scripture = get_object_or_404(Scripture, title=scripture_title)
    chapters = selected_scripture.chapters.all()
    return render(request, 'temp2.html', {'selected_scripture': selected_scripture, 'chapters': chapters})
