
# coding: utf-8


import os
import pprint
import re

# Returns a sample of an input OpenSreetMap (XML) file

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "chicago_illinois.osm"  # original file name 
SAMPLE_FILE = "chicago_illinois_sample.osm"

k = 10 # Parameter: take every k-th top level element

# get the element with tags of node, way or relation
def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
# write the required data to file
with open(SAMPLE_FILE, 'wb') as output:
    output.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write(b'<osm>\n  ')
    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))
    output.write(b'</osm>')

# count the number of each first level element tags in file 
def count_tags(filename):
    context = ET.iterparse(filename, events=('start', 'end'))
    _, root = next(context)
    tagname = []
    for event, elem in context:
        if event == 'end':
            tagname.append(elem.tag)
            root.clear()
    tags = {}
    for i in tagname:
        if i in tags:
            tags[i] +=1
        else:
            tags[i] =1
    return tags

def test():

    tags = count_tags('chicago_illinois_sample.osm')
    pprint.pprint(tags)
    
if __name__ == "__main__":
    test()


# check if any problemchars in keys

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# define functions to return the number of keys in each type
def key_type(element, keys, all_keys):
    if element.tag == "tag":
        k = element.attrib["k"]
        if re.search(lower, k):
            keys["lower"]+=1
            all_keys['lower_key'].add(k)
        elif re.search(lower_colon,k):
            keys["lower_colon"]+=1
            all_keys['lower_colon_key'].add(k)
        elif re.search(problemchars,k):
            keys["problemchars"]+=1
            all_keys['problem_key'].add(k)
        else:
            keys["other"]+=1 
            all_keys['other_key'].add(k)
            
    return keys,all_keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    all_keys={"lower_key":set(),'lower_colon_key':set(),'other_key':set(),'problem_key':set()}
    for _, element in ET.iterparse(filename):
        keys,all_keys = key_type(element, keys,all_keys)
    return keys,all_keys

def test():
    keys,all_keys = process_map('chicago_illinois_sample.osm')
    pprint.pprint(keys)
    pprint.pprint(all_keys)



if __name__ == "__main__":
    test()



import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# standardize the format of street name and phone number

# file name
OSMFILE = "chicago_illinois_sample.osm"

# regex for each format
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
post_code_re = re.compile(r'\d{5}$', re.IGNORECASE)
phone_re = re.compile(r'\d{3}-\d{3}-\d{4}$',re.IGNORECASE)
phone_problem_re = re.compile(r'[\(\)\ \+]')

# expected street name 
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# mapping the acronym or other format to the standardized format
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
phone_number_mapping = {"(":"",
                        ")":"",
                        "-":"",
                        "+":"",
                        " ":""
                        }

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
if the info is in required attribute and fall into the previous categories,
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

# update street name with mapping to standard format
def update_street_name(name,street_type_mapping):
    m = street_type_re.search(name)
    if m:
        if m.group() in street_type_mapping.keys():
            name = re.sub(m.group(),street_type_mapping[m.group()],name)
        return name

# update phone number to standard format
def update_phone_number(value):
    value = re.sub(r'\D', "", value)
    return value
 
def test():
    st_types,post_codes,phones = audit(OSMFILE)

    for phone in phones:
        num = re.sub(r'\D', "", phone)  

        
if __name__ == '__main__':
    test()




