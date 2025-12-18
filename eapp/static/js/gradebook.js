document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.score-input');

    inputs.forEach(input => {
        calculateRow(input.closest('tr'));
        input.addEventListener('input', function() {
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
        setTimeout(() => msg.style.display = 'none', 2000);
    }
}

function updateScore(inputElement, enrollmentId, scoreType) {
    const value = inputElement.value;

    fetch('/api/update-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            'enrollment_id': enrollmentId,
            'score_type': scoreType,
            'value': value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Đã lưu thành công!');
            inputElement.style.borderColor = "green";
            calculateRow(inputElement.closest('tr'));
            showSuccess();
        } else {
            alert(data.msg);
            inputElement.style.borderColor = "red";
        }
    })
    .catch(err => {
        console.error(err);
    });
}