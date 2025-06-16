# admin.py
from django.contrib import admin
from .models import Site, Room, MaintenanceRecord

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('site', 'room_number', 'room_type', 'capacity')
    list_filter = ('site', 'room_type')
    search_fields = ('room_number',)
    raw_id_fields = ('site',) # Giúp chọn site dễ hơn nếu có nhiều site

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('maintenance_date', 'site', 'room', 'description', 'cost', 'performed_by', 'recorded_by')
    list_filter = ('maintenance_date', 'site', 'room', 'performed_by')
    search_fields = ('description', 'performed_by', 'notes')
    raw_id_fields = ('site', 'room', 'recorded_by') # Giúp chọn liên kết dễ hơn
    date_hierarchy = 'maintenance_date' # Tạo bộ lọc theo ngày

  # --- Thêm phương thức này để tự động gán người dùng ---
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Chỉ gán khi tạo mới (chưa có primary key)
            obj.recorded_by = request.user # Gán người dùng đang đăng nhập
        super().save_model(request, obj, form, change)

    # (Tùy chọn) Ẩn trường 'recorded_by' khỏi form nếu không muốn người dùng thấy/sửa
    # fieldsets = (
    #     (None, {
    #         'fields': ('site', 'room', 'description', 'maintenance_date', 'cost', 'performed_by', 'notes')
    #     }),
    # )
    # Hoặc chỉ loại trừ nó khỏi form
    # exclude = ('recorded_by',)
    
    # Nếu anh muốn hiển thị nhưng làm cho nó chỉ đọc (read-only)
    readonly_fields = ('recorded_by',)