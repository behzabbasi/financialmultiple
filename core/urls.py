
from django.contrib import admin
from django.urls import path
from .views import home_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home'),
    path('sp500/', include('sp500.urls'), name='sp500'),
    path('inerest_rate/', include('interest_rate.urls'), name='interest_rate'),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)