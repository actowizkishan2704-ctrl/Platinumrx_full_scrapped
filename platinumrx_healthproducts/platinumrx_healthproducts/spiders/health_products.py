import scrapy
from rich import print
import json
import jmespath
from platinumrx_healthproducts.items import PlatinumrxHealthproductsItem


class PlatinumrxProductSpider(scrapy.Spider):
    name = "health_products"
    allowed_domains = ["www.platinumrx.in"]

    def start_requests(self):
        cookies = {
            'platinumrx-device-id': 'c4f4d87f-86e8-4a88-87b4-e7a45cecb06c',
            'platinumrx-session-id': '03847e4a-2084-4150-87c8-025d9b71066a',
            '_gcl_au': '1.1.1386912106.1789029224',
            '_ga': 'GA1.1.1020510031.1789029225',
            '_ga_BHBBVCGVE0': 'GS2.1.s1789029225$o1$g1$t1789035467$j44$l0$h549390466$da4THJHUtYw8-09PKcD8CrqgcohCDFd1nIw',
            '_dd_s_v2': 'aid=47a24d2b-491d-423a-9130-315a19c20816&id=6a14d788-a1d4-4ecb-a7da-dd2c69eda145&created=1789033148145&expire=1789036371238&c=0',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,gu;q=0.8,bho;q=0.7,so;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.platinumrx.in/medicines',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
            # 'cookie': 'platinumrx-device-id=c4f4d87f-86e8-4a88-87b4-e7a45cecb06c; platinumrx-session-id=03847e4a-2084-4150-87c8-025d9b71066a; _gcl_au=1.1.1386912106.1789029224; _ga=GA1.1.1020510031.1789029225; _ga_BHBBVCGVE0=GS2.1.s1789029225$o1$g1$t1789035467$j44$l0$h549390466$da4THJHUtYw8-09PKcD8CrqgcohCDFd1nIw; _dd_s_v2=aid=47a24d2b-491d-423a-9130-315a19c20816&id=6a14d788-a1d4-4ecb-a7da-dd2c69eda145&created=1789033148145&expire=1789036371238&c=0',
        }
        labels = ["0-9"]
        labels.extend(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        for label in labels:
            url=f'https://www.platinumrx.in/otc?label={label}'
            yield scrapy.Request(url=url,headers=headers,cookies=cookies,meta={"label":label})        
            # break
    def parse(self, response):
        print(response.url)
        file_name=response.meta["label"]
        with open(f"all_medicine_pages/label_{file_name}.html",'w',encoding='utf-8')as f:
            f.write(response.text)
        scripts=response.xpath("//script[contains(text(),'ItemList')]/text()").get()
        data=json.loads(scripts)
        with open(f"product_list_json_pages/label_{file_name}.json",'w',encoding='utf-8')as f:
            json.dump(data,f,indent=4)
        products=jmespath.search("mainEntity.itemListElement[*].url",data)
        for product_url in products:
            products_urls = response.urljoin(product_url)
            item = PlatinumrxHealthproductsItem()
            item["product_url"] = products_urls
            yield item
        next_page = response.xpath("(//li//a[@aria-label='Go to next page']/@href)[2]").get()
        cookies = {
            'platinumrx-device-id': 'c4f4d87f-86e8-4a88-87b4-e7a45cecb06c',
            'platinumrx-session-id': '03847e4a-2084-4150-87c8-025d9b71066a',
            '_gcl_au': '1.1.1386912106.1789029224',
            '_ga': 'GA1.1.1020510031.1789029225',
            '_ga_BHBBVCGVE0': 'GS2.1.s1789029225$o1$g1$t1789037980$j60$l0$h549390466$da4THJHUtYw8-09PKcD8CrqgcohCDFd1nIw',
            '_dd_s_v2': 'aid=47a24d2b-491d-423a-9130-315a19c20816&id=6a14d788-a1d4-4ecb-a7da-dd2c69eda145&created=1789033148145&expire=1789038885018&c=0',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,gu;q=0.8,bho;q=0.7,so;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.platinumrx.in/medicines?label=0-9&page=1',
            'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
            # 'cookie': 'platinumrx-device-id=c4f4d87f-86e8-4a88-87b4-e7a45cecb06c; platinumrx-session-id=03847e4a-2084-4150-87c8-025d9b71066a; _gcl_au=1.1.1386912106.1789029224; _ga=GA1.1.1020510031.1789029225; _ga_BHBBVCGVE0=GS2.1.s1789029225$o1$g1$t1789037980$j60$l0$h549390466$da4THJHUtYw8-09PKcD8CrqgcohCDFd1nIw; _dd_s_v2=aid=47a24d2b-491d-423a-9130-315a19c20816&id=6a14d788-a1d4-4ecb-a7da-dd2c69eda145&created=1789033148145&expire=1789038885018&c=0',
        }
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,headers=headers,cookies=cookies,callback=self.parse,meta={"label": file_name})