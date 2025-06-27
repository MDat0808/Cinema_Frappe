import frappe
from .response import res_success, res_error



@frappe.whitelist(allow_guest=False)
def create_user_membership():
    if frappe.request.method != "POST":
        return res_error(f"Error not found", "api_error",404)

    try:
        data = frappe.request.get_json()
        user = frappe.session.user
        membership_plan = data.get("membership_plan")
        if not user or not membership_plan:
            return res_error("User and membership plan is required","user, membership_plan", 400)

        plan_doc = frappe.get_doc("Membership Plan", membership_plan)
        duration = plan_doc.duration_days or 30
        amount_usd = plan_doc.price
        start_date = frappe.utils.nowdate()
        end_date = frappe.utils.add_days(start_date, duration)
        is_active = 1 if amount_usd == 0 else 0
        user_membership = frappe.get_doc({
            "doctype": "User Membership",
            "user": user,
            "membership_plan": membership_plan,
            "start_date": start_date,
            "end_date": end_date,
            "is_active": is_active
        })
        user_membership.insert(ignore_permissions=True)

        if amount_usd != 0:
          membership_payment = frappe.get_doc({
              "doctype": "Membership Payment",
              "user": user,
              "membership_subscription": user_membership.name,
              "amount": amount_usd,
              "payment_status": "Draft"
          })
          membership_payment.insert(ignore_permissions=True)
        return res_success( "Create membership successfully", user_membership.name)

    except Exception as e:
        return res_error(f"Error create membership: {str(e)}", "server_error")


@frappe.whitelist()
def check_free_plan_eligibility():
    try:
        user = frappe.session.user

        free_plans = frappe.get_all("Membership Plan", filters={"price": 0}, pluck="name")

        used = frappe.get_all("User Membership", filters={
            "user": user,
            "membership_plan": ["in", free_plans]
        }, limit=1)

        eligible = True
        message = "You are eligible for a free membership."
        if used:
            eligible = False
            message = "You have already used a free membership plan."

        return res_success(message, {"eligible":eligible})

    except Exception as e:
        return res_error(f"Error create membership: {str(e)}", "server_error", 500)

