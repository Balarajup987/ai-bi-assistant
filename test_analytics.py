from app.analytics import (
    get_total_revenue,
    get_top_product,
    get_region_sales,
    get_monthly_sales,
    analyze_sales
)

print("Revenue by region:")
print(analyze_sales(group_by="region"))

print("South region revenue:")
print(analyze_sales(filters={"region": "South"}))

print("Top 3 products:")
print(analyze_sales(group_by="product", limit=3))
print("Total Revenue:", get_total_revenue())
print("Top Product:", get_top_product())
print("Region Sales:", get_region_sales())
print("Monthly Sales:", get_monthly_sales())