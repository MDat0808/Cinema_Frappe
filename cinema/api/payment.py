import frappe
from frappe import _
from .response import res_error, res_success

@frappe.whitelist()
def get_payment_history():
    try:
        user = frappe.session.user

        payments = frappe.get_all("Membership Payment",
            filters={"user": user},
            fields=["name", "payment_id", "amount", "status", "payment_at"],
            order_by="creation desc"
        )

        for payment in payments:
                membership_plan = frappe.db.get_all(
                    "User Membership",
                    filters={"user": user},
                    fields=["membership_plan"],
                    limit=1)[0]          
                if membership_plan:
                  plan_doc = frappe.get_doc("Membership Plan", membership_plan.get("membership_plan"))
                  payment["membership_plan"] = {
                        "name": plan_doc.name,
                        "title": plan_doc.title,
                        "duration_days": plan_doc.duration_days,
                  }

        return res_success("Get list history payment successfully", payments)

    except Exception as e:
        return res_error("Unable to fetch payment history.","server_error", 500)



@frappe.whitelist()
def get_payment_detail(payment_id):
    try:
        user = frappe.session.user


        payment = frappe.get_all("Membership Payment",
            filters={"user": user, "payment_id": payment_id},
            fields=["name", "payment_id", "amount", "status", "payment_at"],
            limit=1
        )[0]

        membership_plan = frappe.db.get_all(
                    "User Membership",
                    filters={"user": user},
                    fields=["membership_plan"],
                    limit=1)[0]
        plan_doc = frappe.get_doc("Membership Plan", membership_plan.get("membership_plan"))

        result = {
            "name": payment.name,
            "amount": payment.amount,
            "status": payment.status,
            "payment_at": payment.payment_at,
            "payment_id": payment.payment_id,
        }

        if plan_doc:
            result["membership_plan"] = {
                "name": plan_doc.name,
                "title": plan_doc.title,
                "duration_days": plan_doc.duration_days,
                "price": plan_doc.price,
                "description": plan_doc.description or ""
            }

        return res_success("Get list detail payment successfully", result)

    except frappe.DoesNotExistError:
        return res_error("Payment not found..","payment_id", 404)
    except Exception as e:
        return res_error("Unable to fetch payment history.","server_error", 500)
