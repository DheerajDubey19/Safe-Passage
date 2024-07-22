from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from files.models import File
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
import uuid

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Action to register operations users
    @action(detail=False, methods=['post'])
    def register_ops(self, request):
        data = request.data.copy()
        data['role'] = 'ops'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Ops User registered successfully"}, status=status.HTTP_201_CREATED)

    # Action to verify email
    @action(detail=False, methods=['get'], url_path='verify-email')
    def verify_email(self, request):
        verification_token = request.query_params.get('verification_token')
        user = User.objects.filter(verification_token=verification_token).first()
        if user:
            user.verified = True
            user.verification_token = None
            user.save()
            return render(request, 'login_client.html', {"message": "Email verification successful"})
        return render(request, 'signup_client.html', {"message": "Invalid verification token"})

    # View for operations user login
    def login_ops_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)

            if user and user.role == 'ops':
                login(request, user)
                return redirect(reverse('upload_file'))
            return render(request, 'login_ops.html', {"message": "Invalid credentials"})

        return render(request, 'login_ops.html')

    # View for client user login
    def login_client_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)

            if user and user.role == 'client' and user.verified:
                login(request, user)
                return redirect(reverse('list_files'))
            return render(request, 'login_client.html', {"message": "Invalid credentials"})

        return render(request, 'login_client.html')

    # View for operations user signup
    def signup_ops_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create(email=email, role='ops')
            user.set_password(password)
            user.save()
            return render(request, 'login_ops.html', {"message": "Ops User registered successfully. Please log in."})

        return render(request, 'signup_ops.html')

    # View for client user signup
    def signup_client_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create(email=email, role='client')
            user.set_password(password)
            user.save()
            user.verification_token = uuid.uuid4().hex
            user.save()

            # Create verification URL
            verification_url = request.build_absolute_uri(f"/users/verify-email/?verification_token={user.verification_token}")

            # Send verification email
            send_mail(
                'Verify your email',
                f'Click the following link to verify your email: {verification_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            return render(request, 'signup_client.html', {"message": "Client User registered successfully. Please check your email for verification."})

        return render(request, 'signup_client.html')

    # View to handle file upload
    @login_required
    def upload_file_view(request):
        if request.method == 'POST':
            file = request.FILES.get('file')
            user = request.user

            # Ensure only operations users can upload files
            if user.role != 'ops':
                return render(request, 'upload_file.html', {"message": "Unauthorized"})

            # Check if the file type is allowed
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pptx', 'docx', 'xlsx'}

            if not file or not allowed_file(file.name):
                return render(request, 'upload_file.html', {"message": "Invalid file type"})

            file_record = File.objects.create(file=file, uploaded_by=user)

            return render(request, 'upload_file.html', {"message": "File uploaded successfully", "file_id": file_record.id})

        return render(request, 'upload_file.html')

    # View to list all files
    @login_required
    def list_files_view(request):
        files = File.objects.all()
        return render(request, 'list_files.html', {'files': files})

    # View to handle user logout
    def logout_view(request):
        logout(request)
        return redirect('home')

# Standalone view to verify email
def verify_email_view(request):
    verification_token = request.GET.get('verification_token')
    user = User.objects.filter(verification_token=verification_token).first()
    if user:
        user.verified = True
        user.verification_token = None
        user.save()
        return render(request, 'login_client.html')
    return render(request, 'signup_client.html', {"message": "Invalid verification token"})
