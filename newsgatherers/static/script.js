let dataList = [];
for (let i = 0; i < 9; i++) {
  let randomNumber = Math.floor(Math.random() * (91) + 10);
  dataList.push(randomNumber);  
}

const A = [
  'Andhra Pradesh',
  'Arunachal Pradesh',
  'Assam',
  'Bihar',
  'Chhattisgarh',
  'Goa',
  'Gujarat',
  'Haryana',
  'Himachal Pradesh',
  'Jharkhand',
  'Karnataka',
  'Kerala',
  'Madhya Pradesh',
  'Maharashtra',
  'Manipur',
  'Meghalaya',
  'Mizoram',
  'Nagaland',
  'Odisha',
  'Punjab',
  'Rajasthan',
  'Sikkim',
  'Tamil Nadu',
  'Telangana',
  'Tripura',
  'Uttar Pradesh',
  'Uttarakhand',
  'West Bengal'
];
let stateList = [];
for (let i = 0; i < 9; i++) {
  let randomNumber = Math.floor(Math.random() * (29) + 1);
  const St = A[randomNumber];
  stateList.push(St)
}


var options = {
  chart: {
    type: 'bar'
  },
  series: [{
    name: 'sales',
    data: dataList
  }],
  xaxis: {
    categories: stateList
  }
}

let lineList = [];
for (let i = 0; i < 6; i++) {
  let randomNumber = Math.floor(Math.random() * (91) + 10);
  lineList.push(randomNumber);  
}
let lineList1 = [];
for (let i = 0; i < 6; i++) {
  let randomNumber = Math.floor(Math.random() * (91) + 10);
  lineList1.push(randomNumber);  
}
var options1 = {
  chart: {
    height: 350,
    type: "line",
    stacked: false
  },
  dataLabels: {
    enabled: false
  },
  colors: ["#FF1654", "#247BA0"],
  series: [
    {
      name: "Negative",
      data: lineList
    },
    {
      name: "Positive",
      data: lineList1
    }
  ],
  stroke: {
    width: [4, 4]
  },
  plotOptions: {
    bar: {
      columnWidth: "20%"
    }
  },
  xaxis: {
    categories: ['1hr','2hr','3hr','4hr','5hr','6hr']
  },
  yaxis: [
    {
      axisTicks: {
        show: true
      },
      axisBorder: {
        show: true,
        color: "#FF1654"
      },
      labels: {
        style: {
          colors: "#FF1654"
        }
      },
      title: {
        text: "Negative",
        style: {
          color: "#FF1654"
        }
      }
    },
    {
      opposite: true,
      axisTicks: {
        show: true
      },
      axisBorder: {
        show: true,
        color: "#247BA0"
      },
      labels: {
        style: {
          colors: "#247BA0"
        }
      },
      title: {
        text: "Positive",
        style: {
          color: "#247BA0"
        }
      }
    }
  ],
  tooltip: {
    shared: false,
    intersect: true,
    x: {
      show: false
    }
  },
  legend: {
    horizontalAlign: "left",
    offsetX: 40
  }
  
};
let pieList = [];
for (let i = 0; i < 3; i++) {
  let randomNumber = Math.floor(Math.random() * (91) + 10);
  pieList.push(randomNumber);  
}

var options2 = {
  chart: {
    type: 'donut'
  },
  series: pieList,
  labels: ['Neutral','Positive','Negative']
};


window.onload = () =>{
var bar = new ApexCharts(document.querySelector("#chart"), options);
bar.render();
var line = new ApexCharts(document.querySelector("#line"), options1);
line.render();
var pie = new ApexCharts(document.querySelector("#pie"), options2);
pie.render();
}