# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class NewHouseItem(scrapy.Item):
	url = scrapy.Field()
	name = Field()
	sale_type=Field()
	price = Field()
	rate = Field()
	tenement = Field()
	building_category = Field()
	decoration = Field()
	ring = Field()
	developer = Field()
	status = Field()
	address = Field()
	telephone = Field()
	opening = Field()
	handing = Field()
	permits = Field()
	house_type = Field()
	surrounding_facilities = Field()
	place_area = Field()
	building_area = Field()
	plot_ratio = Field()
	green_ratio = Field()
	carport = Field()
	buildings = Field()
	households = Field()
	property_costs = Field()


class EShouseItem(scrapy.Item):
	url = Field()
	sale_type=Field()
	cost = Field()
	house_type = Field()
	area = Field()
	price = Field()
	orientation = Field()
	storey = Field()
	decoration = Field()
	estate_name = Field()
	region = Field()

	# build_year = Field()
	# elevator = Field()
	# property_right = Field()
	# structure = Field()
	# category = Field()
	#
	# average_price = Field()
	# tenement_type = Field()
	# tenement_price = Field()
	# building_type = Field()
	# green_rate = Field()
	# plot_rate = Field()
	# buildings = Field()
	# households = Field()


class ZUhouseItem(scrapy.Item):
	url = Field()
	sale_type=Field()
	price = Field()
	lease_type = Field()
	house_type = Field()
	area = Field()
	orientation = Field()
	storey = Field()
	decoration = Field()
	estate_name = Field()
	region = Field()