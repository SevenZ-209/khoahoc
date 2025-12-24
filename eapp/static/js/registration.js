function deleteRegistration(detailId) {
    if (confirm("Bạn có chắc chắn muốn hủy đăng ký lớp học này không?")) {
        fetch(`/api/cancel-reg/${detailId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.msg || "Đã hủy đăng ký thành công!");
                location.reload();
            } else {
                alert(data.msg);
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert("Lỗi kết nối đến hệ thống!");
        });
    }
}


function payOnline(receiptId) {
    if (confirm('Bạn có chắc muốn thanh toán học phí cho hóa đơn này?')) {
        fetch(`/api/student-pay/${receiptId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.msg);
                location.reload();
            } else {
                alert(data.msg);
            }
        })
        .catch(err => console.error(err));
    }
}
