import frappe
from .response import res_error, res_success
from ..utils.avg_rating import calculate_avg_movie_rating

@frappe.whitelist(allow_guest=True)
def get_all_movies():
    try:
        movies = frappe.get_all("Movie", fields=["age_limit","name","trailer", "title", "image_vertical","image_horizontal","production_company",  "nationality","release_date", "is_premium"])
        
        for movie in movies:
            genres = frappe.get_all(
                "Movie Genre",  
                filters={"parent": movie["name"]},
                fields=["genre"]  
            )
            movie["genres"] = [g["genre"] for g in genres]
            rating_info = calculate_avg_movie_rating(movie["name"])
            movie["avg_rating"] = rating_info["average"]
            movie["total_ratings"] = rating_info["total_ratings"]
        return res_success("Get all movies successfully", movies)
    except Exception as e:
        return res_error(f"Error fetching movies: {str(e)}")

@frappe.whitelist(allow_guest=True)
def get_movie_detail(title=None, name=None, movie=None):
    try:
        # Ưu tiên lấy id (name) nếu có
        movie_name = name or movie

        # Nếu chưa có id, thì tìm theo title
        if not movie_name and title:
            movie_name = frappe.get_value("Movie", {"title": title}, "name")

        if not movie_name:
            return res_error("Movie not found")

        # Basic movie info
        movie_data = frappe.get_all(
            "Movie",
            filters={"name": movie_name},
            fields=["age_limit","name", "title", "image_vertical", "image_horizontal",
                    "production_company", "release_date", "trailer", "overview", "is_premium","duration"]
        )
        if not movie_data:
            return res_error("Movie not found")
        movie_data = movie_data[0]

        # Genres
        genres = frappe.get_all(
            "Movie Genre",
            filters={"parent": movie_name},
            fields=["genre"]
        )
        movie_data["genres"] = [g["genre"] for g in genres]

        # People (cast & crew)
        people_links = frappe.get_all(
            "Movie Person",
            filters={"movie": movie_name},
            fields=["person", "role_name", "role_type", "person_role"]
        )

        actors, directors, producers = [], [], []

        for link in people_links:
            person = frappe.get_doc("Person", link["person"])
            person_info = {
                "id": person.name,
                "full_name": person.full_name,
                "image": person.image,
                "role_name": link["role_name"],
                "role_type": link["role_type"]
            }

            role = link["person_role"]
            if role == "Actor":
                actors.append(person_info)
            elif role == "Director":
                directors.append(person_info)
            elif role == "Producer":
                producers.append(person_info)

        movie_data["cast"] = actors
        movie_data["directors"] = directors
        movie_data["producers"] = producers
        rating_info = calculate_avg_movie_rating(movie_name)
        movie_data["avg_rating"] = rating_info["average"]
        movie_data["total_ratings"] = rating_info["total_ratings"]

        return res_success("Get movie detail successfully", movie_data)

    except Exception as e:
        return res_error(f"Error fetching movie detail: {str(e)}")

@frappe.whitelist(allow_guest=True)
def get_movie_episodes(movie_id):
    try:
        episodes = frappe.get_all(
            "Episode",
            filters={"movie": movie_id},
            fields=[
                "name",
                "episode_name",
                "episode_number",
                "duration",
                "release_date",
                "video_url",
                "is_premium",
                "image",
                "description"
            ]
        )
        return res_success("Get movie episodes successfully", episodes)
    except Exception as e:
        return res_error(f"Error fetching episodes: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_top_movies(limit = 5):
    try:
        limit = int(limit) if limit else 5
        movies = frappe.get_all("Movie", fields=["age_limit","name", "trailer","title", "image_vertical", "image_horizontal",  "production_company",  "release_date", "is_premium"])

        for movie in movies:
            genres = frappe.get_all(
                "Movie Genre",  
                filters={"parent": movie["name"]},
                fields=["genre"]  
            )
            movie["genres"] = [g["genre"] for g in genres]
            rating_info = calculate_avg_movie_rating(movie["name"])
            movie["avg_rating"] = rating_info["average"]
            movie["total_ratings"] = rating_info["total_ratings"]
        top_movies = sorted(
            movies,
            key=lambda m: (m.get("avg_rating") or 0, m.get("total_ratings") or 0),
            reverse=True
        )[:limit]
        return res_success("Get featured movies successfully", top_movies)

    except Exception as e:
        return res_error(f"Error fetching featured movies: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_top_movies_by_genre(genre_id, limit = 10):
    try:
        filtered_movie_genres = frappe.get_all(
            "Movie Genre",
            filters={"genre": genre_id},
            fields=["parent"]
        )

        movie_ids = list({entry["parent"] for entry in filtered_movie_genres})
        if not movie_ids:
            return res_success("No movies found for this genre", [])

        movies = frappe.get_all(
            "Movie",
            filters={"name": ["in", movie_ids]},
            fields=["name", "title", "image_vertical", "image_horizontal", "release_date"]
        )

        all_movie_genres = frappe.get_all(
            "Movie Genre",
            filters={"parent": ["in", movie_ids]},
            fields=["parent", "genre"]
        )

        genre_map = {}
        for entry in all_movie_genres:
            genre_map.setdefault(entry["parent"], []).append(entry["genre"])

        for movie in movies:
            movie["genres"] = genre_map.get(movie["name"], [])
            rating_info = calculate_avg_movie_rating(movie["name"])
            movie["avg_rating"] = rating_info["average"]
            movie["total_ratings"] = rating_info["total_ratings"]

        top_movies = sorted(
            movies,
            key=lambda m: (m.get("avg_rating") or 0, m.get("total_ratings") or 0),
            reverse=True
        )[:limit]

        return res_success("Get top rated movies by genre successfully", top_movies)

    except Exception as e:
        return res_error(f"Error fetching featured movies: {str(e)}")

@frappe.whitelist(allow_guest=True)
def get_featured_movies_by_nationality(nationality_id, limit = 10):
    try:
        movies = frappe.get_all(
            "Movie",
            filters={"nationality": nationality_id},
            fields=["name", "title", "image_vertical", "image_horizontal","release_date"]
        )

        for movie in movies:
            genres = frappe.get_all(
                "Movie Genre",  
                filters={"parent": movie["name"]},
                fields=["genre"]  
            )
            movie["genres"] = [g["genre"] for g in genres]
            rating_info = calculate_avg_movie_rating(movie["name"])
            movie["avg_rating"] = rating_info["average"]
            movie["total_ratings"] = rating_info["total_ratings"]

        top_movies = sorted(
            movies,
            key=lambda m: (m.get("avg_rating") or 0, m.get("total_ratings") or 0),
            reverse=True
        )[:limit]

        return res_success("Get top rated movies by genre successfully", top_movies)

    except Exception as e:
        return res_error(f"Error fetching featured movies: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_movies_by_genre(genre_id):
    try:
        movie_genre_records = frappe.get_all(
            "Movie Genre",
            filters={"genre": genre_id},
            fields=["parent"]  
        )
        movie_ids = [record["parent"] for record in movie_genre_records]

        if not movie_ids:
            return res_success("No movies found for this genre", [])
        
        movies = frappe.get_all(
            "Movie",
            filters={"name": ["in", movie_ids]},
            fields=["name", "title", "image_vertical", "image_horizontal","production_company", "release_date", "trailer", "is_premium"]
        )

        for movie in movies:
            genres = frappe.get_all(
                "Movie Genre",  
                filters={"parent": movie["name"]},
                fields=["genre"]  
            )
            movie["genres"] = [g["genre"] for g in genres]
            rating_info = calculate_avg_movie_rating(movie["name"])
            movie["avg_rating"] = rating_info["average"]
            movie["total_ratings"] = rating_info["total_ratings"]
        return res_success("Get movies by genre successfully", movies)
    except Exception as e:
        return res_error(f"Error fetching movies by genre: {str(e)}")


@frappe.whitelist(allow_guest=True)
def get_recommended_movies(current_movie_id, limit=5):
    try:
        genres = frappe.get_all(
            "Movie Genre",
            filters={"parent": current_movie_id},
            fields=["genre"]
        )
        genre_ids = [g["genre"] for g in genres]

        if not genre_ids:
            return res_success("No genre found for this movie", [])

        movie_genres = frappe.get_all(
            "Movie Genre",
            filters={"genre": ["in", genre_ids]},
            fields=["parent"]
        )
        movie_ids = list({m["parent"] for m in movie_genres if m["parent"] != current_movie_id})

        if not movie_ids:
            return res_success("No related movies found", [])

        movie_ratings = []
        for movie_id in movie_ids:
            rating = calculate_avg_movie_rating(movie_id)
            movie_ratings.append({"movie_id": movie_id, "avg_rating": rating})

        movie_ratings.sort(key=lambda x: x["avg_rating"], reverse=True)
        top_movie_ids = [r["movie_id"] for r in movie_ratings[:int(limit)]]

        movies = frappe.get_all(
            "Movie",
            filters={"name": ["in", top_movie_ids]},
            fields=["name", "title", "image_vertical", "image_horizontal","release_date", "is_premium"]
        )

        for movie in movies:
            rating = next((r for r in movie_ratings if r["movie_id"] == movie["name"]), {"average": None, "total_ratings": 0})
            movie["avg_rating"] = rating["average"]
            movie["total_ratings"] = rating["total_ratings"]


        return res_success("Recommended movies fetched successfully", movies)

    except Exception as e:
        return res_error(f"Error fetching recommended movies: {str(e)}")

@frappe.whitelist(allow_guest=True)
def get_movies_by_person_role(person_id: str, role: str = "Actor"):
    try:
        movie_links = frappe.get_all(
            "Movie Person",
            filters={
                "person": person_id,
                "person_role": role
            },
            fields=["movie"]
        )
        movie_ids = [m["movie"] for m in movie_links]

        if not movie_ids:
            return res_success(f"No movies found for this person with role {role}", [])

        movies = frappe.get_all(
            "Movie",
            filters={"name": ["in", movie_ids]},
            fields=["name", "title", "image_vertical", "image_horizontal","release_date"]
        )

        for movie in movies:
            genres = frappe.get_all(
                "Movie Genre",
                filters={"parent": movie["name"]},
                fields=["genre"]
            )
            movie["genres"] = [g["genre"] for g in genres]

        return res_success(f"Get movies by person with role {role} successfully", movies)

    except Exception as e:
        return res_error(f"Error fetching movies: {str(e)}")


@frappe.whitelist(allow_guest=True)
def search_movies(keyword: str):
    try:
        keyword = keyword.strip()

        if not keyword:
            return res_success("No search keyword provided", {"movies": [], "people": []})

        movies = frappe.get_all(
            "Movie",
            filters={"title": ["like", f"%{keyword}%"]},
            fields=["name", "title", "image_vertical", "image_horizontal","release_date", "is_premium"]
        )

        people_matches = frappe.get_all(
            "Person",
            filters={"full_name": ["like", f"%{keyword}%"]},
            fields=["name", "full_name", "image", "dob","gender", "nationality"]
        )

        person_ids = [p["name"] for p in people_matches]

        if person_ids:
            related_movies = frappe.get_all(
                "Movie Person",
                filters={"person": ["in", person_ids], "person_role": "Actor"},
                fields=["movie"]
            )
            movie_ids = list(set(m["movie"] for m in related_movies))

            additional_movies = frappe.get_all(
                "Movie",
                filters={"name": ["in", movie_ids]},
                fields=["name", "title", "image_vertical", "image_horizontal","release_date", "is_premium"]
            )

            movie_names = set(m["name"] for m in movies)
            for m in additional_movies:
                if m["name"] not in movie_names:
                    movies.append(m)

        return res_success("Search results", {
            "movies": movies,
            "people": people_matches
        })

    except Exception as e:
        return res_error(f"Error searching movies: {str(e)}")
