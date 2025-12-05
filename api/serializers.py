from rest_framework import serializers
from .models import Category, Dataset, DataPoint, CustomMonthlyRaw, CustomMonthlyExport, CustomMonthlyImport, CustomMonthlyImportSum, CustomMonthlyImportCustom, ExportDaily, ImportDaily, CurrencyMove, FuelImport, SxcoalPrice, MiningAuction, FailTrade

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'

class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = '__all__'

class CustomMonthlyRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMonthlyRaw
        fields = [
            "id", "companyName", "companyRegnum", "importExportFlag", "amountUSD",
            "quantity", "itemId", "itemName", "measure", "senderReceiver",
            "customs", "month", "year"
        ]


class CustomMonthlyAdjustedRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMonthlyRaw
        fields = [
            'year', 'month', 'itemId', 'itemName', 'importExportFlag', 'customs',
            'senderReceiver', 'companyRegnum', 'companyName', 'measure', 'quantity', 'amountUSD'
        ]
class CustomMonthlyExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMonthlyExport
        fields = '__all__'

class CustomMonthlyImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMonthlyImport
        fields = '__all__'

class CustomMonthlyImportSumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMonthlyImportSum
        fields = '__all__'

class CustomMonthlyImportCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMonthlyImportCustom
        fields = '__all__'

class ExportDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportDaily
        fields = '__all__'

class ImportDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportDaily
        fields = '__all__'
class CurrencyMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyMove
        fields = '__all__'
class FuelImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelImport
        fields = '__all__'
class SxcoalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SxcoalPrice
        fields = '__all__'

class MiningAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiningAuction
        fields = '__all__'

class FailTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailTrade
        fields = '__all__'