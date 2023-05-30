from rest_framework import serializers

from .models import Item, List, Comment, Project





class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = '__all__'

    def get_items(self, obj):
        queryset = Item.objects.filter(list=obj).order_by('order')
        return ItemSerializer(queryset, many=True).data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

    def get_lists(self, instance):
        return instance.get_lists()
