# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import json

# all country info
import os

import frappe
from frappe.utils.momentjs import get_all_timezones


def get_country_info(country=None):
	data = get_all()
	data = frappe._dict(data.get(country, {}))
	if "date_format" not in data:
		data.date_format = "dd-mm-yyyy"
	if "time_format" not in data:
		data.time_format = "HH:mm:ss"

	return data


def get_all():
	with open(os.path.join(os.path.dirname(__file__), "country_info.json")) as local_info:
		all_data = json.loads(local_info.read())
	return all_data


@frappe.whitelist()
def get_country_timezone_info():
	return {"country_info": get_all(), "all_timezones": get_all_timezones()}


def get_translated_dict():
	from babel.dates import Locale, get_timezone, get_timezone_name

	translated_dict = {}
	locale = Locale.parse(frappe.local.lang, sep="-")

	# timezones
	for tz in get_all_timezones():
		timezone_name = get_timezone_name(get_timezone(tz), locale=locale, width="short")
		if timezone_name:
			translated_dict[tz] = timezone_name + " - " + tz

	# country names && currencies
	for country, info in get_all().items():
		country_name = locale.territories.get((info.get("code") or "").upper())
		if country_name:
			translated_dict[country] = country_name

		currency = info.get("currency")
		currency_name = locale.currencies.get(currency)
		if currency_name:
			translated_dict[currency] = currency_name

	return translated_dict


def update():
	with open(os.path.join(os.path.dirname(__file__), "currency_info.json")) as nformats:
		nformats = json.loads(nformats.read())

	all_data = get_all()

	for country in all_data:
		data = all_data[country]
		data["number_format"] = nformats.get(data.get("currency", "default"), nformats.get("default"))[
			"display"
		]

	with open(os.path.join(os.path.dirname(__file__), "country_info.json"), "w") as local_info:
		local_info.write(json.dumps(all_data, indent=1))
