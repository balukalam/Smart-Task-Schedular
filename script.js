setInterval(() => {
    const now = new Date();

    tasks.forEach(task => {
        const taskDate = task[2]; // date
        const taskTime = task[3]; // time

        const taskDateTime = new Date(taskDate + "T" + taskTime);

        const diff = (taskDateTime - now) / 1000; // seconds

        // 🔔 Alert 10 seconds before task (for testing)
        if (diff > 0 && diff < 600) {
            alert("⏰ Reminder: " + task[1]);
        }
    });

}, 5000);