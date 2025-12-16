document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.score-input');

    inputs.forEach(input => {
        input.addEventListener('input', function() {
            calculateRow(this.closest('tr'));
        });

        input.addEventListener('change', function() {
            const enrollmentId = this.dataset.enrollment;
            const scoreType = this.dataset.type;
            const value = this.value;

            fetch('/api/update-score', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    enrollment_id: enrollmentId,
                    score_type: scoreType,
                    value: value
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    showSuccess();
                } else {
                    alert('Lỗi lưu điểm!');
                }
            });
            calculateRow(this.closest('tr'));
        });
    });
});

function calculateRow(row) {
    const inputs = row.querySelectorAll('.score-input');

    let total = 0;
    let count = 0;

    inputs.forEach(input => {
        let val = parseFloat(input.value);
        if (!isNaN(val)) {
            total += val;
        }
    });

    count = inputs.length;

    let avg = 0;
    if (count > 0) {
        avg = total / count;
    }

    avg = Math.round(avg * 100) / 100;

    const avgCell = row.querySelector('.avg-score');
    if (avgCell) avgCell.innerText = avg;

    const resultCell = row.querySelector('.result-text');
    if (resultCell) {
        if (avg >= 5.0) {
            resultCell.innerText = "Đạt";
            resultCell.className = "text-center fw-bold result-text text-success";
        } else {
            resultCell.innerText = "Không đạt";
            resultCell.className = "text-center fw-bold result-text text-danger";
        }
    }
}

function showSuccess() {
    const msg = document.getElementById('msg');
    if(msg) {
        msg.style.display = 'block';
        setTimeout(() => msg.style.display = 'none', 1000);
    }
}