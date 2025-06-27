import frappe
import paypalrestsdk
from cinema.integrations.paypal_config import init_paypal
from frappe.utils import now_datetime

@frappe.whitelist()
def create_paypal_payment(payment_id):
    init_paypal()

    payment_doc = frappe.get_doc("Membership Payment", payment_id)
    user_membership = frappe.get_all(
        "User Membership",
        filters={"user": payment_doc.user},
        fields=["name", "membership_plan", "is_active"],
        limit=1
    )

    if user_membership:
        user_membership = user_membership[0]
    else:
        frappe.throw("Không tìm thấy User Membership cho người dùng này.")  


    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": f"{frappe.utils.get_url()}/api/method/cinema.integrations.paypal_payment.execute_payment?payment_id={payment_id}",
            "cancel_url": f"{frappe.utils.get_url()}/payment-cancelled"
        },
        "transactions": [{
            "amount": {"total": str(payment_doc.amount), "currency": "USD"},
            "description": f"Membership for {user_membership.name}"
        }]
    })

    if payment.create():
        frappe.db.set_value("Membership Payment", payment_id, {
            "payment_id": payment.id,
            "status": "Pending"
        })
        frappe.db.commit()

        for link in payment.links:
            if link.rel == "approval_url":
                return {"status": "success", "redirect_url": link.href}
    else:
        frappe.db.set_value("Membership Payment", payment_id, "payment_status", "Failed")
        frappe.log_error(str(payment.error), "PayPal Create Payment Error")
        return {"status": "failed", "error": str(payment.error)}
    
@frappe.whitelist(allow_guest=True)
def execute_payment(paymentId, PayerID, payment_id):
    init_paypal()
    payment = paypalrestsdk.Payment.find(paymentId)

    if payment.execute({"payer_id": PayerID}):
        transaction_id = payment['transactions'][0]['related_resources'][0]['sale']['id']

        frappe.db.set_value("Membership Payment", payment_id, {
            "transaction_id": transaction_id,
            "status": "Paid",
            "payment_at": now_datetime()
        })

        # Optionally update User Membership
        payment_doc = frappe.get_doc("Membership Payment", payment_id)
        user_memberships = frappe.get_all(
            "User Membership",
            filters={"user": payment_doc.user},
            fields=["name", "membership_plan", "is_active"],
            limit=1
        )        

        if user_memberships:
            user_membership_doc = frappe.get_doc("User Membership", user_memberships[0].name)
            user_membership_doc.is_active = 1
            user_membership_doc.save()

        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = f"/payment-success?payment_id={payment_id}"
    else:
        frappe.db.set_value("Membership Payment", payment_id, "payment_status", "Failed")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = f"/payment-failed?payment_id={payment_id}"
