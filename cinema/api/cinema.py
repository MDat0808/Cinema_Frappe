import frappe
from frappe import _
from .response import res_error, res_success


@frappe.whitelist(allow_guest=True)
def get_cinema_by_province(province):
    """
    Trả về danh sách cinema thuộc một tỉnh/thành.
    """
    if not province:
        return res_error("Province is required", "province", "REQUIRED")

    cinema = frappe.get_all(
        "Cinema",
        filters={"province": province},
        fields=["cinema_name","location","description"],
        distinct=True
    )

    region = frappe.get_value("Province", {"province_name": province}, "region")
    
    response = {"region": region,"province": province,
    "cinema": cinema }

    return res_success("Get list province by region success",response)




@frappe.whitelist(allow_guest=True)
def get_rooms_with_seats_by_cinema(cinema):
    """
    Trả về danh sách room thuộc một cinema.
    """
    if not cinema:
        return res_error("Cinema is required", "cinema", "REQUIRED")

    cinema_filter = frappe.get_value("Cinema", {"cinema_name": cinema}, ["name", "province"], as_dict=True)

    rooms = frappe.get_all(
        "Room",
        filters={"cinema": cinema_filter.name},
        fields=["name","room_name"],
        distinct=True
    )
    print(rooms)
    room_list = []
    for room in rooms:
        seats = frappe.get_all(
            "Seat",
            filters={"room": room.name},
            fields=["seat_number", "seat_type"]
        )

        room_list.append({
            "room_name": room.room_name,
            "seats": seats
        })


    response = {
        "province": cinema_filter.province,
        "cinema": {
            "cinema_name": cinema,
            "rooms": room_list
        },
    }

    return res_success("Get list room by cinema success",response)