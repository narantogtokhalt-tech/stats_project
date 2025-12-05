from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Category, Dataset, DataPoint, CustomMonthlyRaw, CustomMonthlyExport, CustomMonthlyImport, CustomMonthlyImportSum, CustomMonthlyImportCustom, ExportDaily, ImportDaily, CurrencyMove, FuelImport, SxcoalPrice, MiningAuction, FailTrade
from .serializers import CategorySerializer, DatasetSerializer, DataPointSerializer, CustomMonthlyRawSerializer, CustomMonthlyExportSerializer, CustomMonthlyImportSerializer, CustomMonthlyImportSumSerializer, CustomMonthlyImportCustomSerializer, ExportDailySerializer, ImportDailySerializer, CurrencyMoveSerializer, FuelImportSerializer, SxcoalPriceSerializer, MiningAuctionSerializer, FailTradeSerializer
from .filters import CustomMonthlyRawFilter
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import  generics
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class DataPointViewSet(viewsets.ModelViewSet):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer

class CustomMonthlyRawPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to adjust page size
    max_page_size = 100  # Maximum page size limit

    def get_paginated_response(self, data):
        """Override to include pagination metadata."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

from django.db.models import Q

class CustomMonthlyRawListView(generics.ListAPIView):
    serializer_class = CustomMonthlyRawSerializer
    pagination_class = CustomMonthlyRawPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomMonthlyRawFilter  # keep if you already use it elsewhere

    def get_queryset(self):
        qs = CustomMonthlyRaw.objects.all()

        # year
        year = self.request.query_params.get('year')
        if year:
            years = [int(y) for y in year.split(',') if y.strip().isdigit()]
            if years:
                qs = qs.filter(year__in=years)

        # month
        month = self.request.query_params.get('month')
        if month:
            months = [m.zfill(2) for m in month.split(',') if m.strip()]
            if months:
                qs = qs.filter(month__in=months)

        # senderReceiver
        sender_receiver = self.request.query_params.get('senderReceiver')
        if sender_receiver:
            countries = [c.strip() for c in sender_receiver.split(',') if c.strip()]
            if countries:
                qs = qs.filter(senderReceiver__in=countries)

        # customs
        customs = self.request.query_params.get('customs')
        if customs:
            customs_list = [c.strip() for c in customs.split(',') if c.strip()]
            if customs_list:
                qs = qs.filter(customs__in=customs_list)

        # NEW: itemId (comma-separated list; exact match)
        item_id = self.request.query_params.get('itemId')
        if item_id:
            # allow numeric or string IDs
            ids = [s.strip() for s in item_id.split(',') if s.strip()]
            if ids:
                qs = qs.filter(itemId__in=ids)

        # NEW: itemName (partial match; supports multiple tokens with OR)
        item_name = self.request.query_params.get('itemName')
        if item_name:
            tokens = [t.strip() for t in item_name.split(',') if t.strip()]
            if tokens:
                q = Q()
                for t in tokens:
                    q |= Q(itemName__icontains=t)  # case-insensitive contains
                qs = qs.filter(q)

        # only needed fields
        qs = qs.only(
            "id", "companyName", "companyRegnum", "importExportFlag", "amountUSD",
            "quantity", "itemId", "itemName", "measure", "senderReceiver",
            "customs", "month", "year"
        ).order_by("id")

        return qs

class CustomMonthlyRawExportAPIView(APIView):
        def get(self, request):
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            flag = request.query_params.get('importExportFlag')
            filters = {}
            if year:
                filters['year'] = year
            if month:
                filters['month'] = month
            if flag:
                filters['importExportFlag'] = flag
            queryset = CustomMonthlyRaw.objects.filter(**filters)
            serializer = CustomMonthlyRawSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class CustomMonthlyRawGroupedAPIView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        flag = request.query_params.get('importExportFlag')
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        if flag:
            filters['importExportFlag'] = flag
        queryset = (
            CustomMonthlyRaw.objects.filter(**filters)
            .values('senderReceiver', 'itemId', 'itemName', 'measure')
            .annotate(
                SumOfquantity=Sum('quantity'),
                SumOfamountUSD=Sum('amountUSD')
            )
        )
        return Response(list(queryset), status=status.HTTP_200_OK)

class CustomMonthlyRawGroupByItemAPIView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        flag = request.query_params.get('importExportFlag')

        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        if flag:
            filters['importExportFlag'] = flag

        queryset = (
            CustomMonthlyRaw.objects.filter(**filters)
            .values('year', 'month', 'itemId', 'itemName', 'measure', 'senderReceiver')
            .annotate(
                SumOfquantity=Sum('quantity'),
                SumOfamountUSD=Sum('amountUSD')
            )
        )
        return Response(list(queryset), status=status.HTTP_200_OK)

class CustomMonthlyExportAPIView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        customs = request.query_params.get('customs')
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        if customs:
            customs_list = customs.split(',')
            filters['customs__in'] = customs_list
        queryset = CustomMonthlyExport.objects.filter(**filters)
        serializer = CustomMonthlyExportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomMonthlyImportSumAPIView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        queryset = CustomMonthlyImportSum.objects.filter(**filters)
        serializer = CustomMonthlyImportSumSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ImportMonthlyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomMonthlyImportListView(generics.ListAPIView):
    serializer_class = CustomMonthlyImportSerializer
    pagination_class = ImportMonthlyPagination
    filter_backends = [DjangoFilterBackend]
    queryset = CustomMonthlyImport.objects.none()  # Use get_queryset

    def get_queryset(self):
        qs = CustomMonthlyImport.objects.all()
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        country = self.request.query_params.get('senderReceiver')  # <-- Add this

        if year:
            years = [int(y) for y in year.split(',') if y.strip().isdigit()]
            if years:
                qs = qs.filter(year__in=years)
        if month:
            months = [m.zfill(2) for m in month.split(',') if m.strip()]
            if months:
                qs = qs.filter(month__in=months)
        if country:
            # Assumes codes (e.g. "MN,CN,RU"), change to .upper() if needed
            countries = [c.strip() for c in country.split(',') if c.strip()]
            if countries:
                qs = qs.filter(country__in=countries)

        qs = qs.only(
            "SumOfamountUSD", "itemId", "itemName", "measure", "SumOfquantity",
            "senderReceiver", "country", "month", "year"
        ).order_by("id")

        return qs  # Use id or your preferred ordering
class CustomMonthlyImportCustomAPIView(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        customs = request.query_params.get('customs')
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        if customs:
            filters['customs'] = customs
        queryset = CustomMonthlyImportCustom.objects.filter(**filters)
        serializer = CustomMonthlyImportCustomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExportDailyAPIView(APIView):
    def get(self, request):
        # Retrieve query params
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        # Prepare the filters
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month

        # Query primary database using the default manager (mof_daily)
        queryset_primary = ExportDaily.objects.using('mof_daily').filter(**filters)
        serializer_primary = ExportDailySerializer(queryset_primary, many=True)  # Fixed missing parenthesis

        # Combine data from the primary database (you can add secondary database querying here if needed)
        combined_data = {
            'primary_db_records': serializer_primary.data
        }
        # Return the combined data
        return Response(combined_data, status=status.HTTP_200_OK)

class ImportDailyAPIView(APIView):
    def get(self, request):
        # Retrieve query params
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        # Prepare the filters
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month

        # Query primary database using the default manager (mof_daily)
        queryset_primary = ImportDaily.objects.using('mof_daily').filter(**filters)
        serializer_primary = ImportDailySerializer(queryset_primary, many=True)  # Fixed missing parenthesis

        # Combine data from the primary database (you can add secondary database querying here if needed)
        combined_data = {
            'primary_db_records': serializer_primary.data
        }
        # Return the combined data
        return Response(combined_data, status=status.HTTP_200_OK)

class CurrencyMoveAPIView(APIView):
    def get(self, request):
        # Retrieve query params
        date = request.query_params.get('date')

        # Prepare the filters
        filters = {}
        if date:
            filters['date'] = date

        # Query primary database using the default manager (mof_daily)
        queryset_primary = CurrencyMove.objects.using('mof_daily').filter(**filters)
        serializer_primary = CurrencyMoveSerializer(queryset_primary, many=True)  # Fixed missing parenthesis

        # Combine data from the primary database (you can add secondary database querying here if needed)
        combined_data = {
            'primary_db_records': serializer_primary.data
        }
        # Return the combined data
        return Response(combined_data, status=status.HTTP_200_OK)

class FuelImportAPIView(APIView):
    def get(self, request):
        # Retrieve query params
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        # Prepare the filters
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month

        # Query primary database using the default manager (mof_daily)
        queryset_primary = FuelImport.objects.using('mof_daily').filter(**filters)
        serializer_primary = FuelImportSerializer(queryset_primary, many=True)  # Fixed missing parenthesis

        # Combine data from the primary database (you can add secondary database querying here if needed)
        combined_data = {
            'primary_db_records': serializer_primary.data
        }
        # Return the combined data
        return Response(combined_data, status=status.HTTP_200_OK)

class SxcoalPriceListView(generics.ListAPIView):
    serializer_class = SxcoalPriceSerializer
    queryset = SxcoalPrice.objects.using('mof_daily').all().order_by('date')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []  # Empty for now because we’ll implement custom filtering below

    def get_queryset(self):
        qs = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])
        elif start_date:
            qs = qs.filter(date__gte=start_date)
        elif end_date:
            qs = qs.filter(date__lte=end_date)
        return qs

class MiningAuctionAPIView(APIView):
    def get(self, request):
        # Retrieve query params
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        # Prepare the filters
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        # Query primary database using the default manager (mof_daily)
        queryset_primary = MiningAuction.objects.using('mof_daily').filter(**filters)
        serializer_primary = MiningAuctionSerializer(queryset_primary, many=True)  # Fixed missing parenthesis

        # Combine data from the primary database (you can add secondary database querying here if needed)
        combined_data = {
            'primary_db_records': serializer_primary.data
        }
        # Return the combined data
        return Response(combined_data, status=status.HTTP_200_OK)

class FailTradeAPIView(APIView):
    def get(self, request):
        # Retrieve query params
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        # Prepare the filters
        filters = {}
        if year:
            filters['year'] = year
        if month:
            filters['month'] = month
        # Query primary database using the default manager (mof_daily)
        queryset_primary = FailTrade.objects.using('mof_daily').filter(**filters)
        serializer_primary = FailTradeSerializer(queryset_primary, many=True)  # Fixed missing parenthesis

        # Combine data from the primary database (you can add secondary database querying here if needed)
        combined_data = {
            'primary_db_records': serializer_primary.data
        }
        # Return the combined data
        return Response(combined_data, status=status.HTTP_200_OK)