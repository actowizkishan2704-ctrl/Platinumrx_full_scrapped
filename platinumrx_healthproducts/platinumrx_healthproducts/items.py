# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlatinumrxHealthproductsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_url=scrapy.Field()


class PlatinumrxPDP(scrapy.Item):
    product_name = scrapy.Field()
    product_sku = scrapy.Field()
    product_url = scrapy.Field()
    product_img_url = scrapy.Field()
    product_category = scrapy.Field()
    product_salt_composition = scrapy.Field()
    product_manufacturer = scrapy.Field()
    product_manufacturer_address = scrapy.Field()
    product_pack_size = scrapy.Field()
    product_description = scrapy.Field()
    product_summary = scrapy.Field()
    product_mrp = scrapy.Field()
    product_price_per_unit = scrapy.Field()
    product_availability = scrapy.Field()
    product_at_pincode = scrapy.Field()
    product_certified = scrapy.Field()
    product_expiry = scrapy.Field()
    product_return = scrapy.Field()
    product_benefits = scrapy.Field()
    product_uses = scrapy.Field()
    product_direction_of_use = scrapy.Field()
    product_how_it_works = scrapy.Field()
    product_daily_dose = scrapy.Field()
    product_side_effects = scrapy.Field()
    product_safety = scrapy.Field()
    product_quick_tips = scrapy.Field()
    product_storage_advice = scrapy.Field()
    product_overdose = scrapy.Field()
    product_missed_dose = scrapy.Field()
    product_drug_food_interaction = scrapy.Field()
    product_drug_interaction = scrapy.Field()
    product_drug_disease_interaction = scrapy.Field()
    product_fact = scrapy.Field()
    product_disclaimer = scrapy.Field()
    product_reference_url = scrapy.Field()
    compared_products = scrapy.Field()