import os

settings = {
    "LIDL_LANGUAGE": os.environ.get("LIDL_LANGUAGE", "de"),
    "LIDL_COUNTRY": os.environ.get("LIDL_COUNTRY", "DE"),
    "LIDL_REFRESH_TOKEN": os.environ.get("LIDL_REFRESH_TOKEN", "555XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX555"),
    "GROCY_URL": os.environ.get("GROCY_URL", "http://192.168.1.111"),
    "GROCY_PORT": os.environ.get("GROCY_PORT", 9283),
    "GROCY_API_KEY":  os.environ.get("GROCY_API_KEY", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"),
    "RUN_INTERVAL": int(os.environ.get("RUN_INTERVAL", 1800)), # Seconds

    "GROCY_LOCATION_ID": os.environ.get("GROCY_LOCATION_ID", 2),
    "GROCY_DEFAULT_CONSUME_LOCATION": os.environ.get("GROCY_LOCATION_ID", 1),
    # Called "Store" in Grocy, https://demo.grocy.info/shoppinglocations
    "GROCY_SHOPPING_LOCATION_ID": os.environ.get("GROCY_SHOPPING_LOCATION_ID", 1),
    "GROCY_DEFAULT_BEST_BEFORE_DAYS": os.environ.get("GROCY_DEFAULT_BEST_BEFORE_DAYS", 5),
    "GROCY_DEFAULT_BEST_BEFORE_DAYS_AFTER_THAWING": os.environ.get("GROCY_DEFAULT_BEST_BEFORE_DAYS_AFTER_THAWING", 0),
    "GROCY_PRODUCT_GROUP_ID":  os.environ.get("GROCY_PRODUCT_GROUP_ID", None),
    "GROCY_QU_ID_STOCK":  os.environ.get("GROCY_QU_ID_STOCK", 2),
    "GROCY_QU_ID_PURCHASE":  os.environ.get("GROCY_QU_ID_PURCHASE", 3),
    "GROCY_QU_ID_CONSUME":  os.environ.get("GROCY_QU_ID_CONSUME", 2),
    "GROCY_QU_ID_PRICE":  os.environ.get("GROCY_QU_ID_PRICE", 3)
}
