from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Project, List, Item
from .serializers import ProjectSerializer, ListSerializer, ItemSerializer


@api_view(['POST'])
def add_project(request):
    project_data = request.data.get('project', {})
    project = ProjectSerializer(data=project_data)

    if project.is_valid():
        project.save()
        return Response(project.data, status=status.HTTP_201_CREATED)
    else:
        return Response(project.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def projects_by_user(request,id):
    projects = Project.objects.filter(owner=id).order_by('-created_at')
    if projects:
        serializer = ProjectSerializer(projects, many=True)
        data = serializer.data
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def project_by_id(request,id):
    project = Project.objects.get(pk=id)
    if project:
        serializer = ProjectSerializer(project)
        data = serializer.data
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_list111(request):
    print(request)
    list_data = request.data.get('list', {})
    list = ListSerializer(data=list_data)

    if list.is_valid():
        list.save()
        return Response(list.data, status=status.HTTP_201_CREATED)
    else:
        return Response(list.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_list(request):
    project_id = request.data.get('project')
    title = request.data.get('title')

    filtered_objects = List.objects.filter(project_id=project_id)
    order = None

    if not filtered_objects.exists():
        order = 2 ** 16 - 1
    elif  filtered_objects.filter(order__isnull=False).exists():
        order = filtered_objects.aggregate(Max('order'))['order__max'] + 2 ** 16 - 1

    newList = ListSerializer(data={
        "project":project_id,"title":title,"order":order
    })
    if newList.is_valid():
        newList.save()
        return Response(newList.data, status=status.HTTP_201_CREATED)
    return Response({'message': 'List added successfully'})


@api_view(['POST'])
def add_item(request):
    list_id = request.data.get('list')
    title = request.data.get('title')

    filtered_objects = Item.objects.filter(list_id=list_id)
    order = None

    if not filtered_objects.exists():
        order = 2 ** 16 - 1
    elif  filtered_objects.filter(order__isnull=False).exists():
        order = filtered_objects.aggregate(Max('order'))['order__max'] + 2 ** 16 - 1

    newItem = ItemSerializer(data={
        "list":list_id,"title":title,"order":order
    })
    if newItem.is_valid():
        newItem.save()
        return Response(newItem.data, status=status.HTTP_201_CREATED)
    return Response({'message': 'Item added successfully'})


@api_view(['POST'])
def update_list_title(request, id):
    try:
        print("*****",request.data)
        list_obj = List.objects.get(pk=id)
        list_obj.title = request.data.get('title', '')
        list_obj.save()
        serializer = ListSerializer(list_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except List.DoesNotExist:
        return Response({'error': 'List not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_item_title(request, id):
    try:
        item_obj = Item.objects.get(pk=id)
        item_obj.title = request.data.get('title', '')
        item_obj.save()
        serializer = ItemSerializer(item_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_item_description(request, id):
    try:
        item_obj = Item.objects.get(pk=id)
        item_obj.title = request.data.get('title', '')
        item_obj.description = request.data.get('description', '')
        item_obj.save()
        serializer = ItemSerializer(item_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_list_order(request, id):
    try:
        list_obj = List.objects.get(pk=id)
        list_obj.title = request.data.get('title', '')
        list_obj.order = request.data.get('order', '')
        list_obj.save()
        serializer = ListSerializer(list_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except List.DoesNotExist:
        return Response({'error': 'List not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_item_order(request, id):
   print("id**",id)
   try:
        item_obj = Item.objects.get(pk=id)
        print("aaaaa",request.data.get('title', ''))
        item_obj.title = request.data.get('title', '')
        item_obj.order = request.data.get('order', '')
        item_obj.list_id = request.data.get('list', '')
        item_obj.save()
        serializer = ItemSerializer(item_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

   except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
