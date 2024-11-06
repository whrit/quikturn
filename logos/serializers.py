from rest_framework import serializers
from .models import Company, Logo

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['id', 'image', 'is_primary', 'source_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CompanySerializer(serializers.ModelSerializer):
    logos = LogoSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'description', 'logos', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']