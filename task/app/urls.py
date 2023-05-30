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
]
