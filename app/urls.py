from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import home, theme_accept, theme_decline, TeacherRegisterView, StudentRegisterView, CustomLoginView, load_ajax, themedelete, teacher_profile
from app.forms import LoginForm
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', home, name='home'),
    path('teacher_register/', TeacherRegisterView.as_view(), name='teacher-register'),
    path('student_register/', StudentRegisterView.as_view(), name='student-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='app/login.html',
                                           authentication_form=LoginForm, next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    path('load_ajax/', load_ajax, name="load_ajax"),
    path(r'delete_theme/<str:theme>', themedelete, name='theme-delete'),
    path('teacher/<int:user_id>/', teacher_profile, name='teacher-profile'),
    path('accept_theme/<int:user_id>/', theme_accept, name='th-acc'),
    path('decline_theme/<int:user_id>/', theme_decline, name='th-dec'),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)