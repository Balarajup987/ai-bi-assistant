
from app.analytics import analyze_sales

print("\n1. Revenue by region")
print(analyze_sales(group_by="region"))

print("\n2. South region revenue")
print(analyze_sales(filters={"region": "South"}))

print("\n3. Top 3 products")
print(analyze_sales(
    group_by="product",
    sort="desc",
    limit=3
))

print("\n4. Lowest revenue region")
print(analyze_sales(
    group_by="region",
    sort="asc",
    limit=1
))

print("\n5. Monthly revenue")
print(analyze_sales(group_by="month"))
