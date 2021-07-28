from django.urls import path
from student import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'student'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/' , views.login, name='login'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name="user_login"),
    path('questions/<int:exam_id>/', views.questions, name="questions"),
    path('finish/<int:exam_id>', views.finish, name="finish"),
    path('exams/', views.exams, name="exams"),
    path('ready/<int:exam_id>', views.ready, name="ready"),
    path('save_answers/', views.save_answers, name="save_answers"),
    path('fortest/', views.questions, name="fortest"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
