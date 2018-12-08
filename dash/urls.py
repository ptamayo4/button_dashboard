from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_proj', views.add_project),
    path('test/<int:p_id>', views.test_ep),
    path('bind/<int:p_id>', views.bind_ep),
    path('delete/<int:p_id>', views.delete_ep),
]
