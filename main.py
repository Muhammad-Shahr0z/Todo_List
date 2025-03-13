import streamlit as st
import pandas as pd
import os

# File path for storing tasks
task_file = "tasks.csv"

# Initialize session state for tasks
if "tasks" not in st.session_state:
    if os.path.exists(task_file):
        st.session_state.tasks = pd.read_csv(task_file)
    else:
        st.session_state.tasks = pd.DataFrame(columns=["Task", "Status"])

# Function to save tasks to CSV
def save_tasks():
    st.session_state.tasks.to_csv(task_file, index=False)

# Enhanced CSS with Additional Animations
st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .task-row {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-in;
        transition: all 0.3s ease;
    }
    
    .task-row:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .task-text {
        flex: 4;
        font-size: 1.1rem;
        padding: 0 1rem;
        margin: 0;
        display: flex;
        align-items: center;
        position: relative;
    }
    
    .completed-task {
        animation: strikeThrough 0.5s ease-out forwards;
    }
    
    @keyframes strikeThrough {
        0% { width: 0; }
        100% { width: 100%; }
    }
    
    .completed-task::after {
        content: "";
        position: absolute;
        left: 0;
        top: 50%;
        width: 100%;
        height: 2px;
        background: #4caf50;
        animation: strikeThrough 0.5s ease-out forwards;
    }
    
    .status-dropdown {
        flex: 2;
        min-width: 150px;
        transition: all 0.3s ease;
    }
    
    .delete-btn {
        flex: 1;
        display: flex;
        justify-content: flex-end;
    }
    
    .stButton button {
        transition: all 0.3s ease !important;
        animation: pulse 2s infinite;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        animation: none;
    }
    
    .pending { 
        color: #ff9800; 
        font-weight: bold; 
        animation: bounce 1s infinite;
    }
    
    .completed { 
        color: #4caf50; 
        font-weight: bold; 
        animation: fadeIn 0.5s ease-out;
    }
    
    [data-baseweb=select] { 
        border-radius: 8px !important;
        padding: 0.25rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-baseweb=select]:hover {
        transform: scale(1.02);
    }
    
    .stTextInput input:focus { 
        box-shadow: 0 0 0 2px #4a90e2 !important; 
        animation: pulse 1.5s infinite;
    }
    
    .header-animation {
        animation: slideIn 0.8s ease-out, fadeIn 1s ease-in;
    }
    
    .stats-number {
        animation: fadeIn 0.5s ease-out, bounce 0.5s ease;
    }
    
    .footer {
        position: relative;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.9em;
        margin-top: 2rem;
        border-top: 1px solid #eee;
        animation: fadeIn 1s ease-in;
    }
    
    .footer:hover {
        animation: pulse 1s infinite;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Animated Header
st.markdown('<h1 class="header-animation">Task Manager ✨</h1>', unsafe_allow_html=True)
st.markdown("---")

# Input Section with Animation
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        new_task = st.text_input("Add a new task:", placeholder="Enter your task here...")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ Add Task", use_container_width=True):
            if new_task:
                new_entry = pd.DataFrame([[new_task, "Pending"]], columns=["Task", "Status"])
                st.session_state.tasks = pd.concat([st.session_state.tasks, new_entry], ignore_index=True)
                save_tasks()
                st.toast(f"🚀 Task added: {new_task}", icon="✅")
                st.rerun()
            else:
                st.warning("Please enter a task before adding!")

# Task List with Enhanced Animations
st.subheader("📋 Your Tasks")
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

if not st.session_state.tasks.empty:
    for index, row in st.session_state.tasks.iterrows():
        task_container = st.container()
        with task_container:
            cols = st.columns([4, 2, 1])
            
            # Animated Task Text
            with cols[0]:
                status_class = "completed" if row["Status"] == "Completed" else "pending"
                task_animation = "completed-task" if row["Status"] == "Completed" else ""
                st.markdown(
                    f"<div class='task-text'>"
                    f"<span style='margin-right: 1rem;' class='bounce'>▢</span>"
                    f"<span class='{status_class} {task_animation}'>{row['Task']}</span>"
                    f"</div>", 
                    unsafe_allow_html=True
                )

            # Animated Status Dropdown
            with cols[1]:
                status = st.selectbox(
                    "",
                    ["Pending", "Completed"],
                    index=["Pending", "Completed"].index(row["Status"]),
                    key=f"status_{index}",
                    label_visibility="collapsed"
                )
                if status != row["Status"]:
                    st.session_state.tasks.at[index, "Status"] = status
                    save_tasks()
                    st.rerun()

            # Animated Delete Button
            with cols[2]:
                if st.button("🗑️", key=f"delete_{index}", help="Delete Task"):
                    st.session_state.tasks = st.session_state.tasks.drop(index).reset_index(drop=True)
                    save_tasks()
                    st.toast(f"❌ Task deleted: {row['Task']}", icon="⚠️")
                    st.rerun()
        st.markdown("---")
else:
    st.markdown(
        "<div style='text-align: center; padding: 2rem; color: #666; animation: fadeIn 1s ease-in;'>"
        "🎉 No tasks found! Add your first task above!"
        "</div>", 
        unsafe_allow_html=True
    )

# Animated Statistics Footer
completed_tasks = st.session_state.tasks[st.session_state.tasks["Status"] == "Completed"].shape[0]
total_tasks = st.session_state.tasks.shape[0]
progress = completed_tasks / total_tasks if total_tasks > 0 else 0

st.markdown("---")
st.markdown(
    f"<div style='display: flex; justify-content: space-between; color: #666;'>"
    f"<div>Total Tasks: <span class='stats-number'>{total_tasks}</span></div>"
    f"<div>Completed: <span class='stats-number'>{completed_tasks}</span></div>"
    f"<div>Progress: <span class='stats-number'>{progress:.0%}</span></div>"
    f"</div>", 
    unsafe_allow_html=True
)

# Animated Developer Footer
st.markdown(
    "<div class='footer'>Developed by Muhammad Shahroz</div>",
    unsafe_allow_html=True
)