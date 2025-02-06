from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns= [
    path('',views.Bhagwat_Gita),
    path('signin/', views.SignIn, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comments/', views.show_minor_page,name='comments'),
    path('logout/', views.logout_user, name='logout'),
    path('texts/<str:chapter_title>/', views.display_text, name='texts'),
    path('pdf/<str:scripture_title>/', views.display_pdf, name='pdf'),
    path('chapters/<str:scripture_title>/', views.view_chapters, name='chapters'),
]
