import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "chicago_illinois_sample.osm"

# regex for street type, post code and phone number
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
post_code_re = re.compile(r'\d{5}$', re.IGNORECASE)
phone_re = re.compile(r'\d{3}-\d{3}-\d{4}$',re.IGNORECASE)

"""
audit_street_type will add the 
info to to set() if the info matched the regex 
but not in the expected format
"""
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
"""
audit_post_type will add the 
info to to set() if the info does not match the regex 
"""
def audit_post_codes(post_codes, post_code):
    m = post_code_re.match(post_code)
    if not m:
        post_codes.add(post_code)

"""
audit_phone will add the 
info to to set() if the info does not match the regex 
"""
def audit_phone(phones, phone):
    m = phone_re.match(phone)
    if not m:
        phones.add(phone)

# find the element with required attribute

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_post_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def is_phone(elem):
    return (elem.attrib['k'] == "phone")

"""
if the info is in required attribute and match the regex ,
it will be added to the street_types, post_codes and phones 
"""
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    post_codes = set()
    phones = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_post_code(tag):
                    audit_post_codes(post_codes, tag.attrib['v'])
                elif is_phone(tag):
                    audit_phone(phones,tag.attrib['v'])
    osm_file.close()
    return street_types, post_codes, phones
