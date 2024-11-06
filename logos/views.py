from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from .models import Company, Logo
from .serializers import CompanySerializer, LogoSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = Company.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def list(self, request, *args, **kwargs):
        # Try to get from cache
        cache_key = 'companies_list'
        cached_data = cache.get(cache_key)
        
        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=300)  # Cache for 5 minutes
            return response
        return Response(cached_data)

class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

    def get_queryset(self):
        queryset = Logo.objects.all()
        company_id = self.request.query_params.get('company', None)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        logo = self.get_object()
        logo.is_primary = True
        logo.save()
        return Response({'status': 'Logo set as primary'})

    def perform_create(self, serializer):
        company_id = self.request.data.get('company')
        try:
            company = Company.objects.get(id=company_id)
            serializer.save(company=company)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company ID")
