from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'api_category'
        managed = False

class Dataset(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'api_dataset'
        managed = False

class DataPoint(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    year = models.IntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'api_datapoint'
        managed = False
class CustomMonthlyRaw(models.Model):
    id = models.AutoField(primary_key=True)
    amountUSD = models.DecimalField(max_digits=65, decimal_places=2)
    companyCNumber = models.CharField(max_length=765)
    companyName = models.CharField(max_length=765)
    companyRegnum = models.CharField(max_length=60)
    customs = models.CharField(max_length=765, db_index=True)  # Added index
    downloadDate = models.DateTimeField()
    itemId = models.CharField(max_length=30)
    importExportFlag = models.CharField(max_length=3)
    itemName = models.TextField()
    measure = models.CharField(max_length=135)
    month = models.CharField(max_length=2, db_index=True)  # Added index
    quantity = models.DecimalField(max_digits=65, decimal_places=2)
    senderReceiver = models.CharField(max_length=9, db_index=True)  # Added index
    statYearMonth = models.CharField(max_length=30)
    year = models.IntegerField(db_index=True)  # Added index

    class Meta:
        db_table = 'custom_monthly_raw'
        managed = True
        indexes = [
            models.Index(fields=['year', 'month']),  # Composite index for filtering by year and month
            models.Index(fields=['senderReceiver', 'customs']),  # Composite index for filtering by senderReceiver and customs
        ]

class CustomMonthlyExport(models.Model):
    id = models.IntegerField(primary_key=True)  # <- add this line
    amountUSD = models.DecimalField(max_digits=65, decimal_places=2)
    companyName = models.CharField(max_length=765)
    companyRegnum = models.CharField(max_length=60)
    customs = models.CharField(max_length=765)
    itemId = models.CharField(max_length=30)
    importExportFlag = models.CharField(max_length=3)
    itemName = models.TextField()
    measure = models.CharField(max_length=135)
    month = models.CharField(max_length=6)
    quantity = models.DecimalField(max_digits=65, decimal_places=2)
    senderReceiver = models.CharField(max_length=9)
    year = models.IntegerField()
    country = models.TextField()

    class Meta:
        db_table = 'custom_monthly_export_e'
        managed = True

class CustomMonthlyImport(models.Model) :
    id = models.IntegerField(primary_key=True)
    SumOfamountUSD = models.DecimalField(max_digits=65, decimal_places=2)
    itemId = models.CharField(max_length=30)
    itemName = models.TextField()
    measure = models.CharField(max_length=135)
    SumOfquantity = models.DecimalField(max_digits=65, decimal_places=2)
    senderReceiver = models.CharField(max_length=9)
    country = models.TextField()
    month = models.CharField(max_length=2, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'custom_monthly_import_summary'
        managed = True  # This means Django will NOT manage/migrate this table!
        indexes = [
            models.Index(fields=['year', 'month'], name='idx_year_month'),
        ]

class CustomMonthlyImportSum(models.Model) :
    id = models.IntegerField(primary_key=True)
    SumOfamountUSD = models.DecimalField(max_digits=65, decimal_places=2)
    itemId = models.CharField(max_length=30)
    itemName = models.TextField()
    measure = models.CharField(max_length=135)
    SumOfquantity = models.DecimalField(max_digits=65, decimal_places=2)
    year = models.IntegerField()
    month = models.CharField(max_length=2)
    class Meta:
        db_table = 'custom_monthly_import_summary_all'
        managed = True

class CustomMonthlyImportCustom(models.Model) :
    id = models.IntegerField(primary_key=True)
    SumOfamountUSD = models.DecimalField(max_digits=65, decimal_places=2)
    itemId = models.CharField(max_length=30)
    itemName = models.TextField()
    measure = models.CharField(max_length=135)
    SumOfquantity = models.DecimalField(max_digits=65, decimal_places=2)
    customs = models.TextField()
    month = models.CharField(max_length=2)
    year = models.IntegerField()
    class Meta:
        db_table = 'custom_monthly_import_custom'
        managed = True

class CustomMonthlyImportCustom(models.Model) :
    id = models.IntegerField(primary_key=True)
    SumOfamountUSD = models.DecimalField(max_digits=65, decimal_places=2)
    itemId = models.CharField(max_length=30)
    itemName = models.TextField()
    measure = models.CharField(max_length=135)
    SumOfquantity = models.DecimalField(max_digits=65, decimal_places=2)
    customs = models.TextField()
    month = models.CharField(max_length=2)
    year = models.IntegerField()
    class Meta:
        db_table = 'custom_monthly_import_custom'
        managed = True

class ExportDaily(models.Model):
    date = models.DateField(null=True, blank=True)
    code_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    code_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    code_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    code_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    value_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    value_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    value_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    value_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    quarter = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    avg7_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    avg7_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    avg7_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    avg7_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    cumulative_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    cumulative_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    cumulative_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    cumulative_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_avg7_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_avg7_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_avg7_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_avg7_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_month_avg_2601 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_month_avg_2603 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_month_avg_2701 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    price_month_avg_2709 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'export_data'
        managed = True  # Prevents Django from creating the table

class ImportDaily(models.Model):
    date = models.DateField(unique=True)  # Ensures uniqueness based on the date field
    total_import = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    food_products = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    oil_products = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    vehicles = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    others = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_import_today = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    food_products_today = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    oil_products_today = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    vehicles_today = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    others_today = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    quarter = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    total_import_7d_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    food_products_7d_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    oil_products_7d_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    vehicles_7d_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    others_7d_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    total_import_month_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    food_products_month_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    oil_products_month_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    vehicles_month_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    others_month_avg = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'import_data'  # The name of the table in the database
        managed = False

class CurrencyMove(models.Model):
    date = models.DateField(unique=True)  # Ensures uniqueness based on the date field
    official_rate = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    daily_change = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'currency_change'  # The name of the table in the database
        managed = False # Prevents Django from creating the table

class FuelImport(models.Model):
    date = models.DateField(unique=True)  # Ensures uniqueness based on the date field
    a80 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ai92 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ai95 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    diesel_winter = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    diesel_summer = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    diesel = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    quarter = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    avg_a80 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    avg_ai92 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    avg_ai95 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    avg_diesel = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_a80 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_ai92 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_ai95 = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    month_avg_diesel = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'fuel_prices'  # The name of the table in the database
        managed = False


class SxcoalPrice(models.Model):
    date = models.DateField(unique=True)  # Ensures uniqueness based on the date field
    raw_coking_coal = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    washed_coking_coal = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    usd_rate = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)
    cny_rate = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'sxcoal_price'  # The name of the table in the database
        managed = False

class MiningAuction(models.Model):
    trade_date = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    weekday = models.CharField(max_length=10, null=True, blank=True)
    trade_type = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    seller = models.CharField(max_length=100, null=True, blank=True)
    product_name_type = models.CharField(max_length=100, null=True, blank=True)
    quantity_ton = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    asking_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deal_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    price_growth = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    prev_day_mnt_bank_rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    prev_day_usd_rate = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    asking_price_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    deal_price_usd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    asking_total_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    deal_total_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    amount_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_amount_currency = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    amount_mnt = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    extra_income_usd = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    coal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    iron = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    copper = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    fluorspar = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'trades'  # The name of the table in the database
        managed = False

class FailTrade(models.Model):
    trade_date = models.DateField(null=True, blank=True)  # The trade date, nullable
    year = models.IntegerField(null=True, blank=True)  # The year, nullable
    month = models.IntegerField(null=True, blank=True)  # The month, nullable
    day = models.IntegerField(null=True, blank=True)  # The day, nullable
    weekday = models.CharField(max_length=16, null=True, blank=True)  # Day of the week, optional
    trade_type = models.CharField(max_length=32, null=True, blank=True)  # Type of trade, optional
    type = models.CharField(max_length=32, null=True, blank=True)  # Type of product, optional
    seller = models.CharField(max_length=128, null=True, blank=True)  # Seller's name, optional
    product_name_type = models.CharField(max_length=128, null=True, blank=True)  # Product name and type, optional
    quantity_ton = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)  # Quantity in tons, nullable
    asking_price = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)  # Asking price, nullable
    currency = models.CharField(max_length=8, null=True, blank=True)  # Currency type, optional
    prev_day_mnt_bank_rate = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)  # Previous day's bank rate, optional
    prev_day_usd_rate = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True)  # Previous day's USD rate, optional
    asking_price_usd = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)  # Asking price in USD, optional
    asking_total_usd = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)  # Total asking price in USD, optional
    asking_total_currency = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)  # Total asking price in original currency, optional
    note = models.CharField(max_length=255, null=True, blank=True)  # Optional note field

    class Meta:
        db_table = 'failed_trades'  # The name of the table in the database
        managed = False