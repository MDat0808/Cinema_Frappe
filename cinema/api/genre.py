import frappe
from .response import res_error, res_success

@frappe.whitelist(allow_guest=True)
def get_all_genres():
    try:
        genres = frappe.get_all("Genre", fields=["name", "genre_name", "genre_code","description"])
        
        return res_success("Get all genres successfully", genres)
    except Exception as e:
        return res_error(f"Error fetching genres: {str(e)}")


@frappe.whitelist(allow_guest=True)
def search_genre(keyword: str = "", limit: int = 10, offset: int = 0):
    try:
        if not keyword:
            return res_error("Keyword is required", "keyword")

        genres = frappe.get_all(
            "Genre",
            filters={
                "genre_name": ["like", f"%{keyword}%"]
            },
            fields=["name", "genre_name", "genre_code","description"],
            order_by="genre_name asc",
            limit_start=offset,
            limit_page_length=limit
        )

        return res_success("Search results", {
            "keyword": keyword,
            "count": len(genres),
            "results": genres
        })

    except Exception as e:
        return res_error(f"Error searching genres: {str(e)}", "server_error", code= 500)
