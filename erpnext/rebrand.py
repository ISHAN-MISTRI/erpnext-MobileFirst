# Copyright (c) 2026, HP and contributors
# For license information, please see license.txt

import frappe

def run():
	print("Starting database rebranding...")

	# 1. Update System Settings app name
	frappe.db.set_single_value("System Settings", "app_name", "MobileFirst")
	print("- System Settings 'app_name' set to 'MobileFirst'")

	# 2. Update Website Settings app name
	frappe.db.set_single_value("Website Settings", "app_name", "MobileFirst")
	print("- Website Settings 'app_name' set to 'MobileFirst'")

	# 3. Update Website Settings brand HTML
	brand_html = '<div style="font-weight:600;font-size:18px;">MobileFirst</div>'
	frappe.db.set_single_value("Website Settings", "brand_html", brand_html)
	print("- Website Settings 'brand_html' updated")

	# 4. Clear old translation records for 'en'
	frappe.db.delete("Translation", {"source_text": ["in", ["ERPNext", "Frappe Framework"]], "language": "en"})
	print("- Deleted old English translations for 'ERPNext' and 'Frappe Framework'")

	# 5. Insert new translations
	translations = [
		{"source_text": "ERPNext", "translated_text": "MobileFirst"},
		{"source_text": "Frappe Framework", "translated_text": "MobileFirst Framework"}
	]

	for trans in translations:
		doc = frappe.new_doc("Translation")
		doc.language = "en"
		doc.source_text = trans["source_text"]
		doc.translated_text = trans["translated_text"]
		doc.insert(ignore_permissions=True)
		print(f"- Added translation: '{trans['source_text']}' -> '{trans['translated_text']}'")

	# 6. Commit database changes
	frappe.db.commit()
	print("- Database changes committed successfully")

	# 7. Clear system and translation cache
	frappe.clear_cache()
	print("- Cache cleared")
	print("Database rebranding complete!")
