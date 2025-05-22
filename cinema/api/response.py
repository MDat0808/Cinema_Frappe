import frappe


def res_success(message: str, data=None, result=None, paging=None, status_code=200):
    # request_id = getattr(frappe.local, 'request_id', str(uuid.uuid4()))
    # trace_id = getattr(frappe.local, 'trace_id', str(uuid.uuid4()))

    response = {
        "message": message,
        "data": data or {},
        # "meta": {
        #     "request_id": request_id,
        #     "trace_id": trace_id
        # }
    }

    # if result is not None:
    #     response["result"] = result

    # if paging:
    #     response["paging"] = paging

    frappe.local.response["http_status_code"] = status_code
    frappe.local.response.update(response)
    frappe.local.flags.write_response = True


def res_error(message, field, code, status_code=400):
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["message"] = "Validation failed"
    frappe.local.response["errors"] = [{
        "message": message,
        "field": field,
        "code": code
    }]
    # frappe.local.response["meta"] = {
    #     "request_id": request_id,
    #     "trace_id": trace_id
    # }
    frappe.local.flags.write_response = True


