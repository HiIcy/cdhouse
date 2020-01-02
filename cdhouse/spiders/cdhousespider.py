# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request, Selector
from scrapy.http import Response
from urllib.parse import urljoin
from ..items import *
from scrapy_redis.spiders import RedisSpider
# http://www.waitingfy.com/archives/2027
from scrapy import Spider


# TODO:分布式，部署
class CdhomeSpider(Spider):
    name = 'cdhome'
    # redis_key = "cdhome:start_urls"
    start_urls = [
        'https://cd.newhouse.fang.com/house/s/',
        'https://cd.esf.fang.com/',
        'https://cd.zu.fang.com/'
    ]

    def start_requests(self):
        for i, url in enumerate(self.start_urls,0):
            if i == 0:
                yield Request(url, callback=self.visit_nh)
            elif i == 1:
                yield Request(url, callback=self.visit_esf)
            elif i == 2:
                yield Request(url, callback=self.visit_zu)

    def visit_nh(self, response: Response):
        self.logger.info(f"crawler newhouse: {response.url}")
        houses = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li')
        for house in houses:
            nlc_href: str = house.xpath('.//div[@class="nlc_details"]/div[1]/div[1]/a/@href').extract_first("")
            url = ""
            if nlc_href and nlc_href.startswith("https"):
                url = nlc_href
            elif nlc_href:
                url = urljoin("https:", nlc_href)
            else:
                pass
            if url:
                yield Request(url, callback=self.parse_nh)
        if not response.meta.get("page", 1) > 1:
            pages = response.xpath('//div[@class="page"]/ul/li[2]')
            last = pages.xpath('a[@class="last"]/@href').extract_first(1)
            if type(last) != int:
                last = last.rsplit("/", maxsplit=2)[-2][-2:]
                try:
                    last = int(last)
                except:
                    last = 1
            for i in range(2, last + 1):
                base_url = r"https://cd.newhouse.fang.com/house/s/b9"
                aim_url = base_url + str(i) + "/"
                self.logger.info(f"crawler newhouse aim_url  {aim_url}")
                yield response.follow(aim_url, callback=self.visit_nh, meta={"page": i})  # meta 浅拷贝

    def visit_esf(self, response: Response):
        self.logger.info(f"crawler ershouhouse: {response.url}")
        shops = response.xpath('//div[contains(@class,"shop_list")]/dl')
        for shop in shops:
            shop_href = shop.xpath('dd//a/@href').get("")
            url = ""
            if shop_href and shop_href.startswith("https"):
                url = shop_href
            elif shop_href:
                url = urljoin("https://cd.esf.fang.com/", shop_href)
            else:
                pass
            if url:
                yield Request(url, callback=self.parse_esf)
        pages = response.css("#list_D10_15 > p:last-child::text").re_first(".*?(\d+).*?", default=1)
        pages = int(pages)
        if not response.meta.get("page", 1) > 1:
            for i in range(2, pages + 1):
                base_url = "https://cd.esf.fang.com/house/i3"
                aim_url = base_url + str(i) + "/"
                self.logger.info(f"crawler ershouhouse aim_url: {aim_url}")
                yield response.follow(aim_url, callback=self.visit_esf, meta={"page": i})

    def visit_zu(self, response: Response):
        self.logger.info(f"crawler zuhouse: {response.url}")
        shops = response.css('#listBox > div.houseList > dl')
        for shop in shops:
            shop_href = shop.css('dd a::attr(href)').get("")
            url = ""
            if shop_href and shop_href.startswith("https"):
                url = shop_href
            elif shop_href:
                url = urljoin("https://cd.zu.fang.com/", shop_href)
            else:
                pass
            if url:
                yield Request(url, callback=self.parse_zu)
        pages = response.css("#rentid_D10_01 > span::text").re_first(".*?(\d+).*?", default=1)
        pages = int(pages)
        if not response.meta.get("page", 1) > 1:
            for i in range(2, pages + 1):
                base_url = "https://cd.zu.fang.com/house/i3"
                aim_url = base_url + str(i) + "/"
                self.logger.info(f"crawler zuhouse aim_url: {aim_url}")
                yield response.follow(aim_url, callback=self.visit_zu, meta={"page": i})

    def parse_nh(self, response: Response):
        more_info = response.xpath('//*[@id="xfptxq_B04_14"]/p/a/@href').get("")
        if more_info:
            more_info = urljoin("https:", more_info)
            yield Request(more_info, callback=self.parse_nh_info,
                          cb_kwargs={"url": response.url})

    def parse_nh_info(self, response: Response, url):
        nh_item = NewHouseItem()
        nh_item["url"] = url
        info_div = response.xpath("/html/body/div[5]/div/div[1]/div[1]")
        nh_item['name'] = response.xpath('/html/body/div[3]/div[2]/dl/dd/div[1]/h1/a/text()').get("").strip()
        nh_item['sale_type'] = "newhouse"
        nh_item["price"] = info_div.xpath("div[1]/div[1]/em/text()").re_first(".*?(\d+).*?", "-")
        nh_item["rate"] = info_div.xpath("div[1]/div[2]/a/span[2]/text()").get("0")
        nh_item["tenement"] = info_div.xpath("ul/li[1]/div[2]/text()").get("").strip("\t\n ")
        building_category = response.xpath("//span[@class='bulid-type']/text()").get("")
        if building_category:
            j = re.search(".*?(\w+).*\s*.*?(\w*)", building_category)
            building_category = j.group(1) + j.group(2)
        nh_item["building_category"] = building_category

        nh_item["decoration"] = info_div.xpath("ul/li[2]/div[2]/li[2]/div[2]/text()").get("").strip("\t\n ")
        # 环线位置
        nh_item["ring"] = info_div.xpath("ul/li[2]/div[2]/li[4]/div[2]/text()").get("").strip("\t\n ")
        nh_item["developer"] = info_div.xpath("ul/li[2]/div[2]/li[5]/div[2]/a/text()").get("").strip(" ")

        sale_div = response.xpath("/html/body/div[5]/div/div[1]/div[1]/ul/li[2]/div[3]")
        nh_item['status'] = sale_div.xpath("ul/li[1]/div[2]/text()").get("-").strip("\t\n ")
        # TODO: 开盘时间还有附属详情
        nh_item['opening'] = sale_div.xpath("ul/li[3]/div[2]/text()").get("-")
        nh_item['handing'] = sale_div.xpath("ul/li[4]/div[2]/text()").get("-")
        nh_item['address'] = sale_div.xpath("ul/li[5]/div[2]/text()").get("")
        nh_item['telephone'] = sale_div.xpath("ul/li[6]/div[2]/text()").get("-")
        house_types = sale_div.xpath("ul/li[7]/div[2]/a/text()").getall()
        nh_item['house_type'] = ",".join(house_types) if house_types else ""

        main_table = sale_div.xpath("div/div[contains(@class,table-part)]/table")
        pre_sale_permits = ""
        if len(main_table) > 0:
            trs = main_table.xpath("tr[position()>1]")
            for tr in trs:
                liecense = tr.xpath("td[1]/text()").get("")
                time = tr.xpath("td[2]/text()").get("")
                bind_build = tr.xpath("td[last()]/text()").get("").strip()
                cur_liecense = ""
                if liecense and time:
                    cur_liecense += f"{liecense}={time}"
                if cur_liecense and bind_build:
                    cur_liecense += f"~{bind_build}"
                if cur_liecense:
                    pre_sale_permits += f"{cur_liecense}|"
            pre_sale_permits = pre_sale_permits[:-1]  # 取消最后一个|
        nh_item['permits'] = pre_sale_permits

        facilities = response.xpath('//*[@id="Configuration"]')
        surrounding_facilities = ""
        for surround in facilities.xpath("ul/li"):
            title = surround.xpath("span/text()").get("")
            if title:
                surrounding_facilities += f"{title},"
        surrounding_facilities = surrounding_facilities[:-1]
        nh_item["surrounding_facilities"] = surrounding_facilities

        # FIXME: 修复这个
        plot_div = response.xpath("/html/body/div[5]/div/div[1]/div[1]/ul/li[2]/div[5]")
        nh_item['place_area'] = plot_div.xpath("ul/li[1]/div[2]/text()").get("-")
        nh_item['building_area'] = plot_div.xpath("ul/li[2]/div[2]/text()").get("-")
        nh_item['plot_ratio'] = plot_div.xpath("ul/li[3]/div[2]/text()").get("-").split("&")[0]
        nh_item['green_ratio'] = plot_div.xpath("ul/li[4]/div[2]/text()").get("-")
        nh_item['carport'] = plot_div.xpath("ul/li[5]/div[2]/text()").get("")
        nh_item['buildings'] = plot_div.xpath("ul/li[6]/div[2]/text()").re_first("(\d+).*?", "-")
        nh_item['households'] = plot_div.xpath("ul/li[7]/div[2]/text()").re_first("(\d+).*?", "-")
        nh_item['property_costs'] = plot_div.xpath("ul/li[9]/div[2]/text()").get("").split("&")[0]

        yield nh_item

    def parse_esf(self, response: Response):
        esh_item = EShouseItem()
        esh_item['url'] = response.url
        cont_div = response.xpath("/html/body/div[4]/div[1]/div[4]")
        esh_item['sale_type'] = 'ershouhouse'
        esh_item['cost'] = cont_div.css("div[1]/div[1]/div[1]/i/text()").get("")
        esh_item['house_type'] = cont_div.xpath("div[2]/div[1]/div[1]/text()").get("").strip("\t\n ")
        esh_item['area'] = cont_div.xpath("div[2]/div[2]/div[1]/text()").get("").strip(" ")
        esh_item['price'] = cont_div.xpath("div[2]/div[3]/div[1]/text()").get("").strip(" ")
        esh_item['orientation'] = cont_div.xpath("div[3]/div[1]/div[1]/text()").get("").strip(" ")
        esh_item['storey'] = cont_div.xpath("div[3]/div[2]/div[1]/text()").get("").strip(" ")
        esh_item['decoration'] = cont_div.xpath("div[3]/div[3]/div[1]/text()").get("").strip(" ")
        esh_item['estate_name'] = cont_div.xpath("div[4]/div[1]/div[2]//text()").get()
        regions = cont_div.xpath("div[4]/div[2]/div[2]/a/text()").getall()
        if regions:
            regions = [reg.strip("\t\n ") for reg in regions]
            regions = " > ".join(regions)
        esh_item['region'] = regions if regions else ""
        # TODO:FIXME : 顺序不一的问题(用字典映射)
        """
        resource_info = response.css("body > div.wid1200.clearfix > div.w1200.clearfix > "
                                     "div.zf_new_left.floatl > div.content-item.fydes-item > div.cont.clearfix")
        esh_item['build_year'] = resource_info.xpath("div[1]/span/text()").get()
        esh_item['elevator'] = resource_info.xpath("div[2]/span/text()").get()
        esh_item['property_right'] = resource_info.xpath("div[3]/span/text()").get()
        esh_item['structure'] = resource_info.xpath("div[4]/span/text()").get()
        esh_item['category'] = resource_info.xpath("div[5]/span/text()").get()

        estate_info = response.css("body > div.wid1200.clearfix > div.w1200.clearfix > "
                                   "div.zf_new_left.floatl > div:nth-child(3) > div.cont.pt30")

        esh_item['average_price'] = estate_info.xpath("div[1]/div[1]/span[2]/i/text()").get()
        esh_item['tenement_type'] = estate_info.xpath("div[2]/div[1]/span[2]/text()").re(".*(\w+).*")
        esh_item['tenement_price'] = estate_info.xpath("div[2]/div[2]/span[2]/text()").get()
        esh_item['building_type'] = estate_info.xpath("div[2]/div[3]/span[2]/text()").get()
        esh_item['green_rate'] = estate_info.xpath("div[2]/div[6]/span[2]/text()").get()
        esh_item['plot_rate'] = estate_info.xpath("div[2]/div[7]/span[2]/text()").get()
        esh_item['buildings'] = estate_info.xpath("div[2]/div[9]/span[2]/text()").get()
        esh_item['households'] = estate_info.xpath("div[2]/div[10]/span[2]/text()").get()
        """
        yield esh_item

    def parse_zu(self, response: Response):
        zu_item = ZUhouseItem()
        zu_item['url'] = response.url
        cont_div = response.css("body > div:nth-child(40) > div.tab-cont.clearfix > div.tab-cont-right")
        zu_item['sale_type'] = "zuhouse"
        zu_item['price'] = cont_div.css("div.tr-line.clearfix.zf_new_title > div:nth-child(1) > i::text").get()
        zu_item['lease_type'] = cont_div.xpath("div[3]/div[1]/div[1]/text()").get()
        zu_item['house_type'] = cont_div.xpath("div[3]/div[2]/div[1]/text()").get()
        zu_item['area'] = cont_div.xpath("div[3]/div[3]/div[1]/text()").get()
        zu_item['orientation'] = cont_div.xpath("div[4]/div[1]/div[1]/text()").get()
        storey = cont_div.xpath("div[4]/div[2]/div/text()").getall()
        if storey:
            storey = [sto.strip("\t\n ") for sto in storey]
            storey = "/".join(storey)
        zu_item['storey'] = storey if storey else ""
        zu_item['decoration'] = cont_div.xpath("div[4]/div[3]/div[1]/text()").get()

        estate_name = cont_div.xpath("div[5]/div[1]/div[2]/a/text()").getall()
        if estate_name:
            estate_name = " ".join(estate_name)
        zu_item['estate_name'] = estate_name if estate_name else ""
        zu_item['region'] = cont_div.xpath("div[5]/div[2]/div[2]/a/text()").get()

        yield zu_item
