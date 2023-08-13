import streamlit as st
import functions as f
import os


path = "files/todo_"
proj_count_path = "files/projects.txt"
proj_names_path = "files/projects_names.txt"
done_todos_path = "files/done.txt"

st.title("Ahmed Sedeek Apps")

#Function to create file if the file doesn't exist and read the whole file again.
def path_create(path):
    if os.path.exists(path):
        result = f.read_file(path)
    else:
        f.write_file(path,"")
        result = f.read_file(path)
    return result
#end of create file function


projects_count = path_create(proj_count_path)
projects_names = path_create(proj_names_path)
done_todos = path_create(done_todos_path)




col1, col2 = st.columns(2)
col1.text_input("",placeholder="Write your Project Name", key="project_name")
col2.markdown('#')

if col2.button("Add Project",key="add_proj"):

    if len(projects_count) == 0:
        projects_count.append("1\n")
        projects_names.append(st.session_state["project_name"].lower()+"\n")
        f.write_file(proj_count_path,projects_count)
        f.write_file(proj_names_path,projects_names)

    else:
        projects_count = f.read_file(proj_count_path)
        projects_names = f.read_file(proj_names_path)
        new_proj_num = int(projects_count[-1].replace("\n","")) + 1
        projects_count.append(str(new_proj_num)+"\n")
        projects_names.append(st.session_state["project_name"]+"\n")
        f.write_file(proj_count_path,projects_count)
        f.write_file(proj_names_path,projects_names)

#DELET Button Function
def done_btn():
    try:
        for i, project in enumerate(projects_count):
            project = project.replace("\n","")
            todos = f.read_file(path+project+".txt")
            new_todos = []
            done_todos = f.read_file(done_todos_path)
            for index, todo in enumerate(todos):
                index = str(index)
                todo_key = st.session_state[f"todo_{project}_{index}"]
               
                if todo_key == True:
                    new_project_name = projects_names[i].replace("\n","")
                    done_todos.append(f"{new_project_name}:{todo}")
                else:
                    new_todos.append(todo)

            todos = new_todos
            f.write_file(f"{path}{project}.txt",todos)

            if st.session_state[f"done_{project}"]:
                f.write_file(done_todos_path,done_todos)
            else:
                pass
            del st.session_state[f"input_{project}"]
                
            if len(todos) == 0:
                projects_count.pop(i)
                projects_names.pop(i)
                f.write_file(proj_count_path,projects_count)
                f.write_file(proj_names_path,projects_names)
    except:
        print("eror")
        #st.error(icon="🤖",body="Please select something to be deleted!")
#end of delete & complete function

#delete done tasks functiom
def delete_done_todo():
    data = f.read_file(done_todos_path)
    done_checklist = f.create_dict(data)[0]
    done_projects = f.create_dict(data)[1]
    dummy_list = []
    for i, done_project in enumerate(done_projects):
        for list_index, done_todo in enumerate(done_checklist[done_project]):
            done_todo_key = st.session_state[f"done_{i}_{list_index}"]

            if done_todo_key == True:
                pass
            else:
                dummy_list.append(f"{done_project}:{done_todo}\n")
    f.write_file("files/done.txt",dummy_list)    

if 'something' not in st.session_state:
    st.session_state.something = ''
    st.session_state.something_index = ''


def submit():
    for proj_index, project in enumerate(projects_count):
        project = project.replace("\n","")
        if st.session_state[f"input_{project}"] != "":
            st.session_state.something = st.session_state[f"input_{project}"]
            st.session_state.something_index = str(proj_index)
            st.session_state[f"input_{project}"] = ''
            


for proj_index, project in enumerate(projects_count):
    project = project.replace("\n","")

    projects_names = f.read_file(proj_names_path)

    with st.expander(F"{projects_names[proj_index].upper()}"):

        col1, col2 = st.columns(2)
        col1.subheader(F"{projects_names[proj_index].title()}")
        #st.session_state[f"input_{project}"] = ''
        col1.text_input("TYPE YOUR TODO: ", placeholder="Write your Task", key=f"input_{project}",on_change=submit)

        todos = path_create(f"{path}{project}.txt")

        if st.session_state.something_index == str(proj_index):
            todo = st.session_state.something.title()
            #print(st.session_state.something)
            st.session_state.something = ''
        else:
            todo = ''

        if todo == '' or f"{todo}\n" in todos:
            pass
        else:
            todos.append(todo + "\n")
            #col1.checkbox(todo,key=f"todo_{project}_{i_str}")
            f.write_file(f"{path}{project}.txt",todos)
            #todos_len = str(len(todos))
            #st.experimental_rerun()


        if len(todos) == 0:
            pass
        else:
            for i,todo in enumerate(todos):
                i_str = str(i)
                col1.checkbox(todo,key=f"todo_{project}_{i_str}")
                #col2.selectbox("#",('Low Urgency', 'Mid Urgency', 'High Urgency'),key=f"dropdown_{project}_{i_str}")

        #todo = st.session_state[f"input_{project}"].title()


            
        col1_1, col1_2 = col1.columns(2)
        col1_1.button("Complete",on_click=done_btn,key=f"done_{project}")
        col1_2.button("Delete",on_click=done_btn,key=f"delete_{project}")
        


    
with st.sidebar:
    ss= st.subheader("Done Tasks")
    data = f.read_file(done_todos_path)
    done_checklist = f.create_dict(data)[0]
    done_projects = f.create_dict(data)[1]
    for index,project in enumerate(done_projects):
        st.text(project.replace("_"," ").upper())
        for list_index, checklist in enumerate(done_checklist[project]):
            st.checkbox(checklist,key=f"done_{index}_{list_index}")
    st.button("Delete",on_click=delete_done_todo)

