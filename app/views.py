from django.shortcuts import get_object_or_404
from .models import UserPasswordManager
from .serializers import UserPasswordSerializer
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters


class UserPasswordView(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = UserPasswordManager.objects.all()
    serializer_class = UserPasswordSerializer


# CRUD MODELI UCHUN VIEWLAR
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by name': '/?name=name',
        'Filter by application': '/?application_type=application_type',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/delete/pk/delete',
    }

    return Response(api_urls)


@api_view(['POST'])
def add_items(request):
    item = UserPasswordSerializer(data=request.data)

    if UserPasswordManager.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
    filter_params = {key: value for key, value in request.query_params.items() if key.startswith('filter_')}

    if filter_params:
        items = UserPasswordManager.objects.filter(**filter_params)
    else:
        items = UserPasswordManager.objects.all()

    if items:
        serializer = UserPasswordSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_items(request, pk):
    item = UserPasswordManager.objects.get(pk=pk)
    data = UserPasswordSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(UserPasswordManager, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
