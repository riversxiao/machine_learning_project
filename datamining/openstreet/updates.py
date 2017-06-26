
from audit_file import street_type_re, post_code_re, phone_re
import re


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

street_type_mapping = { "St": "Street",
                        "St.": "Street",
                        "Ave": "Avenue",
                        "Ave." : "Avenue",
                        "Rd" : "Road",
                        "Rd." : "Road",
                        "Cir" : "Circle",
                        'Ln' : "Line",
                        "Dr" : "Drive",
                        "Ct" : "Court",
                        "Trl" : "Trail"
                        }

def update_street_name(name,street_type_mapping):
    m = street_type_re.search(name)
    if m:
        if m.group() in street_type_mapping.keys():
            name = re.sub(m.group(),street_type_mapping[m.group()],name)
        return name
    else:
        return None
def update_phone_number(value):
    value = re.sub(r'\D', "", value)
    return value
def update_value(value, key):
    if key == "addr:street":
        return update_street_name(value,street_type_mapping)
    elif key == "phone":
        return update_phone_number(value)
    else:
        return value
