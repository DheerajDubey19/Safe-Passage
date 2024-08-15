from django.contrib import admin
from django.urls import path, include
from users.views import UserViewSet, verify_email_view
from files.views import FileViewSet
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView

# Initialize the default router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'files', FileViewSet, basename='file')

# Define URL patterns
urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/v1/', include(router.urls)),
    
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Operations user login
    path('login_ops/', UserViewSet.login_ops_view, name='login_ops'),
    
    # Client user login
    path('login_client/', UserViewSet.login_client_view, name='login_client'),
    
    # Email verification
    path('users/verify-email/', verify_email_view, name='verify-email'),
    
    # Operations user signup
    path('signup_ops/', UserViewSet.signup_ops_view, name='signup_ops'),
    
    # Client user signup
    path('signup_client/', UserViewSet.signup_client_view, name='signup_client'),
    
    # File upload
    path('upload_file/', UserViewSet.upload_file_view, name='upload_file'),
    
    # List files
    path('list_files/', UserViewSet.list_files_view, name='list_files'),
    
    # Download file
    path('download-file/<int:pk>/', FileViewSet.as_view({'get': 'download_file'}), name='download_file'),
    
    # Generate download link
    path('generate-download-link/<int:pk>/', FileViewSet.as_view({'get': 'generate_download_link'}), name='generate_download_link'),
    
    # User logout
    path('logout/', UserViewSet.logout_view, name='logout'),
]
