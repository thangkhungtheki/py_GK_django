"""
URL configuration for gksolutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from . import views

# --- Bắt đầu phần chỉnh sửa ---
admin.site.site_header = "Hệ thống Quản lý Thiết bị Gia Khang"  # Tên bạn muốn hiển thị ở header
admin.site.site_title = "Quản trị Gia Khang"      # Tên hiển thị trên tab trình duyệt
admin.site.index_title = "Chào mừng đến với trang Quản trị" # Tiêu đề trang index của admin
# --- Kết thúc phần chỉnh sửa ---


urlpatterns = [
    path('admin/', admin.site.urls),
    path('gkcentral/', include('gkcentral.urls')),
    path('', views.index, name='index')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)