function renderCharts(revenueLabels, revenueData, courseLabels, courseData, passLabels, passData, failData) {
    
    // 1. VẼ BIỂU ĐỒ DOANH THU
    const ctxRevenue = document.getElementById('revenueChart');
    if (ctxRevenue) {
        new Chart(ctxRevenue, {
            type: 'bar',
            data: {
                labels: revenueLabels, // Nhận từ tham số
                datasets: [{
                    label: 'Doanh thu (VNĐ)',
                    data: revenueData, // Nhận từ tham số
                    backgroundColor: 'rgba(25, 135, 84, 0.6)',
                    borderColor: 'rgba(25, 135, 84, 1)',
                    borderWidth: 1
                }]
            }
        });
    }

    // 2. VẼ BIỂU ĐỒ SỐ LƯỢNG HỌC VIÊN
    const ctxCourse = document.getElementById('courseChart');
    if (ctxCourse) {
        new Chart(ctxCourse, {
            type: 'doughnut',
            data: {
                labels: courseLabels,
                datasets: [{
                    data: courseData,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                }]
            }
        });
    }

    // 3. VẼ BIỂU ĐỒ TỶ LỆ ĐẠT (PASS RATE)
    const ctxPass = document.getElementById('passRateChart');
    if (ctxPass) {
        new Chart(ctxPass, {
            type: 'bar',
            data: {
                labels: passLabels,
                datasets: [
                    {
                        label: 'Đạt',
                        data: passData,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    },
                    {
                        label: 'Không đạt',
                        data: failData,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    }
                ]
            },
            options: {
                scales: {
                    x: { stacked: true },
                    y: { stacked: true, beginAtZero: true }
                }
            }
        });
    }
}