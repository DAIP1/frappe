import frappe


def execute():
	days = frappe.db.get_single_value("Website Settings", "auto_account_deletion")
	frappe.db.set_value("Website Settings", None, "auto_account_deletion", days * 24)
