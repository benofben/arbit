<!DOCTYPE html>
<html>
<meta charset="utf-8">

<!-- Example based on http://bl.ocks.org/mbostock/3887118 -->
<!-- Tooltip example from http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html -->

<style>
body {
  font: 11px sans-serif;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.dot {
  stroke: #000;
}

.tooltip {
  position: absolute;
  width: 200px;
  height: 28px;
  pointer-events: none;
}
</style>
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script>

var data =<?php $m = new MongoClient();
		$db = $m -> arbit;
		$collection = $db -> form4;
		$symbol = $_GET['symbol'];
		$query = array('IssuerTradingSymbol' => $symbol);
		$cursor = $collection -> find($query);
		$jsonEDGARData = iterator_to_array($cursor);
		echo json_encode(array_values($jsonEDGARData));
	?>;

function toDate(secs)
{
 var t = new Date(1970,0,1);
 t.setSeconds(secs);
 return t;
}

var margin = {top: 20, right: 20, bottom: 30, left: 100},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var dateInSecondsSinceEpoch = function(d) { return d.TransactionDate.sec;},
minDate = toDate(d3.min(data, dateInSecondsSinceEpoch)),
maxDate = toDate(d3.max(data, dateInSecondsSinceEpoch));

// setup x 
var xValue = function(d) { return toDate(d.TransactionDate.sec);},
xScale = d3.time.scale().domain([minDate, maxDate]).range([0, width]);
xMap = function(d) { return xScale(xValue(d));},
xAxis = d3.svg.axis().scale(xScale).orient("bottom");

// setup y
var yValue = function(d) { 
  if (d.TransactionAcquiredDisposed == 'A'){
  	var tradePrice = d.TransactionShares*d.TransactionPricePerShare;
	return tradePrice;
  }
  else if(d.TransactionAcquiredDisposed == 'D'){
  	var tradePrice = d.TransactionShares*d.TransactionPricePerShare*-1;
	return tradePrice;
  }
}, // data -> value
yScale = d3.scale.linear().range([height, 0]), // value -> display
yMap = function(d) { return yScale(yValue(d));}, // data -> display
yAxis = d3.svg.axis().scale(yScale).orient("left");

// setup fill color
var cValue = function(d) {
	  if (d.TransactionAcquiredDisposed == 'A'){
	return "Acquired";
  }
  else if(d.TransactionAcquiredDisposed == 'D'){
	return "Disposed";
  };
},
    color = d3.scale.category10();

// add the graph canvas to the body of the webpage
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  // don't want dots overlapping axis, so add in buffer to data domain
  yScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);

  // x-axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Transaction Date");

  // y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Transaction Price");

  // draw dots
  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", xMap)
      .attr("cy", yMap)
      .style("fill", function(d) { return color(cValue(d));}) 
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html(d.RptOwnerName + "<br/> " + xValue(d) 
          + "<br/> Transaction Price = $" + yValue(d).toFixed(2) 
          + "<br/> IsDirector = " + d.IsDirector 
          + "<br/> IsOfficer = " + d.IsOfficer 
          + "<br/> IsOther = " + d.IsOther 
          + "<br/> TransactionPricePerShare = $" + d.TransactionPricePerShare.toFixed(2))
               .style("left", (d3.event.pageX + 5) + "px")
               .style("top", (d3.event.pageY - 28) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      });

  // draw legend
  var legend = svg.selectAll(".legend")
      .data(color.domain())
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  // draw legend colored rectangles
  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

  // draw legend text
  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d;})

</script>
</body>
</html>

