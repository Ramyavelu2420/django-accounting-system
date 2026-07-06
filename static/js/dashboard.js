// Dashboard JavaScript interactions & Chart rendering

document.addEventListener("DOMContentLoaded", function () {
    // 1. Sidebar Toggling (Mobile)
    const sidebarToggle = document.getElementById("sidebar-toggle-btn");
    const sidebarClose = document.getElementById("sidebar-close-btn");
    const sidebar = document.getElementById("sidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function (e) {
            e.stopPropagation();
            sidebar.classList.toggle("show");
        });
    }

    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener("click", function () {
            sidebar.classList.remove("show");
        });
    }

    // Close sidebar clicking outside on mobile
    document.addEventListener("click", function (event) {
        if (sidebar && sidebar.classList.contains("show") && !sidebar.contains(event.target) && event.target !== sidebarToggle) {
            sidebar.classList.remove("show");
        }
    });

    // 2. Expandable Sidebar Dropdowns
    const dropdownHeaders = document.querySelectorAll(".dropdown-header-link");
    dropdownHeaders.forEach(header => {
        header.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            const targetMenu = document.querySelector(targetId);
            
            if (targetMenu) {
                const isOpen = targetMenu.classList.contains("show");
                
                // Toggle current
                if (isOpen) {
                    targetMenu.classList.remove("show");
                    this.classList.remove("open");
                } else {
                    targetMenu.classList.add("show");
                    this.classList.add("open");
                }
            }
        });
    });

    // 3. ApexCharts Initialization
    // Theme colors matching the screenshots
    const greenColor = '#709f54';
    const redColor = '#ea4335';
    const purpleColor = '#565895';
    const grayColor = '#cbd5e1';

    // A. Cash Flow Chart
    const cashFlowOptions = {
        series: [
            { name: 'Incoming', data: [0, 0, 0, 0, 0, 0] },
            { name: 'Outgoing', data: [0, 0, 0, 0, 0, 0] },
            { name: 'Profit', data: [0, 0, 0, 0, 0, 0] }
        ],
        chart: {
            type: 'line',
            height: 250,
            toolbar: { show: false },
            fontFamily: 'Inter, sans-serif'
        },
        colors: [greenColor, redColor, purpleColor],
        stroke: { width: 3, curve: 'smooth' },
        xaxis: {
            categories: ['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov']
        },
        yaxis: {
            labels: {
                formatter: function (value) { return "₹" + value.toFixed(2); }
            }
        },
        legend: { position: 'top', horizontalAlign: 'left' }
    };
    const cashFlowChartEl = document.querySelector("#cash-flow-chart");
    if (cashFlowChartEl) {
        const cashFlowChart = new ApexCharts(cashFlowChartEl, cashFlowOptions);
        cashFlowChart.render();
    }

    // B. Profit & Loss Chart
    const profitLossOptions = {
        series: [
            { name: 'Income', data: [0, 0, 0, 0] },
            { name: 'Expense', data: [0, 0, 0, 0] }
        ],
        chart: {
            type: 'bar',
            height: 250,
            toolbar: { show: false },
            fontFamily: 'Inter, sans-serif'
        },
        colors: [greenColor, redColor],
        plotOptions: {
            bar: { horizontal: false, columnWidth: '45%', borderRadius: 3 }
        },
        xaxis: {
            categories: ['Jan 2026', 'Apr 2026', 'Jul 2026', 'Oct 2026']
        },
        yaxis: {
            labels: {
                formatter: function (value) { return "₹" + value.toFixed(2); }
            }
        },
        legend: { position: 'top', horizontalAlign: 'left' }
    };
    const profitLossChartEl = document.querySelector("#profit-loss-chart");
    if (profitLossChartEl) {
        const profitLossChart = new ApexCharts(profitLossChartEl, profitLossOptions);
        profitLossChart.render();
    }

    // C. Expenses By Category Chart (Donut)
    const expensesCategoryOptions = {
        series: [0],
        labels: ['Other'],
        chart: {
            type: 'donut',
            height: 250,
            fontFamily: 'Inter, sans-serif'
        },
        colors: [grayColor],
        legend: { position: 'right' },
        responsive: [{
            breakpoint: 480,
            options: {
                legend: { position: 'bottom' }
            }
        }]
    };
    const expensesCategoryChartEl = document.querySelector("#expenses-category-chart");
    if (expensesCategoryChartEl) {
        const expensesCategoryChart = new ApexCharts(expensesCategoryChartEl, expensesCategoryOptions);
        expensesCategoryChart.render();
    }
});
