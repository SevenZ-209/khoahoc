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

    // 2. Xử lý khi tích vào ô Có/Vắng
    const radios = document.querySelectorAll('.attendance-radio');
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            const enrollmentId = this.dataset.enrollment;
            const isPresent = (this.value === '1'); // 1=True, 0=False
            const date = document.getElementById('attendanceDate').value;

            // Gọi hàm lưu
            saveAttendance(enrollmentId, date, isPresent);
        });
    });
});

// Hàm gọi API
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
            alert('Lỗi lưu dữ liệu!');
        }
    })
    .catch(err => console.error(err));
}

// Hàm hiện thông báo
function showSuccessMessage() {
    const msg = document.getElementById('msg');
    if(msg) {
        msg.style.display = 'block';
        setTimeout(() => { msg.style.display = 'none'; }, 800);
    }
}