from django.urls import path
from .views import lead_create, lead_list, lead_detail, lead_update


app_name = "leads"

urlpatterns = [
    path('', lead_list),
    path('create/', lead_create),
    path('<int:pk>/update/', lead_update),
    path('<int:pk>/', lead_detail),
]
