import frappe
from frappe import _
from frappe.utils import cstr
from frappe.website.page_renderers.template_page import TemplatePage


class NotPermittedPage(TemplatePage):
	def __init__(self, path=None, http_status_code=None, exception=""):
		frappe.local.message = cstr(exception)
		super().__init__(path=path, http_status_code=http_status_code)
		self.http_status_code = 403

	def can_render(self):
		return True

	def render(self):
		frappe.local.message_title = _("Not Permitted")
		frappe.local.response["context"] = dict(
			indicator_color="red", primary_action="/login", primary_label=_("Login"), fullpage=True
		)
		self.set_standard_path("message")
		return super().render()
