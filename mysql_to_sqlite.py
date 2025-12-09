import sqlite3
import mysql.connector
from decimal import Decimal

def norm(v):
    """sqlite3-д таарах төрөл рүү хөрвүүлнэ."""
    if isinstance(v, Decimal):
        return float(v)   # хүсвэл str(v) гэж хадгалж болно
    return v

# -------------------------------
#  MySQL CONNECTION
# -------------------------------
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Med@admin2023",       # нууц үгтэй бол энд бичээрэй
    database="mof_customs",
)

mysql_cursor = mysql_conn.cursor(dictionary=True)

# MySQL талаас бүх мөрийг авах
mysql_cursor.execute("SELECT * FROM custom_monthly_export_e")
rows = mysql_cursor.fetchall()
print(f"MySQL → fetched rows: {len(rows)}")


# -------------------------------
#  SQLITE CONNECTION
# -------------------------------
sqlite_conn = sqlite3.connect("db.sqlite3")
sqlite_cursor = sqlite_conn.cursor()

# Хуучин data устгах (хэрвээ цэвэрлээд эхлэх бол)
sqlite_cursor.execute("DELETE FROM custom_monthly_export_e")


# -------------------------------
#  INSERT LOOP
# -------------------------------
insert_sql = """
INSERT INTO custom_monthly_export_e (
    id,
    amountUSD,
    companyName,
    companyRegnum,
    customs,
    itemId,
    importExportFlag,
    itemName,
    measure,
    month,
    quantity,
    senderReceiver,
    year,
    country
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

count = 0

for r in rows:
    sqlite_cursor.execute(
        insert_sql,
        (
            norm(r["id"]),
            norm(r["amountUSD"]),
            r["companyName"],
            r["companyRegnum"],
            r["customs"],
            r["itemId"],
            r["importExportFlag"],
            r["itemName"],
            r["measure"],
            r["month"],
            norm(r["quantity"]),
            r["senderReceiver"],
            norm(r["year"]),
            r["country"],
        ),
    )
    count += 1

sqlite_conn.commit()

mysql_cursor.close()
mysql_conn.close()
sqlite_conn.close()

print(f"SUCCESS: {count} rows migrated from MySQL → SQLite (custom_monthly_export_e).")