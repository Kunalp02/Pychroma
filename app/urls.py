from django.urls import path

from .views import ChromaLoginView, CollectionView, DashboardView

urlpatterns = [
    path("", ChromaLoginView.as_view(), name="chroma_login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "collection/<str:collection_name>/",
        CollectionView.as_view(),
        name="collection_view",
    ),
]
