import frappe
from .response import res_error, res_success

@frappe.whitelist(allow_guest=False)  
def get_episode_detail(episode_id):
    try:
        episode = frappe.get_all(
            "Episode",
            filters={"name": episode_id},
            fields=["name", "episode_name", "episode_number", "duration", "release_date", "video_url", "is_premium"]
        )[0]
        if not episode:
            return res_error("Episode not found")
      

        if episode.get("is_premium"):
            user = frappe.session.user
            if not user_has_access(user, episode):
                return res_error("You do not have permission to access this premium episode")

        return res_success("Get episode detail successfully", episode)
    except Exception as e:
        return res_error(f"Error fetching episode detail: {str(e)}")



@frappe.whitelist(allow_guest=True)
def get_episodes_by_movie(movie_id):
    try:
        episodes = frappe.get_all(
            "Episode",
            filters={"movie": movie_id},
            fields=["name", "episode_name", "episode_number", "duration", "release_date", "is_premium"]
        )
        return res_success("Get episodes successfully", episodes)
    except Exception as e:
        return res_error(f"Error fetching episodes: {str(e)}")



def user_has_access(user: str, episode: str) -> bool:
    try:
        if not episode.is_premium:
            return True
        
        membership = frappe.get_all(
            "Membership",
            filters={
                "user": user,
                "is_active": 1,  
                "start_date": ["<=", frappe.utils.nowdate()],
                "end_date": [">=", frappe.utils.nowdate()]
            },
            limit_page_length=1
        )

        return bool(membership)

    except Exception as e:
        frappe.log_error(str(e), "Error in user_has_access")
        return False