$(document).ready(function() {
	var ctx = $("#bar")[0].getContext("2d");
	var options = {
		/*scaleOverride: true,
		scaleStartValue: 0,*/
		scaleStartValue: 0,
		scaleShowGridLines: false,
		scaleShowLabels: false,
		title: "Percentile",
	};
	var data = {
    	labels: ["0s", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s"],
    	datasets: [
	        {
	            fillColor: "rgba(146,69,171,0.5)",
	            strokeColor: "rgba(146,69,171,0.8)",
	            highlightFill: "rgba(146,69,171,0.75)",
	            highlightStroke: "rgba(146,69,171,1)",
	            data: [0, 5, 10, 15, 25, 25, 5, 5, 5, 5],
	        },
    	],
	};
	var percentileChart = new Chart(ctx).Bar(data, options);
});