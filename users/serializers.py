from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    # Meta class to specify the model and fields to be serialized
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'verification_token', 'verified']
        # Make the password field write-only
        extra_kwargs = {'password': {'write_only': True}}

    # Override the create method to hash the password
    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
