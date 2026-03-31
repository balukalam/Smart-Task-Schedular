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

    let percent = total === 0 ? 0 : (completed / total) * 100;
    document.getElementById("progressFill").style.width = percent + "%";
}

function displayTasks() {
    let table = document.getElementById("taskTable");
    let search = document.getElementById("searchInput").value.toLowerCase();

    table.innerHTML = "";

    tasks
    .filter(task => task.name.toLowerCase().includes(search))
    .forEach((task, index) => {

        let priorityClass = task.priority.toLowerCase();

        table.innerHTML += `
        <tr>
            <td>${task.name}</td>
            <td>${task.date}</td>
            <td>${task.time}</td>
            <td class="${priorityClass}">${task.priority}</td>
            <td>${task.status}</td>
            <td>
                <button onclick="deleteTask(${index})">❌</button>
            </td>
        </tr>`;
    });

    updateStats();
}

function addTask() {
    let name = document.getElementById("taskInput").value;

    if (!name) {
        alert("Enter task!");
        return;
    }

    let task = {
        name,
        date: document.getElementById("dateInput").value,
        time: document.getElementById("timeInput").value,
        priority: document.getElementById("priorityInput").value,
        status: document.getElementById("statusInput").value
    };

    tasks.push(task);
    saveTasks();
    displayTasks();

    document.getElementById("taskInput").value = "";
}

function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    displayTasks();
}

displayTasks();
