from django.urls import path

from api.views import get_providers, delete_provider, update_provider, get_provider_by_id

provider_urlpatterns = [
    path('Provider/GetAll', get_providers),
    path('Provider/GetById', get_provider_by_id),
    path('Provider/Update', update_provider),
    path('Provider/Delete', delete_provider),
]