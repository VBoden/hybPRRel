from os import listdir
from os.path import isfile, join
import os
from pathlib import Path
from shutil import copyfile

import xml.etree.ElementTree as ET

from notcomitableConstants import localextensions, extentions_dir


def get_all_extension_names(localextensions):
    mytree = ET.parse(localextensions)
    myroot = mytree.getroot()
    names = []
    for el in myroot[0]:
        if el.tag == "extension":
            if "name" in el.attrib:                
#                print(el.attrib)
#                print(el.attrib["name"])
                names.append(el.attrib["name"])
            elif "dir" in el.attrib:
#                print(el.attrib)
#                print(el.attrib["dir"].split("/")[-1])
                names.append(el.attrib["dir"].split("/")[-1])
    return names
    
def get_relations(extentions_dir_path, extension_names):
    dependencies_map = {}
    project_collections = [c for c in listdir(extentions_dir_path) if not isfile(join(extentions_dir_path, c))]
#    print(project_collections)
    not_look_folders = [".idea","idea-module-files","platform"]
    for pr_collection in project_collections:
        if pr_collection in not_look_folders:
            continue
#        print("\n\n\n")
#        print(pr_collection)
        path_to_collection = join(extentions_dir_path, pr_collection)
#        print(listdir(path_to_collection))
        projects = [f for f in listdir(path_to_collection) if not isfile(join(path_to_collection, f))]
        for pr in projects:
            read_ext_info_file(path_to_collection, pr, dependencies_map,extension_names)
#            print(" dir name ",pr)
#            path_to_project = join(path_to_collection, pr)
#            file_path = join(path_to_project, "extensioninfo.xml")
#            if Path(file_path).exists():
#                print(file_path)
#                ext_name, required_exts = get_dependencies(file_path)
#                if ext_name in extension_names:
#                    dependencies_map[ext_name] = required_exts
    return dependencies_map

def read_ext_info_file(path_to_collection, pr, dependencies_map,extension_names):
    path_to_project = join(path_to_collection, pr)
    file_path = join(path_to_project, "extensioninfo.xml")
    if Path(file_path).exists():
#        print(file_path)
        ext_name, required_exts = get_dependencies(file_path)
        if ext_name in extension_names:
            dependencies_map[ext_name] = required_exts
    else:
        projects = [f for f in listdir(path_to_project) if not isfile(join(path_to_project, f))]
        for pr in projects:
            read_ext_info_file(path_to_project, pr, dependencies_map,extension_names)
    

def get_dependencies(file_path):
    tree = ET.parse(file_path)
    myroot = tree.getroot()
#    print("\n\n\n")
#    print(myroot[0].attrib['name'])
    names = []
    for el in myroot[0].findall('requires-extension'):
        names.append(el.attrib["name"])
#    for el in myroot[0][0]:
#        if el.tag == "extension":
#            if "name" in el.attrib:                
#                print(el.attrib)
#                print(el.attrib["name"])
#                names.append(el.attrib["name"])
#            elif "dir" in el.attrib:
#                print(el.attrib)
#                print(el.attrib["dir"].split("/")[-1])
#                names.append(el.attrib["dir"].split("/")[-1])
#    print(names)
#    print("\n\n\n")
    return myroot[0].attrib['name'], names

def reformat_relations(relations):
    dependencies_list = []
    sorted_rel = dict(sorted(relations.items(), key=lambda item: len(item[1])))
#    print(sorted_rel)
    for key in sorted_rel:
#        print(key)
        for value in sorted_rel[key]:
#            print("_____"+value)
            dependencies_list.append({key : value})
    return dependencies_list


dir_path = os.path.dirname(os.path.realpath(__file__))


local_ext_path = os.path.dirname(os.path.realpath(localextensions))

extentions_dir_path = os.path.dirname(os.path.realpath(extentions_dir+"platform"))

nam = get_all_extension_names(localextensions)
print(nam)
relations = get_relations(extentions_dir_path, nam)
print("\n\n\n")
print(relations)
relations_list = reformat_relations(relations)
print("\n\n\n")
print(relations_list)




def test():
    print("\n\n\n ====strat parsing =======\n\n\n ")
    mytree = ET.parse(localextensions)
    myroot = mytree.getroot()
    print(myroot.attrib)
    print(myroot[0][1].tag)
    print(myroot[0][1].attrib)
    print(myroot[0][1].attrib["name"])    
    print("\n\n=====end of root ===== \n\n\n ")
    
    project_collections = [c for c in listdir(dir_path) if not isfile(join(dir_path, c))]        
    print(project_collections)

