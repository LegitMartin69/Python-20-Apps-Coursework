import streamlit as st
import functions

todos = functions.get_todos()

def add_todo():
    new_todo = st.session_state["new"]
    todos.append(new_todo + "\n")
    functions.write_todos(todos)

st.title("My ToDo List")
st.subheader("Whats up")

for index, todo in enumerate(todos):
    checkbox = st.checkbox(todo, key=todo)
    if checkbox:
        todos.pop(index)
        functions.write_todos(todos)
        del st.session_state[todo]
        st.rerun()

st.text_input(label=" ", label_visibility="hidden", placeholder="ToDos go here:", on_change=add_todo, key="new")

st.session_state