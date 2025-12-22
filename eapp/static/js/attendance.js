document.addEventListener('DOMContentLoaded', function() {
    const btnChangeDate = document.querySelector('button[onclick="location.reload()"]');
    if(btnChangeDate) {
        btnChangeDate.onclick = function(e) {
            e.preventDefault();
            const date = document.getElementById('attendanceDate').value;
            const currentUrl = window.location.pathname;
            window.location.href = `${currentUrl}?date=${date}`;
        }
    }

    const radios = document.querySelectorAll('.attendance-radio');
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            const enrollmentId = this.dataset.enrollment;
            const isPresent = (this.value === '1');
            const date = document.getElementById('attendanceDate').value;
            saveAttendance(enrollmentId, date, isPresent);
        });
    });
});

function saveAttendance(enrollmentId, date, isPresent) {
    fetch('/api/attendance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            enrollment_id: enrollmentId,
            date: date,
            present: isPresent
        })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            showSuccessMessage();
        } else {
            alert('Lỗi: ' + data.msg);
            location.reload();
        }
    })
    .catch(err => console.error(err));
}

function showSuccessMessage() {
    const msg = document.getElementById('msg');
    if(msg) {
        msg.style.display = 'block';
        setTimeout(() => { msg.style.display = 'none'; }, 800);
    }
}