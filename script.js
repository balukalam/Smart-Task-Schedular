let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

function updateStats() {
    let total = tasks.length;
    let completed = tasks.filter(t => t.status === "Completed").length;
    let pending = tasks.filter(t => t.status === "Pending").length;
    let progress = tasks.filter(t => t.status === "In Progress").length;

    document.getElementById("total").innerText = total;
    document.getElementById("completed").innerText = completed;
    document.getElementById("pending").innerText = pending;
    document.getElementById("progress").innerText = progress;
}

function displayTasks() {
    let table = document.getElementById("taskTable");
    table.innerHTML = "";

    tasks.forEach((task, index) => {
        table.innerHTML += `
        <tr>
            <td>${task.name}</td>
            <td>${task.date}</td>
            <td>${task.time}</td>
            <td>${task.priority}</td>
            <td>${task.status}</td>
            <td>
                <button onclick="editTask(${index})">Edit</button>
                <button onclick="deleteTask(${index})">Delete</button>
            </td>
        </tr>`;
    });

    updateStats();
}

function addTask() {
    let name = document.getElementById("taskInput").value;

    if (name === "") {
        alert("Enter task!");
        return;
    }

    let task = {
        name: name,
        date: document.getElementById("dateInput").value,
        time: document.getElementById("timeInput").value,
        priority: document.getElementById("priorityInput").value,
        status: document.getElementById("statusInput").value
    };

    tasks.push(task);
    saveTasks();
    displayTasks();
}

function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    displayTasks();
}

function editTask(index) {
    let newTask = prompt("Edit task:", tasks[index].name);
    if (newTask) {
        tasks[index].name = newTask;
        saveTasks();
        displayTasks();
    }
}

displayTasks();
