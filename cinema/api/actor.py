import frappe
from .response import res_error, res_success

@frappe.whitelist(allow_guest=True)
def get_actor_detail(actor_id):
    try:
        if not actor_id:
            res_error(f"Actor ID required","actor_id")
        actor = frappe.get_all(
                    "Person",
                    filters={"person_type": "Actor", "name" : actor_id},  
                    fields=["name", "full_name", "image", "nationality", "bio", "dob", "gender", "active_date", "person_type"],
                )[0]
        res_success("Get actor detail successfully", actor)
    except Exception as e:
        return res_error(f"Error getting actor: {str(e)}")

@frappe.whitelist(allow_guest=True)
def search_actor(keyword: str = "", limit: int = 10, offset: int = 0):
    try:
        if not keyword:
            return res_error("Keyword is required", "keyword")

        actors = frappe.get_all(
            "Person",
            filters={
                "person_type": "Actor",
                "full_name": ["like", f"%{keyword}%"]
            },
            fields=["name", "full_name", "image", "nationality", "bio", "dob", "gender", "active_date", ""],
            order_by="full_name asc",
            limit_start=offset,
            limit_page_length=limit
        )

        return res_success("Search results", {
            "keyword": keyword,
            "count": len(actors),
            "results": actors
        })

    except Exception as e:
        return res_error(f"Error searching actors: {str(e)}", "server_error", code= 500)
