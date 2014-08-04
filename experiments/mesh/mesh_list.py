import pickle
import xml.etree.ElementTree as ET

tree = ET.parse('desc2014.xml')
root = tree.getroot()
mesh = [a.text for a in root.findall('./DescriptorRecord/DescriptorName/String')]
print len(mesh)
with open('mesh_list', 'w') as f:
    pickle.dump(mesh, f)
