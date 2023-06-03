import uuid

from django.core.mail import send_mail
from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Project, List, Item, Comment
from .serializers import ProjectSerializer, ListSerializer, ItemSerializer, CommentSerializer


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
        return Response([])


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


@api_view(['GET'])
def comments_by_item(request,id):
    comments = Comment.objects.filter(item_id=id).order_by('-created_at')
    if comments:
        serializer = CommentSerializer(comments,many=True)
        data = serializer.data
        return Response(data)
    else:
        return Response([])


@api_view(['POST'])
def add_comment(request):
    print(request.data)
    comment = CommentSerializer(data=request.data)

    if comment.is_valid():
        comment.save()
        return Response(comment.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_comment(request, id):
    try:
        comment_obj = Comment.objects.get(pk=id)
        comment_obj.body = request.data.get('body', '')
        comment_obj.save()
        serializer = CommentSerializer(comment_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_comment(request, id):
    try:
        comment_obj = Comment.objects.get(pk=id)
        comment_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def invite_member(request, id):
    try:
        project = Project.objects.get(pk=id)
        email = request.data.get('email', '')
        owner_name= request.data.get('name', '')
        receiver_id= request.data.get('receiver_id', '')
        if receiver_id in project.members:
             return Response({'error': 'Member already exist'}, status=status.HTTP_404_NOT_FOUND)
        uidb64 = urlsafe_base64_encode(force_bytes(project.pk))
        activate_url = reverse('join', kwargs={'uidb64': uidb64, 'id': receiver_id})
        activate_url = request.build_absolute_uri(activate_url)
        subject = f'{owner_name} has invited you to join {project.title}'
        message = (f'Click on the following link to accept: {activate_url}')
        to_email = email
        send_mail(subject, message, from_email=None,
                          recipient_list=[to_email])

        return Response(status=status.HTTP_204_NO_CONTENT)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def join_member(request, uidb64,id):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        project = Project.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, Project.DoesNotExist):
        project = None

    if project :
        if project.members is None:
            project.members=[]
        project.members.append(id)
        project.save()
        return Response({'message': 'Join successful!'}, status=status.HTTP_200_OK)

    return Response({'message': 'Join link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def assign_to_item(request,id,idUser):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    if item:
        item.assigned_to=idUser
        item.save()
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'message': 'J invalid!'}, status=status.HTTP_400_BAD_REQUEST)
