from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Giả sử User là người thực hiện sửa chữa

# --- Model 1: Site (Địa điểm/Cơ sở) ---
class Site(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên Site")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ")
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="Người liên hệ")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    
    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Các Site"
        ordering = ['name']

    def __str__(self):
        return self.name

# --- Model 2: Room (Phòng) ---
class Room(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name="Thuộc Site"
    )
    room_number = models.CharField(max_length=50, verbose_name="Số Phòng/Tên Phòng")
    room_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Loại Phòng")
    capacity = models.IntegerField(blank=True, null=True, verbose_name="Sức chứa")
    
    class Meta:
        verbose_name = "Phòng"
        verbose_name_plural = "Các Phòng"
        # Đảm bảo mỗi phòng là duy nhất trong một site
        unique_together = ('site', 'room_number') 
        ordering = ['site__name', 'room_number']

    def __str__(self):
        return f"{self.site.name} - Phòng {self.room_number}"

# --- Model 3: MaintenanceRecord (Lịch sử sửa chữa) ---
class MaintenanceRecord(models.Model):
    # Liên kết với Site (nếu sửa chữa cho cả site, ví dụ: sửa mái nhà)
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        null=True,
        blank=True,
        verbose_name="Site liên quan"
    )
    
    # Liên kết với Room (nếu sửa chữa cho từng phòng, ví dụ: sửa điều hòa phòng 101)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        null=True,
        blank=True,
        verbose_name="Phòng liên quan"
    )

    # Đảm bảo phải có ít nhất một trong hai trường site hoặc room được chọn
    # Điều này sẽ được xử lý trong form Django hoặc logic view
    
    description = models.TextField(verbose_name="Mô tả sửa chữa")
    maintenance_date = models.DateField(default=timezone.now, verbose_name="Ngày sửa chữa")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Chi phí (VNĐ)")
    performed_by = models.CharField(max_length=255, blank=True, null=True, verbose_name="Thực hiện bởi") # Có thể là nhà cung cấp dịch vụ
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú thêm")
    
    # Người tạo bản ghi (có thể là User quản lý nội bộ)
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_maintenance',
        verbose_name="Người ghi nhận"
    )

    class Meta:
        verbose_name = "Bản ghi sửa chữa"
        verbose_name_plural = "Lịch sử sửa chữa"
        ordering = ['-maintenance_date']

    def __str__(self):
        if self.room:
            return f"Sửa chữa Phòng {self.room.room_number} ({self.room.site.name}) - {self.maintenance_date}"
        elif self.site:
            return f"Sửa chữa Site {self.site.name} (chung) - {self.maintenance_date}"
        return f"Sửa chữa không xác định - {self.maintenance_date}"
    
    def clean(self):
        # Đảm bảo chỉ một trong site hoặc room được điền
        if self.site is None and self.room is None:
            raise models.ValidationError("Phải chọn ít nhất một Site hoặc một Phòng.")
        if self.site is not None and self.room is not None:
            # Nếu cả hai được chọn, đảm bảo phòng thuộc về site đó
            if self.room.site != self.site:
                raise models.ValidationError("Phòng được chọn không thuộc Site đã chọn.")
            # Có thể đặt logic chỉ chấp nhận một trong hai nếu cần sự rõ ràng tuyệt đối
            # raise models.ValidationError("Chỉ có thể chọn Site HOẶC Phòng, không được cả hai.")