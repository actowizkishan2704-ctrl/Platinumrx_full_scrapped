import scrapy
from platinumrx.pipelines import create_table
from platinumrx.items import PlatinumrxPDP
from rich import print
import re
import json
import jmespath


class ParserSpider(scrapy.Spider):
    name = "parser"
    allowed_domains = ["www.platinumrx.in"]
    def start_requests(self):
        cursor,conn=create_table()
        from_cid = int(getattr(self, "from_id", 1))
        to_cid = int(getattr(self, "to_id", 421321))
        cursor.execute("""SELECT id, products_urls FROM platinumrx_products_url WHERE status = 0 AND id BETWEEN %s AND %s ORDER BY id""",(from_cid, to_cid))
        urls = cursor.fetchall()
        cursor.close()
        conn.close()
        cookies = {
            'platinumrx-device-id': 'c4f4d87f-86e8-4a88-87b4-e7a45cecb06c',
            'platinumrx-session-id': '03847e4a-2084-4150-87c8-025d9b71066a',
            '_gcl_au': '1.1.1386912106.1789029224',
            '_ga': 'GA1.1.1020510031.1789029225',
            '_ga_BHBBVCGVE0': 'GS2.1.s1789105050$o4$g1$t1789106254$j60$l0$h801576389$da4THJHUtYw8-09PKcD8CrqgcohCDFd1nIw',
            '_dd_s_v2': 'aid=47a24d2b-491d-423a-9130-315a19c20816&id=6f6821bc-e994-4cdc-a81a-f6343d5f0893&created=1789100800476&expire=1789107159281&c=0',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,gu;q=0.8,bho;q=0.7,so;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
        }
        for id, url in urls:
            new_url = url.replace("/product-display/","/medicines/")
            yield scrapy.Request(url=new_url,headers=headers,cookies=cookies,callback=self.parse,meta={"id": id})

    def parse(self, response):
        print(response.url, "...")
        ids = response.meta["id"]
        json_data = response.xpath("//script[@type='application/ld+json'][contains(., 'Product')]/text()").get()
        if not json_data:
            return
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return
        
        product_price = jmespath.search("additionalProperty[?name=='MRP'].value | [0]",data)
        if product_price:
            try:
                product_price = float(product_price.replace("₹", "").strip())
            except (ValueError, TypeError):
                product_price = None
        else:
            product_price = None  
        product_pack_size = jmespath.search("additionalProperty[?name=='Pack Size'].value | [0]",data) or None
        product_availabilty = jmespath.search("additionalProperty[?name=='Availability'].value | [0]",data) or None
        product_menufacturer = jmespath.search("manufacturer.name",data) or None
        product_name = jmespath.search("name",data) or None
        product_img_url = jmespath.search("image",data) or None
        prodcut_description = jmespath.search("description",data) or None
        prodcut_SKU = jmespath.search("sku",data) or None
        product_url = jmespath.search("url",data) or None
        product_salt_composition = jmespath.search("activeIngredient",data) or None
        price_per_unit_text = "".join(response.xpath("//span[contains(string(), '/ Unit')]//text()").getall())
        price_per_unit_text = (price_per_unit_text.replace("/ Unit", "").replace("₹", "").strip())
        match = re.search(r'\d+(?:\.\d+)?',price_per_unit_text)
        if match:
            price_per_unit = float(match.group(0))
        else:
            price_per_unit = None
        product_price_per_unit = price_per_unit
        related_products = jmespath.search("isRelatedTo",data)
        compared_products = []
        if related_products:
            if isinstance(related_products, dict):
                related_products = [related_products]
            if isinstance(related_products, list):
                for product in related_products:
                    compared_price = jmespath.search("offers.price",product)
                    if compared_price is not None:
                        try:
                            compared_price = float(compared_price)
                        except (ValueError, TypeError):
                            compared_price = None
                    compared_product = {
                        "product_name": product.get("name"),
                        "product_url": product.get("url"),
                        "product_img_url": product.get("image"),
                        "product_manufacturer": jmespath.search("manufacturer.name",product),
                        "product_salt_composition": product.get("activeIngredient"),
                        "product_pack_size": response.xpath("//div[@data-testid='pdp-card-substitute-pack-size']/text()").get(),
                        "product_price_per_unit": price_per_unit,
                        "product_price": compared_price
                    }
                    compared_products.append(compared_product)
        if not compared_products:
            compared_products = None
        product_category ="Medecines"
        product_at_pincode = response.xpath("//p[@data-testid='pdp-edd-pincode-value']/text()").get() or None
        product_certified = response.xpath("//div[@data-testid='pdp-hero-trust-badge-fda-&-gmp-certified']//p/text()").get() or None
        product_expiry = response.xpath("//div[@data-testid='pdp-hero-trust-badge-long-expiry-(>8-months)']//p/text()").get() or None
        product_return = response.xpath("//div[@data-testid='pdp-hero-trust-badge-15-days-easy-returns']//p/text()").get() or None
        product_summary = ''.join(response.xpath("//div[@id='short-description']//p//text()").getall()) or None
        product_benefits = ''.join(response.xpath('//div[@data-slot="section-benefits"]//p//text()').getall()) or None
        product_side_effects = ''.join(response.xpath('//div[@data-slot="section-side-effects"]//div[@data-slot="section-content"]//text()').getall()) or None
        product_uses = ' '.join(response.xpath('//div[@data-slot="section-uses"]//div[@data-slot="section-content"]//*[self::p or self::li]//text()').getall()).strip() or None
        product_direction_of_use = ' '.join(x.strip() for x in response.xpath('//div[@data-slot="section-direction-of-use"]//div[@data-slot="section-content"]//*[self::p or self::li]//text()').getall()if x.strip()) or None
        product_how_it_works = ' '.join(x.strip()for x in response.xpath('//div[@data-slot="section-how-it-works"]//div[@data-slot="section-content"]//p//text()').getall() if x.strip()) or None
        product_safety = ' '.join(x.xpath('normalize-space(.)').get()for x in response.xpath('//div[@data-slot="section-safety-advice"]//p')if x.xpath('normalize-space(.)').get()) or None
        product_quick_tips = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-quick-tips"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_storage_advice = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-storage"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_drug_food_interaction = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-drug-food-interaction"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_drug_interaction = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-testid="pdp-description-section-drug-drug-interaction"]''//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_drug_disease_interaction = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-drug-disease-interactions"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_daily_dose = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-daily-dose"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_manufacturer_address = ' '.join( x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-manufacturer-address"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_disclaimer = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[contains(@class, "PdpComponent_disclaimer")]//p')if x.xpath('normalize-space(.)').get()) or None
        product_overdose = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-overdose"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_missed_dose = ' '.join(x.xpath('normalize-space(.)').get() for x in response.xpath('//div[@data-slot="section-missed-dose"]//div[@data-slot="section-content"]//*[self::p or self::li]')if x.xpath('normalize-space(.)').get()) or None
        product_reference_url = response.xpath('//div[@data-slot="section-references"]//a/@href').getall() or None
        product_fact = {x.xpath('normalize-space(./p[1])').get(): x.xpath('normalize-space(./p[2])').get()for x in response.xpath('//div[@data-testid="pdp-fact-box"]''//div[starts-with(@data-testid, "pdp-fact-box-row-")]')} or None

        item = PlatinumrxPDP()
        item["product_name"] = product_name
        item["product_sku"] = prodcut_SKU
        item["product_url"] = product_url
        item["product_img_url"] = product_img_url
        item["product_category"] = product_category
        item["product_salt_composition"] = product_salt_composition
        item["product_manufacturer"] = product_menufacturer
        item["product_manufacturer_address"] = product_manufacturer_address
        item["product_pack_size"] = product_pack_size
        item["product_description"] = prodcut_description
        item["product_summary"] = product_summary
        item["product_mrp"] = product_price
        item["product_price_per_unit"] = product_price_per_unit
        item["product_availability"] = product_availabilty
        item["product_at_pincode"] = product_at_pincode
        item["product_certified"] = product_certified
        item["product_expiry"] = product_expiry
        item["product_return"] = product_return
        item["product_benefits"] = product_benefits
        item["product_uses"] = product_uses
        item["product_direction_of_use"] = product_direction_of_use
        item["product_how_it_works"] = product_how_it_works
        item["product_daily_dose"] = product_daily_dose
        item["product_side_effects"] = product_side_effects
        item["product_safety"] = product_safety
        item["product_quick_tips"] = product_quick_tips
        item["product_storage_advice"] = product_storage_advice
        item["product_overdose"] = product_overdose
        item["product_missed_dose"] = product_missed_dose
        item["product_drug_food_interaction"] = product_drug_food_interaction
        item["product_drug_interaction"] = product_drug_interaction
        item["product_drug_disease_interaction"] = product_drug_disease_interaction
        item["product_fact"] = product_fact
        item["product_disclaimer"] = product_disclaimer
        item["product_reference_url"] = product_reference_url
        item["compared_products"] = compared_products


        cursor,conn=create_table()    
        cursor.execute("UPDATE platinumrx_products_url SET status = 1 WHERE id = %s",(ids,))
        conn.commit()
        cursor.close()
        conn.close()
        yield item
