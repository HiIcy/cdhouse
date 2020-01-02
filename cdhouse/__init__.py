# from urllib.parse import urljoin
#
# import aiohttp
# import asyncio
# from bs4 import BeautifulSoup
# from aiohttp import TCPConnector
# from lxml import etree
#
#
# async def mian():
#     url = "https://xiangsonghu028.fang.com/house/3210602438/housedetail.htm"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as res:
#             f = open("./temSite.html", encoding='gb2312', mode='w')
#             text = await res.text(encoding='gb2312', errors='ignore')
#             f.write(text)
#             response: etree._ElementTree = etree.fromstring(text, etree.HTMLParser())
#             nh_item = response.xpath("/html/body/div[5]/div/div[1]/div[1]/ul/li[2]/div[2]/li[2]/div[2]/text()")
#             for ni in nh_item[:]:
#                 print(ni)
#             import re
#             print(len(nh_item))
#             exit(0)
#         # houses = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li')
#         # for house in houses:
#         # 	nlc_href: str = house.xpath('.//div[@class="nlc_details"]/div[1]/div[1]/a/@href')
#         # 	try:
#         # 		nlc_href = nlc_href[0]
#         # 	except:
#         # 		nlc_href = ""
#         # 	url = ""
#         # 	if nlc_href and nlc_href.startswith("https"):
#         # 		url = nlc_href
#         # 	elif nlc_href:
#         # 		url = urljoin("https:", nlc_href)
#         # 	else:
#         # 		pass
#         # 	if url:
#         # 		pass
#         # # print(url)
#         # pages = response.xpath('//div[@class="page"]/ul/li[2]')[0]
#         # last = pages.xpath('a[@class="last"]/@href')
#         # try:
#         # 	last = last[0]
#         # except:
#         # 	last = 1
#         # print(last)
#         # if type(last) != int:
#         # 	last = last.rsplit("/", maxsplit=2)[-2][-2:]
#         # 	try:
#         # 		last = int(last)
#         # 	except:
#         # 		last = 1
#         # print(last)
#         # for i in range(2, last + 1):
#         # 	base_url = r"https://cd.newhouse.fang.com/house/s/b9"
#         # 	aim_url = base_url + str(i) + "/"
#         # 	print(aim_url)
#
#
# async def mnai():
#     with open(r"./tempSite.html", "r", encoding='gb2312') as f:
#         content = f.read()
#         # response = etree.HTML(content, etree.HTMLParser())
#         response = etree.HTML(content)
#         cont_div = response.xpath("/html/body/div[4]/div[1]/div[4]")[0]
#         print(cont_div)
#         sale_type = 'ershouhouse'
#         cost = cont_div.xpath("div[1]/div[1]/div[1]/i/text()")[0]
#         print(cost)
#         house_type = cont_div.xpath("div[2]/div[1]/div[1]/text()")[0].strip("\t\n ")
#         print(house_type)
#         area = cont_div.xpath("div[2]/div[2]/div[1]/text()")[0].strip(" ")
#         print(area)
#         price = cont_div.xpath("div[2]/div[3]/div[1]/text()")[0].strip(" ")
#         print(price)
#         orientation = cont_div.xpath("div[3]/div[1]/div[1]/text()")[0].strip(" ")
#         print(orientation)
#         storey = cont_div.xpath("div[3]/div[2]/div[1]/text()")[0].strip(" ")
#         print(storey)
#         decoration = cont_div.xpath("div[3]/div[3]/div[1]/text()")[0].strip(" ")
#         print(decoration)
#         estate_name = cont_div.xpath("div[4]/div[1]/div[2]//text()")[0]
#         print(estate_name)
#         regions = cont_div.xpath("div[4]/div[2]/div[2]/a/text()")
#         if regions:
#             regions = [reg.strip("\t\n ") for reg in regions]
#             regions = " > ".join(regions)
#         region = regions if regions else ""
#         print(region)
#
#         # resource_dict = {"build_year":"修建年份",
#         #                  "elevator":'有无电梯',
#         #                  'property_right':''}
#         # # TODO:FIXME : 顺序不一的问题
#         # resource_infos = response.xpath("/html/body/div[4]/div[2]/div[1]/div[1]/div[2]/div")
#         # for resource_info in resource_infos:
#         #
#         # print(resource_info)
#         # build_year = resource_info.xpath("div[1]/span/text()")[0]
#         # print(build_year)
#         # elevator = resource_info.xpath("div[2]/span/text()")[0]
#         # print(elevator)
#         # property_right = resource_info.xpath("div[3]/span/text()")[0]
#         # print(property_right)
#         # structure = resource_info.xpath("div[4]/span/text()")[0]
#         # print(structure)
#         # category = resource_info.xpath("div[5]/span/text()")
#         # print(category)
#         #
#         #
#         # estate_info = response.xpath("/html/body/div[4]/div[2]/div[1]/div[2]/div[2]")[0]
#         # average_price = estate_info.xpath("div[1]/div[1]/span[2]/i/text()")[0]
#         # print(average_price)
#         #
#         # tenement_type = estate_info.xpath("div[2]/div[1]/span[2]/text()")[0]
#         # print(tenement_type)
#         # tenement_price = estate_info.xpath("div[2]/div[2]/span[2]/text()")[0]
#         # print(tenement_price)
#         # building_type = estate_info.xpath("div[2]/div[3]/span[2]/text()")[0]
#         # print(building_type)
#         # green_rate = estate_info.xpath("div[2]/div[6]/span[2]/text()")
#         # print(green_rate)
#         # plot_rate = estate_info.xpath("div[2]/div[7]/span[2]/text()")
#         # print(plot_rate)
#         # buildings = estate_info.xpath("div[2]/div[9]/span[2]/text()")
#         # print(buildings)
#         # households = estate_info.xpath("div[2]/div[10]/span[2]/text()")
#         # print(households)
#
# # status = sale_div.xpath("ul/li[1]/di
#
# lp = asyncio.get_event_loop()
# lp.run_until_complete(mnai())
