from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be serialized
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']
        # Make the 'uploaded_by' and 'uploaded_at' fields read-only
        read_only_fields = ['uploaded_by', 'uploaded_at']
