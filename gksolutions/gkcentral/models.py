from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ThietBi(models.Model):
    ten_thiet_bi = models.CharField(max_length=255, verbose_name="Tên Thiết Bị")
    ngay_nhap = models.DateField(default=timezone.now, verbose_name="Ngày Nhập")
    ngay_het_han = models.DateField(null=True, blank=True, verbose_name="Ngày Hết Hạn")
    don_vi_tinh = models.CharField(max_length=50, verbose_name="Đơn Vị Tính")

    nguoi_nhap = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='thiet_bis_nhap',
        verbose_name="Người Nhập"
    )

    # --- Thêm trường ghi chú mới ---
    ghi_chu = models.TextField(
        blank=True, # Cho phép trường này trống (không bắt buộc nhập)
        null=True,  # Cho phép giá trị NULL trong cơ sở dữ liệu
        verbose_name="Ghi Chú Chi Tiết"
    )

    class Meta:
        verbose_name = "Thiết Bị"
        verbose_name_plural = "Thiết Bị"
        ordering = ['-ngay_nhap']

    def __str__(self):
        return self.ten_thiet_bi