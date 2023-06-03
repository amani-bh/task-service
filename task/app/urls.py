from django.urls import path

from . import views

urlpatterns = [
    path("add_project", views.add_project),
    path("user_projects/<int:id>", views.projects_by_user),
    path("project_by_id/<int:id>", views.project_by_id),
    path("add_list", views.add_list),
    path("add_item", views.add_item),
    path("update_list_title/<int:id>", views.update_list_title),
    path("update_item_title/<int:id>", views.update_item_title),
    path("update_item_description/<int:id>", views.update_item_description),
    path("update_item_order/<int:id>", views.update_item_order),
    path("update_list_order/<int:id>", views.update_list_order),
    path("comments_by_item/<int:id>", views.comments_by_item),
    path("add_comment", views.add_comment),
    path("update_comment/<int:id>", views.update_comment),
    path("delete_comment/<int:id>", views.delete_comment),
    path("invite_member/<int:id>", views.invite_member),
    path('join/<uidb64>/<id>/', views.join_member, name='join'),
    path('assign_to_item/<int:id>/<int:idUser>/', views.assign_to_item),
]
