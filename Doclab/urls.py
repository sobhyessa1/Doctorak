from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Pages.urls')),
    path('accounts/',include('Accounts.urls')),
    path('add_data/',include('Add_Data.urls')),
    path('Aianalysis/', include('Aianalysis.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
