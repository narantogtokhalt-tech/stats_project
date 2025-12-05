import django_filters
from .models import CustomMonthlyRaw

class CustomMonthlyRawFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="year")
    month = django_filters.CharFilter(field_name="month", lookup_expr='exact')
    companyName = django_filters.CharFilter(field_name="companyName", lookup_expr='icontains')
    senderReceiver = django_filters.CharFilter(field_name="senderReceiver", lookup_expr='exact')
    importExportFlag = django_filters.CharFilter(field_name="importExportFlag", lookup_expr='exact')  # <-- Add this line

    class Meta:
        model = CustomMonthlyRaw
        fields = ['year', 'month', 'companyName', 'senderReceiver', 'importExportFlag']