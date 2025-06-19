import frappe
from .response import res_error, res_success

@frappe.whitelist(allow_guest=True)
def get_all_nationalities():
    try:
        nationalities = frappe.get_all("Nationlity", fields=["name", "nationality_name", "nationality_code","image"])
        
        return res_success("Get all nationalities successfully", nationalities)
    except Exception as e:
        return res_error(f"Error fetching nationalities: {str(e)}")

