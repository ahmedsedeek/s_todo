import os
    
def write_file(filepath,content):
    """ open the file in write mode
    Arguement: filepath & new content to be writen
    Return:file contnet in a list"""
    with open(filepath,"w") as file_loc:
        return file_loc.writelines(content) 
    
def read_file(filepath):
    """ open the file in read mode
    Arguement: filepath
    Return:file contnet in a list"""

    with open(filepath,"r") as file_loc:
        return file_loc.readlines()
    
def create_dict(data):
    projects = []
    final = {}
    for index, item in enumerate(data):
        proj = item.split(":")[0].replace(" ","_")
        task = item.split(":")[1].replace("\n","")

        if index == 0 or proj not in projects:
            final[proj] = []
            final[proj].append(task)
        else:
            final[proj].append(task)
        if proj not in projects:
            projects.append(proj)
    return final, projects