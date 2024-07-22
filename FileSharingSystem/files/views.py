from django.shortcuts import render, HttpResponse
import os 
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import File
from django.shortcuts import get_object_or_404
from .serializers import FileSerializer
from django.contrib.auth.decorators import login_required

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    # Action to handle file uploads
    @login_required
    @action(detail=False, methods=['post'])
    def upload_file(self, request):
        current_user = request.user
        # Ensure only operations users can upload files
        if current_user.role != 'ops':
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        file = request.FILES.get('file')

        # Check if the file type is allowed
        if not file or not self.allowed_file(file.name):
            return Response({"message": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST)

        file_record = File.objects.create(file=file, uploaded_by=current_user)

        return Response({"message": "File uploaded successfully", "file_id": file_record.id}, status=status.HTTP_201_CREATED)

    # Static method to check allowed file types
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pptx', 'docx', 'xlsx'}

    # Action to generate a download link for a file
    @action(detail=True, methods=['get'])
    # @login_required
    def generate_download_link(self, request, pk=None):
        current_user = request.user

        # Ensure only client users can generate download links
        if current_user.role != 'client':
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        file = get_object_or_404(File, id=pk)

        # Generate a secure download link (use file ID in the link)
        download_link = request.build_absolute_uri(f'/download-file/{file.id}/')
        return render(request, 'download_link.html', {'download_link': download_link, 'message': 'success'})

    # Action to handle file downloads
    @action(detail=True, methods=['get'])
    # @login_required
    def download_file(self, request, pk=None):
        current_user = request.user

        # Ensure only client users can download files
        if current_user.role != 'client':
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        file = get_object_or_404(File, id=pk)
        file_path = file.file.path

        # Check if the file exists on the server
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            return Response({"message": "File not found on the server"}, status=status.HTTP_404_NOT_FOUND)
