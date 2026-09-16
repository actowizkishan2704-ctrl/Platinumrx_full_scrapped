import mysql.connector as my_conn
from platinumrx_healthproducts.items import PlatinumrxPDP
import json


def db_connection():
    conn = my_conn.connect(
        host="localhost",
        user="root",
        password="actowiz"
    )
    cursor = conn.cursor()
    return cursor, conn


def create_database():
    cursor, conn = db_connection()
    cursor.execute("CREATE DATABASE IF NOT EXISTS platinumrx")
    conn.commit()
    cursor.close()
    conn.close()
    conn = my_conn.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="platinumrx"
    )
    cursor = conn.cursor()
    return cursor, conn

def create_table():
    cursor, conn = create_database()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS platinumrx_healthproduct_PDP (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name TEXT,
            product_sku VARCHAR(255),
            product_url TEXT,
            product_img_url TEXT,
            product_category VARCHAR(255),
            product_salt_composition TEXT,
            product_manufacturer VARCHAR(255),
            product_manufacturer_address TEXT,
            product_pack_size VARCHAR(255),
            product_description TEXT,
            product_summary TEXT,
            product_mrp DECIMAL(10,2),
            product_price_per_unit DECIMAL(10,2),
            product_availability VARCHAR(255),
            product_at_pincode VARCHAR(50),
            product_certified VARCHAR(255),
            product_expiry VARCHAR(255),
            product_return VARCHAR(255),
            product_benefits TEXT,
            product_uses TEXT,
            product_direction_of_use TEXT,
            product_how_it_works TEXT,
            product_daily_dose TEXT,
            product_side_effects TEXT,
            product_safety TEXT,
            product_quick_tips TEXT,
            product_storage_advice TEXT,
            product_overdose TEXT,
            product_missed_dose TEXT,
            product_drug_food_interaction TEXT,
            product_drug_interaction TEXT,
            product_drug_disease_interaction TEXT,
            product_fact JSON,
            product_disclaimer TEXT,
            product_reference_url JSON,
            compared_products JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return cursor, conn


class PlatinumrxHealthproductsPipeline:
    def open_spider(self, spider):
        cursor, conn = create_table()
        cursor.close()
        conn.close()


    def process_item(self, item, spider):
        if isinstance(item, PlatinumrxPDP):
            cursor, conn = create_table()
            product_fact = item.get("product_fact")
            if product_fact is not None:
                product_fact = json.dumps(product_fact)
            product_reference_url = item.get("product_reference_url")
            if product_reference_url is not None:
                product_reference_url = json.dumps(product_reference_url)
            compared_products = item.get("compared_products")
            if compared_products is not None:
                compared_products = json.dumps(compared_products)

            cursor.execute("""
                INSERT INTO platinumrx_healthproduct_PDP (
                    product_name,
                    product_sku,
                    product_url,
                    product_img_url,
                    product_category,
                    product_salt_composition,
                    product_manufacturer,
                    product_manufacturer_address,
                    product_pack_size,
                    product_description,
                    product_summary,
                    product_mrp,
                    product_price_per_unit,
                    product_availability,
                    product_at_pincode,
                    product_certified,
                    product_expiry,
                    product_return,
                    product_benefits,
                    product_uses,
                    product_direction_of_use,
                    product_how_it_works,
                    product_daily_dose,
                    product_side_effects,
                    product_safety,
                    product_quick_tips,
                    product_storage_advice,
                    product_overdose,
                    product_missed_dose,
                    product_drug_food_interaction,
                    product_drug_interaction,
                    product_drug_disease_interaction,
                    product_fact,
                    product_disclaimer,
                    product_reference_url,
                    compared_products
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

                ON DUPLICATE KEY UPDATE
                    product_name = VALUES(product_name),
                    product_sku = VALUES(product_sku),
                    product_url = VALUES(product_url),
                    product_img_url = VALUES(product_img_url),
                    product_category = VALUES(product_category),
                    product_salt_composition = VALUES(product_salt_composition),
                    product_manufacturer = VALUES(product_manufacturer),
                    product_manufacturer_address =VALUES(product_manufacturer_address),
                    product_pack_size = VALUES(product_pack_size),
                    product_description = VALUES(product_description),
                    product_summary = VALUES(product_summary),
                    product_mrp = VALUES(product_mrp),
                    product_price_per_unit =VALUES(product_price_per_unit),
                    product_availability =VALUES(product_availability),
                    product_at_pincode =VALUES(product_at_pincode),
                    product_certified = VALUES(product_certified),
                    product_expiry = VALUES(product_expiry),
                    product_return = VALUES(product_return),
                    product_benefits = VALUES(product_benefits),
                    product_uses = VALUES(product_uses),
                    product_direction_of_use =VALUES(product_direction_of_use),
                    product_how_it_works =VALUES(product_how_it_works),
                    product_daily_dose =VALUES(product_daily_dose),
                    product_side_effects =VALUES(product_side_effects),
                    product_safety =VALUES(product_safety),
                    product_quick_tips =VALUES(product_quick_tips),
                    product_storage_advice =VALUES(product_storage_advice),
                    product_overdose =VALUES(product_overdose),
                    product_missed_dose =VALUES(product_missed_dose),
                    product_drug_food_interaction =VALUES(product_drug_food_interaction),
                    product_drug_interaction =VALUES(product_drug_interaction),
                    product_drug_disease_interaction =VALUES(product_drug_disease_interaction),
                    product_fact = VALUES(product_fact),
                    product_disclaimer =VALUES(product_disclaimer),
                    product_reference_url = VALUES(product_reference_url),
                    compared_products = VALUES(compared_products)
            """,
            (
                item.get("product_name"),
                item.get("product_sku"),
                item.get("product_url"),
                item.get("product_img_url"),
                item.get("product_category"),
                item.get("product_salt_composition"),
                item.get("product_manufacturer"),
                item.get("product_manufacturer_address"),
                item.get("product_pack_size"),
                item.get("product_description"),
                item.get("product_summary"),
                item.get("product_mrp"),
                item.get("product_price_per_unit"),
                item.get("product_availability"),
                item.get("product_at_pincode"),
                item.get("product_certified"),
                item.get("product_expiry"),
                item.get("product_return"),
                item.get("product_benefits"),
                item.get("product_uses"),
                item.get("product_direction_of_use"),
                item.get("product_how_it_works"),
                item.get("product_daily_dose"),
                item.get("product_side_effects"),
                item.get("product_safety"),
                item.get("product_quick_tips"),
                item.get("product_storage_advice"),
                item.get("product_overdose"),
                item.get("product_missed_dose"),
                item.get("product_drug_food_interaction"),
                item.get("product_drug_interaction"),
                item.get("product_drug_disease_interaction"),
                product_fact,
                item.get("product_disclaimer"),
                product_reference_url,
                compared_products
            ))
            conn.commit()
            cursor.close()
            conn.close()
        return item