// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
var ctx = document.getElementById("predictionPieChart");
var valueLabel = document.getElementById("valueLabel");

var data = {
  
  datasets: [{
    data: [55, 30],
    backgroundColor: ['#FFCCFF', '#17a673'],
    hoverBackgroundColor: ['#FFCCFF', '#17a673'],
    hoverBorderColor: "rgba(234, 236, 244, 1)",
  }],
};

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: data,
  options: {
    maintainAspectRatio: false,
    cutoutPercentage: 80,
    tooltips: {
      enabled: false
    }
  }
});

// Function to update the chart data and display the value inside the circle
function updateChartData(fraud, notFraud) {
  data.datasets[0].data = [fraud, notFraud];
  if(fraud<=30)
  {
    color1 = '#55FF33'
  }
  else if(fraud>30 && fraud<=50)
  {
    color1 = '#FFFF00'
  }
  else if(fraud>50 && fraud<80)
  {
    color1 = '#ff6347'
  }
  else
  {
    color1 = '#ff0800'
  }
  color2 = '#FFCCFF'
  data.datasets[0].backgroundColor=[color1,color2]
  data.datasets[0].hoverBackgroundColor=[color1,color2]
  myPieChart.update();
  
  // Display the value inside the circle
  valueLabel.textContent = (fraud  + "%")   ;
}

// Example usage: Update the chart with new data (e.g., fraud = 60, notFraud = 40)
let fraudScore = document.getElementById('fraudScore').textContent*100;
updateChartData(fraudScore, 100-fraudScore);
let curTransaction = document.getElementById('curTransaction').textContent;
curTransaction = curTransaction.split(' ');
console.log(curTransaction)
function addRow() {
    //var table = document.getElementById("myTable");
    var tbody = document.getElementById("dataToShow");

    // Create a new row
       var newRow = tbody.insertRow();
        for(var i = 0 ;i<6;i++)
        {
            var cell = newRow.insertCell(i);
            if(i!=0)
            cell.innerHTML = curTransaction[i];
           else
           cell.innerHTML = 0;
        }

    
   
    
}
addRow();

