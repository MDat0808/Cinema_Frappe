import frappe
from frappe import _
from .response import res_error, res_success


@frappe.whitelist(allow_guest=True)
def get_provinces_by_region(region):
    """
    Trả về danh sách tỉnh/thành thuộc một miền.
    """
    if not region:
        res_error("Region is required", "region", "REQUIRED")

    provinces = frappe.get_all(
        "Province",
        filters={"region": region},
        fields=["province_name"],
        distinct=True
    )
    
    
    response = {"region": region,
    "provinces": provinces }

    res_success("Get list province by region success",response)