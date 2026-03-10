import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Smart Task Manager", page_icon="✅", layout="centered")

st.title("🚀 Smart To-Do Manager")
st.write("Organize your tasks efficiently")

FILE = "tasks.csv"


if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Task", "Priority", "Deadline", "Status"])


st.subheader("➕ Add New Task")

task = st.text_input("Task Name")
priority = st.selectbox("Priority", ["Low", "Medium", "High"])
deadline = st.date_input("Deadline", min_value=date.today())

if st.button("Add Task"):
    if task != "":
        new_task = pd.DataFrame(
            [[task, priority, deadline, "Pending"]],
            columns=["Task", "Priority", "Deadline", "Status"],
        )

        df = pd.concat([df, new_task], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Task Added Successfully!")
        st.rerun()

st.divider()


st.subheader("📋 Your Tasks")

for i, row in df.iterrows():

    col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])

    with col1:
        if row["Status"] == "Completed":
            st.write("~~" + row["Task"] + "~~")
        else:
            st.write(row["Task"])

    with col2:
        st.write("Priority:", row["Priority"])

    with col3:
        st.write("Deadline:", row["Deadline"])

    with col4:
        if st.button("✅ Done", key=f"done{i}"):
            df.loc[i, "Status"] = "Completed"
            df.to_csv(FILE, index=False)
            st.rerun()

    with col5:
        if st.button("❌", key=f"del{i}"):
            df = df.drop(i)
            df.to_csv(FILE, index=False)
            st.rerun()

st.divider()

st.subheader("📊 Progress")

total = len(df)
completed = len(df[df["Status"] == "Completed"])

if total > 0:
    progress = completed / total
    st.progress(progress)
    st.write(f"Completed {completed} out of {total} tasks")
else:
    st.write("No tasks yet!")