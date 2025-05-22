# Copyright (c) 2025, Khai, Dat and contributors
# For license information, please see license.txt

# import frappe
import json
from frappe.model.document import Document
import frappe

class Room(Document):

	def after_insert(self):
			if not self.seat_map_template:
				return

			# Lấy template layout
			template = frappe.get_doc("Seat Map Template", self.seat_map_template)

			try:
				layout = json.loads(template.layout)  # layout là chuỗi JSON
			except Exception as e:
				frappe.throw(f"Lỗi khi đọc layout trong SeatMapTemplate: {e}")

			for seat in layout.get("seats", []):
				

				frappe.get_doc({
					"doctype": "Seat",
					"seat_number": seat["seat_number"],
					"seat_type": seat.get("seat_type", "Standard"),
					"room": self.name
				}).insert()
	
	def before_delete(self):
		seats = frappe.get_all("Seat", filters={"room": self.name}, fields=["name"])
		for seat in seats:
			frappe.delete_doc("Seat", seat.name, force=True)


