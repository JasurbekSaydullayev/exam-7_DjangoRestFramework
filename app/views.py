from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import UserPasswordManager
from .serializers import UserPasswordSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters


class RobotList(generics.ListCreateAPIView):
    queryset = UserPasswordManager.objects.all()
    serializer_class = UserPasswordSerializer
    name = 'user_password'
    filter_fields = ['application_type']


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
        'Filter by application': '/?application=application_type',
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
    if request.query_params:
        items = UserPasswordManager.objects.filter(**request.query_params.dict())
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
