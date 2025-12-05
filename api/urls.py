from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DatasetViewSet, DataPointViewSet, CustomMonthlyRawExportAPIView, CustomMonthlyRawGroupedAPIView, CustomMonthlyRawGroupByItemAPIView, CustomMonthlyExportAPIView, CustomMonthlyImportSumAPIView, CustomMonthlyImportCustomAPIView, ExportDailyAPIView, ImportDailyAPIView, CurrencyMoveAPIView, FuelImportAPIView, SxcoalPriceListView, FailTradeAPIView, MiningAuctionAPIView, CustomMonthlyImportListView, CustomMonthlyRawListView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'datasets', DatasetViewSet)
router.register(r'datapoints', DataPointViewSet)

urlpatterns = [
    path('', include(router.urls)),  # all your ViewSet routes
    path('custom_monthly_adjusted/', CustomMonthlyRawExportAPIView.as_view(), name='custommonthlyyadjusted'),
    path('import_monthly_adjusted/', CustomMonthlyRawGroupedAPIView.as_view(), name='monthly-summary'),
    path('export_monthly/', CustomMonthlyExportAPIView.as_view(), name='export-monthly'),
    path('import_monthly_sum/', CustomMonthlyImportSumAPIView.as_view(), name='import-monthly-sum'),
    path('import_monthly/', CustomMonthlyImportListView.as_view(), name='import-monthly'),
    path('foreign_trade/', CustomMonthlyRawListView.as_view(), name='foreign-trade'),
    path('import_custom/', CustomMonthlyImportCustomAPIView.as_view(), name='import-custom'),
    path('monthly_groupby_item/', CustomMonthlyRawGroupByItemAPIView.as_view(), name='monthly-group-by-item'),
    path('export_daily/', ExportDailyAPIView.as_view(), name='export-daily'),
    path('import_daily/', ImportDailyAPIView.as_view(), name='import-daily'),
    path('currency_move/', CurrencyMoveAPIView.as_view(), name='import-daily'),
    path('fuel_import/', FuelImportAPIView.as_view(), name='fuel-import'),
    path('sxcoal_price/', SxcoalPriceListView.as_view(), name='sxcoal-price'),
    path('mining_auction/', MiningAuctionAPIView.as_view(), name='mining-auction'),
    path('fail_trades/', FailTradeAPIView.as_view(), name='fail-trades'),
]