function pay(receiptId) {
    if (confirm('Xác nhận học viên đã đóng đủ tiền cho hóa đơn #' + receiptId + '?')) {
        fetch('/api/pay/' + receiptId, {
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
                alert('Lỗi: ' + data.msg);
            }
        })
        .catch(err => {
            console.error(err);
            alert('Có lỗi');
        });
    }
}