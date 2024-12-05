document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const taskId = this.closest('.task-item').dataset.taskId;
            const isDone = this.checked ? 1 : 0;

            fetch(`/tasks/${taskId}/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ is_done: isDone })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error updating task');
                }
            });
        });
    });

    document.querySelectorAll('.unpin-btn').forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.closest('.task-item').dataset.taskId;

            fetch(`/tasks/${taskId}/unpin/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ is_priority: 0 })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error unpinning task');
                }
            });
        });
    });

    document.querySelectorAll('.pin-btn').forEach(button => {
        button.addEventListener('click', function () {
            const taskId = this.closest('.task-item').dataset.taskId;

            fetch(`/tasks/${taskId}/pin/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ is_priority: 1 })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error pinning task');
                }
            });
        });
    });

    // Handle delete all completed tasks (with AJAX)
    let deleteAllClicked = false; // Track if the button was clicked once

    document.querySelector('#delete-all-btn').addEventListener('click', function () {
        if (deleteAllClicked) {
            // Proceed with deleting completed tasks if clicked twice
            fetch('/task/delete/completed/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({})  // No body data, we just need to trigger the delete action
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error deleting completed tasks');
                }
            });
        } else {
            // Change the button color and show confirmation
            this.style.backgroundColor = '#ffa726';  // Lighter color on first click
            this.textContent = 'Are you sure? Click again to delete';  // Update the button text
            deleteClicked = true;  // Mark that the button was clicked once
        }
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
