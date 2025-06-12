import frappe
from .response import res_success, res_error

@frappe.whitelist(allow_guest=True)
def get_reviews_by_movie(movie_id: str):
    try:
        if not movie_id:
            return res_error("Movie ID is required", "movie_id")

        ratings = frappe.get_all(
            "Movie Rating",
            filters={"movie": movie_id},
            fields=["name", "rating", "user", "comment", "creation", "parent_rating"],
            order_by="creation desc"
        )

        if not ratings:
            return res_success("Movie ratings fetched successfully", {
                "avg_rating": 0,
                "total_ratings": 0,
                "reviews": []
            })

        users = list({r["user"] for r in ratings})
        user_map = {
            u.name: u.full_name
            for u in frappe.get_all("User", filters={"name": ["in", users]}, fields=["name", "full_name"])
        }

        root_reviews = []
        replies_by_parent = {}
        all_ratings = []

        for r in ratings:
            r["rating"] = round(float(r["rating"]) * 5, 1) if r.get("rating") is not None else 0
            r["username"] = user_map.get(r["user"], r["user"])

            all_ratings.append(r["rating"])

            if r.get("parent_rating"):
                replies_by_parent.setdefault(r["parent_rating"], []).append(r)
            else:
                root_reviews.append(r)

        for r in root_reviews:
            r["replies"] = replies_by_parent.get(r["name"], [])

        total_ratings = len(all_ratings)
        avg_rating = round(sum(all_ratings) / total_ratings, 1) if total_ratings else 0

        return res_success("Movie ratings fetched successfully", {
            "avg_rating": avg_rating,
            "total_ratings": total_ratings,
            "reviews": root_reviews
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return res_error(f"Error fetching movie ratings: {str(e)}", "server_error")