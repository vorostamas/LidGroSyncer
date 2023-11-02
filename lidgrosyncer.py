import json
import time
import os
import logging
import sys


from settings import settings
from datetime import datetime, timedelta
from lidlplus import LidlPlusApi
from pygrocy import Grocy, EntityType
from pygrocy.errors import GrocyError

LIDL_LANGUAGE = settings["LIDL_LANGUAGE"]
LIDL_COUNTRY = settings["LIDL_COUNTRY"]
LIDL_REFRESH_TOKEN = settings["LIDL_REFRESH_TOKEN"]
PROCESS_ONLY_FAVORITES = settings["PROCESS_ONLY_FAVORITES"]

GROCY_URL = settings["GROCY_URL"]
GROCY_PORT = settings["GROCY_PORT"]
GROCY_API_KEY = settings["GROCY_API_KEY"]
RUN_INTERVAL = settings["RUN_INTERVAL"]
PROCESSED_IDS_FILE = "processed_ids.txt"

location_id = settings["GROCY_LOCATION_ID"]
default_consume_location_id = settings["GROCY_LOCATION_ID"]
grocy_shopping_location_id = settings["GROCY_SHOPPING_LOCATION_ID"]
default_best_before_days = settings["GROCY_DEFAULT_BEST_BEFORE_DAYS"]
default_best_before_days_after_thawing = settings[
    "GROCY_DEFAULT_BEST_BEFORE_DAYS_AFTER_THAWING"
]
product_group_id = settings["GROCY_PRODUCT_GROUP_ID"]
qu_id_stock = settings["GROCY_QU_ID_STOCK"]
qu_id_purchase = settings["GROCY_QU_ID_PURCHASE"]
qu_id_consume = settings["GROCY_QU_ID_CONSUME"]
qu_id_price = settings["GROCY_QU_ID_PRICE"]


def load_processed_ids():
    try:
        with open(PROCESSED_IDS_FILE, "r") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()


def mark_receipt_processed(id):
    with open(PROCESSED_IDS_FILE, "a") as file:
        file.write(id + "\n")


def get_product_by_barcode(barcode):
    try:
        return grocy.product_by_barcode(barcode)
    except:
        return None


def save_receipt(receipt):
    receipts_folder = "receipts"
    if not os.path.exists(receipts_folder):
        os.makedirs(receipts_folder)
    with open(f"{receipts_folder}/{receipt['id']}.json", "w", encoding="utf8") as f:
        json.dump(receipt, f, ensure_ascii=False)


def create_best_before_date(purchase_date):
    date_object = datetime.strptime(purchase_date, "%Y-%m-%dT%H:%M:%S")
    return date_object + timedelta(days=default_best_before_days)


def purchase_product(product_id, amount, price, date, name=None):
    best_before_date = create_best_before_date(date)
    amount = float(amount.replace(",", "."))
    price = float(price.replace(",", "."))
    _LOGGER.info(
        f"Purchasing product: product_id: {product_id}, name:{name} amount:{amount}, price:{price}, best_before_date: {best_before_date}"
    )
    try:
        grocy.add_product(product_id, amount, price, best_before_date)
    except GrocyError as error:
        _LOGGER.error("Error during product purchase, message: %s", error.message)
        raise Exception("Purchase error: ", error)


def create_new_product(name):
    _LOGGER.info("Creating new product " + name)
    payload = {
        "name": name,
        "active": "1",
        "description": "Automatically created by LidGroSyncer",
        "location_id": location_id,
        "default_consume_location_id": default_consume_location_id,
        "shopping_location_id": grocy_shopping_location_id,
        "min_stock_amount": "0",
        "treat_opened_as_out_of_stock": "1",
        "due_type": "1",
        "default_best_before_days": default_best_before_days,
        "default_best_before_days_after_open": "0",
        "default_best_before_days_after_freezing": "0",
        "default_best_before_days_after_thawing": default_best_before_days_after_thawing,
        "product_group_id": product_group_id,
        "qu_id_stock": qu_id_stock,
        "qu_id_purchase": qu_id_purchase,
        "qu_id_consume": qu_id_consume,
        "qu_id_price": qu_id_price,
        "calories": "0",
        "quick_consume_amount": "1",
        "quick_open_amount": "1",
        "move_on_open": "0",
        "cumulate_min_stock_amount_of_sub_products": "0",
        "should_not_be_frozen": "0",
        "enable_tare_weight_handling": "0",
        "not_check_stock_fulfillment_for_recipes": "0",
        "hide_on_stock_overview": "0",
        "no_own_stock": "0",
        "parent_product_id": "",
    }

    # Prevent creating a product with an existing product name
    get_product_by_name = grocy.get_generic_objects_for_type(
        EntityType.PRODUCTS, [f"name={name}"]
    )
    if not get_product_by_name:
        _LOGGER.info(name + " is not in product names, creating new product")
        return grocy.add_generic(entity_type=EntityType.PRODUCTS, data=payload)[
            "created_object_id"
        ]
    else:
        return get_product_by_name[0]["id"]


def add_barcode(product_id, barcode):
    payload = {
        "product_id": product_id,
        "barcode": barcode,
        "amount": "1",
        "shopping_location_id": grocy_shopping_location_id,
        "note": "Automatically added by LidGroSyncer",
        "qu_id": "1",
    }
    try:
        return grocy.add_generic(entity_type=EntityType.PRODUCT_BARCODES, data=payload)[
            "created_object_id"
        ]
    except GrocyError as error:
        _LOGGER.error("Error during barcode creation, message: %s", error.message)
        raise Exception("Barcode creation exception: ", error)


def purchase_products(receipt):
    _LOGGER.info(f"Processing ticket with id {receipt['id']}")
    for item in receipt["itemsLine"]:
        name = item["name"]
        _LOGGER.debug(f"Product name: {name}, amount: {item['quantity']}")
        barcode = item["codeInput"]
        product = get_product_by_barcode(barcode)

        if product is None:
            product_id = create_new_product(name)
            add_barcode(product_id, barcode)
        else:
            product_id = product.id

        amount = item["quantity"]
        price = item["currentUnitPrice"]
        date = receipt["date"]
        purchase_product(product_id, amount, price, date, name)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

lidl = LidlPlusApi(LIDL_LANGUAGE, LIDL_COUNTRY, LIDL_REFRESH_TOKEN)
grocy = Grocy(base_url=GROCY_URL, api_key=GROCY_API_KEY, port=GROCY_PORT)


def get_generic_object_ids(entity_type: EntityType, filename: str):
    objects = grocy.get_generic_objects_for_type(entity_type)
    with open(filename, "w") as file:
        for object in objects:
            file.write(f"Name: {object['name']}, ID: {object['id']} \n")


def process_receipts():
    processed_ids = load_processed_ids()
    for ticket in lidl.tickets(only_favorite=PROCESS_ONLY_FAVORITES):
        receipt_id = ticket["id"]
        if receipt_id not in processed_ids:
            receipt = lidl.ticket(receipt_id)
            save_receipt(receipt)
            purchase_products(receipt)
            mark_receipt_processed(receipt_id)
        else:
            _LOGGER.info(f"Skipping {receipt_id} because it's already processed")


while True:
    process_receipts()
    _LOGGER.info(f"Sleeping for {RUN_INTERVAL} seconds")
    time.sleep(RUN_INTERVAL)
