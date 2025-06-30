import frappe

def calculate_avg_movie_rating(movie_id: str) -> dict:
    """
    Tính điểm đánh giá trung bình và số lượt đánh giá cho một bộ phim.

    Args:
        movie_id (str): Tên (name) của Movie.

    Returns:
        dict: {
            "average": float | None,
            "total_ratings": int
        }
    """
    ratings = frappe.get_all(
        "Movie Rating",
        filters={"movie": movie_id},
        fields=["rating"]
    )

    total_ratings = len(ratings)

    if total_ratings == 0:
        return {
            "average": None,
            "total_ratings": 0
        }

    total_score = sum(r["rating"] * 5 for r in ratings)  # giả sử scale là 0.0 -> 1.0
    average = round(total_score / total_ratings, 1)

    return {
        "average": average,
        "total_ratings": total_ratings
    }
