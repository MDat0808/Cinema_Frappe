import frappe
from .response import res_error, res_success


@frappe.whitelist(allow_guest=True)
def get_all_production():
    try:
        production = frappe.get_all(
                    "Production Company",
                    fields=["name", "production_name", "logo", "nationality", "founded_date"],
                )
        res_success("Get all production company successfully", production)
    except Exception as e:
        return res_error(f"Error getting production company: {str(e)}")

@frappe.whitelist(allow_guest=True)
def get_movies_by_production(production_id: str ):
    try:
        movies = frappe.get_all(
            "Movie",
            filters={
                "production_company": production_id,
            },
            fields=["name", "title", "image_vertical", "image_horizontal","production_company", "release_date", "trailer", "overview","is_premium"]
        )

        production_name = frappe.get_all(
            "Production Company",
            filters={
                "name": production_id,
            },
            fields=["production_name"]
        )[0]

        data = {
            "production" : production_name,
            "movies": movies,
            "total_movies": len(movies)
        }

        return res_success(f"Get movies by production company successfully", data)

    except Exception as e:
        return res_error(f"Error fetching movies: {str(e)}")

