from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all().order_by('-date_taken')
    serializer_class = SessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['name']

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('-date_uploaded')
    serializer_class = PhotoSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'session', 'main_page']
    search_fields = ['name']

    @action(detail=True, methods=['delete'])
    def delete_photo(self, request, pk=None):
        Photo.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk=None):
        serializer = PhotoSerializer(Photo.objects.get(pk=pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        instance = Photo.objects.get(pk=pk)

        if ('session' in request.data and request.data['session'] == 'None'):
            instance.session = None
            instance.save()
            del request.data['session']

        serializer = PhotoSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)