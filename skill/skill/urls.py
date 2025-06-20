
from django.contrib import admin 
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from skillapp import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='login_page'), name='logout'),

    # path('', views.my_home, name="my_home"),
    path('login_page/', views.login_page, name="login_page"),
    path('rec/', views.rec, name="rec"),
    path('', views.index, name="index"),
    path('sample/', views.sample, name="sample"),
    path('export/', views.export, name="export"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])