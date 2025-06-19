import frappe
from .response import res_error, res_success
from collections import Counter

@frappe.whitelist(allow_guest=True)
def get_all_actors():
    try:
        actors = frappe.get_all(
                    "Person",
                    filters={"person_type": "Actor"},  
                    fields=["name", "full_name", "image", "nationality", "bio", "dob", "gender", "active_date", "person_type"],
                )
        res_success("Get all actors successfully", actors)
    except Exception as e:
        return res_error(f"Error getting actor: {str(e)}")


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

@frappe.whitelist(allow_guest=True)
def get_top_actors(limit=10):
    try:
        movie_cast = frappe.get_all(
            "Movie Person",
            filters={"person_role": "Actor"},
            fields=["person"]
        )

        if not movie_cast:
            return res_success("No actors found", [])

        actor_counts = Counter(record["person"] for record in movie_cast)
        top_actors = actor_counts.most_common(int(limit))

        actor_ids = [actor_id for actor_id, _ in top_actors]

        actor_infos = frappe.get_all(
            "Person",
            filters={"name": ["in", actor_ids]},
            fields=["name", "full_name", "image"]
        )
        actor_info_map = {actor["name"]: actor for actor in actor_infos}

        result = []
        for actor_id, movie_count in top_actors:
            info = actor_info_map.get(actor_id, {})
            result.append({
                "actor_id": actor_id,
                "full_name": info.get("full_name", actor_id),
                "image": info.get("image"),
                "movie_count": movie_count
            })

        return res_success("Top actors fetched successfully", result)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get_top_actors error")
        return res_error(f"Error getting top actors: {str(e)}", "server_error", code=500)