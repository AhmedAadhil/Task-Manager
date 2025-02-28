const token = localStorage.getItem("access_token");

//Fetch Tasks
async function fetchTasks() {
    const response = await fetch("/api/tasks", {
        method: "GET",
        headers: { "Authorization": `Bearer ${token}` }
    });
    const tasks = await response.json();
    displayTasks(tasks);
}

//Display Tasks
function displayTasks(tasks) {
    const taskList = document.getElementById("taskList");
    taskList.innerHTML = "";
    tasks.forEach(task => {
        const li = document.createElement("li");
        li.innerHTML = `
            <span class="${task.completed ? 'completed' : ''}">${task.title}</span>
            <button onclick="toggleTask(${task.id})">✔</button>
            <button onclick="deleteTask(${task.id})">🗑</button>
        `;
        taskList.appendChild(li);
    });
}

//Add Task
async function addTask() {
    const taskTitle = document.getElementById("taskInput").value;
    if (!taskTitle) {
        alert("Task title cannot be empty!");
        return;
    }

    const response = await fetch("/api/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ title: taskTitle })
    });

    if (response.ok) {
        fetchTasks();  // Refresh list
        document.getElementById("taskInput").value = "";  // Clear input
    } else {
        alert("Error adding task.");
    }
}

//Toggle Task Completion
async function toggleTask(taskId) {
    const response = await fetch(`/api/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        fetchTasks();  // Refresh list
    } else {
        alert("Error updating task.");
    }
}

//Delete Task
async function deleteTask(taskId) {
    const response = await fetch(`/api/tasks/${taskId}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        fetchTasks(); 
    } else {
        alert("Error deleting task.");
    }
}

fetchTasks();  // this function loads all the tasks when the page loads