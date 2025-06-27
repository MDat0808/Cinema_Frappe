import frappe
from frappe import _
from .response import res_error, res_success

@frappe.whitelist()
def get_logged_user_info_custom():
    try:
        user = frappe.session.user

        if user == "Guest":
            return res_error("Unauthorized","token",401)
        
        user_doc = frappe.get_doc("User", user)

        data = {
              "name": user_doc.name,
              "full_name": user_doc.full_name or "",
              "email": user_doc.email,
              "avatar": user_doc.user_image or "",
        }

        return res_success("Get profile user successfully", data)

    except Exception as e:
        return res_error("Get profile user error","server_error",500)
