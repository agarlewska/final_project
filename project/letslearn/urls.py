from django.urls import path

from .views import IndexView, MaterialListView, MaterialDetailView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('materials/', MaterialListView.as_view(), name="material_list"),
    path('materials/<int:material_id>/', MaterialDetailView.as_view(), name="material_details"),
]
