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
                alert("Đã hủy đăng ký thành công!");
                location.reload();
            } else {
                alert("Lỗi: Không thể hủy đăng ký. Vui lòng thử lại!");
            }
        })
        .catch(err => {
            console.error('Error:', err);
            alert("Lỗi kết nối đến hệ thống!");
        });
    }
}