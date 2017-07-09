import unicodecsv
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema
import updates

OSM_FILE = "chicago_illinois.osm" # OSM file to be processed

# file path
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"


PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
"""Regular expression to recognise problem characters"""

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'category']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'category']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_category='regular'):
    
    """
    Clean and shape node or way XML element to Python dict.
    Paras:
        element (obj): element found using ET.iterparse().
        node_attr_fields (list): node attribute fields to be passed to output dict
        way_attr_fields (list): way attribute fields to be passed to output dict
        problem_chars (regex): regular expression to recognise problem characters
        default_tag_category (str): default value to be passed to the 'category' 
            field in output dict
    Returns:
        dict of node/way element attributes and attributes of child elements (tags)
        format if node: {'node': node_attribs, 'node_tags': tags}
        format if way: {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
    """
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = [] # Handle secondary tags the same way for node and way elements

    nd_position = 0

    for child in element:
        if child.tag == 'tag':
            # Strip 'k' value to ensure those reflecting "type" are properly handled later
            key_attrib = child.attrib['k'].strip()
            if not PROBLEMCHARS.search(key_attrib):
                tag = {'category': default_tag_category}
                tag['id'] = element.attrib['id'].strip()
                key_colon = key_attrib.find(':')
                if key_colon > 0:
                    tag['key'] = key_attrib[(key_colon + 1):]
                    tag['category'] = key_attrib[:(key_colon)]
                else:
                    tag['key'] = key_attrib
                value = updates.update_value(child.attrib['v'].strip(), key_attrib)
                tag['value'] = value
                tags.append(tag)
        if child.tag == 'nd':
            way_node = {}
            way_node['id'] = element.attrib['id'].strip()
            way_node['node_id'] = child.attrib['ref'].strip()
            way_node['position'] = nd_position
            way_nodes.append(way_node)
            nd_position += 1
    if element.tag == 'node':
        for field in NODE_FIELDS:
            node_attribs[field] = element.attrib[field].strip()
        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        for field in WAY_FIELDS:
            way_attribs[field] = element.attrib[field].strip()
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):

    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate=False):


    with open(NODES_PATH, 'wb') as nodes_file, \
         open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
         open(WAYS_PATH, 'wb') as ways_file, \
         open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
         open(WAY_TAGS_PATH, 'wb') as way_tags_file:

        nodes_writer = unicodecsv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = unicodecsv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = unicodecsv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = unicodecsv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = unicodecsv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

process_map(OSM_FILE)
