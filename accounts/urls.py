from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, include, reverse_lazy

from accounts.views import register_user, login_user, logout_user, sent_confirm_view, confirm_email_view, user_account
from django.contrib.auth import views as auth_views #import this
urlpatterns = [

                path('login/', login_user, name='login'),
                path('logout/', logout_user, name='logout'),
                path('register/', register_user, name='register_user'),
                path('confirm-email/<str:token>', confirm_email_view, name='confirm-view'),
                path('go-confirm-email/', sent_confirm_view, name='confirmation-message-view'),
                path('user-account/me', user_account, name='user_account'),

                path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password'
                                                                                                    '/password_reset_done.html'),
                     name='password_reset_done'),
                path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"),
                     name='password_reset_confirm'),
                path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'),
                     name='password_reset_complete'),


]