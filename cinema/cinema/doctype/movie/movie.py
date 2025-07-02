# Copyright (c) 2025, Khai, Dat and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe

class Movie(Document):
	def after_insert(self):
		self.set_age_limit_from_genres()

	def on_update(self):
		self.set_age_limit_from_genres()

	def set_age_limit_from_genres(self):
		genre_ids = [row.genre for row in self.movie_genre if row.priority == 1 and row.genre]
		
		genre_age_links = frappe.get_all("Genre", filters = {"name": ["in", genre_ids]}, fields=["age_limit"])

		age_limit_ids = [g.age_limit for g in genre_age_links if g.age_limit]

		age_values = frappe.get_all(
        "Age",
        filters={"name": ["in", age_limit_ids]},
        fields=["age_limit"]
    )

		min_age = min((a.age_limit for a in age_values if a.age_limit is not None), default=0)

		if min_age and self.age_limit != min_age:
			self.age_limit = min_age
			self.save(ignore_permissions=True)

