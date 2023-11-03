// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
// // Initialize the pie chart with initial data
var ctx = document.getElementById("myPieChart");
var data = {
  labels: ["Fraud", "Not Fraud"],
  datasets: [{
    data: [55, 30, 15],
    backgroundColor: ['#ff0038','#17a673', '#36b9cc'],
    hoverBackgroundColor: ['#ff0000', '#17a673', '#2c9faf'],
    hoverBorderColor: "rgba(234, 236, 244, 1)",
  }],
};

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: data,
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

// Function to update the chart data
function updateChartData(fraud, notFraud) {
  data.datasets[0].data = [fraud, notFraud];
  myPieChart.update();
}

// Example usage: Update the chart with new data (e.g., fraud = 60, notFraud = 40)
let fraudCount = document.getElementById('fraudCount').textContent*100
let nonFraudCount = document.getElementById('nonFraudCount').textContent*100

updateChartData(fraudCount, nonFraudCount);
