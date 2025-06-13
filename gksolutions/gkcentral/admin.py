

# Register your models here.
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from .models import ThietBi

class ThietBiAdmin(admin.ModelAdmin):
    list_display = (
        'ten_thiet_bi',
        'ngay_nhap',
        'ngay_het_han',
        'don_vi_tinh',
        'nguoi_nhap_display',
        'ghi_chu_preview', # Thêm để xem trước ghi chú trên list
        'id'
    )
    search_fields = (
        'ten_thiet_bi',
        'nguoi_nhap__username',
        'don_vi_tinh',
        'ghi_chu' # Có thể tìm kiếm trong ghi chú
    )
    # list_filter = (
    #     'ngay_nhap',
    #     'ngay_het_han',
    #     'don_vi_tinh',
    #     'nguoi_nhap'
    # )
    list_per_page = 25

    fields = (
        'ten_thiet_bi',
        'don_vi_tinh',
        'ngay_nhap',
        'ngay_het_han',
        'nguoi_nhap_readonly',
        'ghi_chu', # Thêm trường ghi chú vào đây
    )

    readonly_fields = ('nguoi_nhap_readonly',)

    def save_model(self, request, obj, form, change):
        if not change and not obj.nguoi_nhap:
            obj.nguoi_nhap = request.user
        super().save_model(request, obj, form, change)

    def nguoi_nhap_display(self, obj):
        return obj.nguoi_nhap.username if obj.nguoi_nhap else 'N/A'
    nguoi_nhap_display.short_description = "Người Nhập"

    def nguoi_nhap_readonly(self, obj):
        if obj.nguoi_nhap:
            return obj.nguoi_nhap.username
        return "N/A"
    nguoi_nhap_readonly.short_description = "Người Nhập"

    # --- Phương thức mới: Hiển thị một phần của ghi chú trên list_display ---
    def ghi_chu_preview(self, obj):
        if obj.ghi_chu:
            # Hiển thị 50 ký tự đầu tiên và thêm '...' nếu dài hơn
            return obj.ghi_chu[:50] + '...' if len(obj.ghi_chu) > 50 else obj.ghi_chu
        return "Không có"
    ghi_chu_preview.short_description = "Ghi Chú"

# Đăng ký model với lớp Admin tùy chỉnh
admin.site.register(ThietBi, ThietBiAdmin)