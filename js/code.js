 //Map code (adapted from examples at http://datamaps.github.io/)
      var map = new Datamap({
        scope: 'world',
        element: document.getElementById('container1'),
        projection: 'equirectangular',

        fills: {
          defaultFill: '#b1b1b1',
          gt50: '#06D4EC'
        },
        
        data: {

  DZA: {fillKey: 'gt50' },
  BEL: {fillKey: 'gt50' },
  LKA: {fillKey: 'gt50' },
  IND: {fillKey: 'gt50' },
  IRL: {fillKey: 'gt50' },
  LUX: {fillKey: 'gt50' },
  NLD: {fillKey: 'gt50' },
  MDV: {fillKey: 'gt50' },
	BRA: {fillKey: 'gt50' },
  POL: {fillKey: 'gt50' },
  GBR: {fillKey: 'gt50' },
  IMN: {fillKey: 'gt50' },
  SGP: {fillKey: 'gt50' },
	TUN: {fillKey: 'gt50' },
	MAR: {fillKey: 'gt50' },
	EGY: {fillKey: 'gt50' },
	FRA: {fillKey: 'gt50' },
	ITA: {fillKey: 'gt50' },
	GRC: {fillKey: 'gt50' },
	ESP: {fillKey: 'gt50' },
	SWE: {fillKey: 'gt50' },
	ARE: {fillKey: 'gt50' },
	USA: {fillKey: 'gt50' },
	CHE: {fillKey: 'gt50' },
	CZE: {fillKey: 'gt50' },
	DEU: {fillKey: 'gt50' },
	
       }
      }) 

//Reload button for the languages sections
function myfunction(){
	document.getElementById('fra').contentWindow.location.reload(true);
	}



$(document).ready(function () {
    $("#about").fadeIn(500);
    $("#cv").fadeIn(1000);
    $("#publi").fadeIn(1500);
    $("#contact").fadeIn(2000);
    $("#web").fadeIn(2500);
    $("#en").fadeIn(3000);
    $("#fr").fadeIn(3500);
    $("#ar").fadeIn(4000);
    $("#it").fadeIn(4500);

});


// language
var width = 200,
    height = 150,
    twoPi = 2 * Math.PI,
    progress = 0,
    progress2 = 0,
    progress3 = 0,
    total = 990, 
    score = 970,
    duration = 3000,
    formatPercent = d3.format(".0%");

var arc = d3.svg.arc()
    .startAngle(0)
    .innerRadius(45)
    .outerRadius(60);

var svg = d3.select("#l1").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var meter = svg.append("g")
    .attr("class", "progress-meter");

meter.append("path")
    .attr("class", "background")
    .attr("d", arc.endAngle(twoPi));

var foreground = meter.append("path")
    .attr("class", "foreground");

var text = meter.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em");

var i = d3.interpolate(0, score / total);
d3.transition().duration(duration).tween("progress", function() {
        return function(t) {
          progress = i(t);
          foreground.attr("d", arc.endAngle(twoPi * progress));
          text.text(~~(progress*total)+"/" +total);
        };
      });

      
      
      
var arc2 = d3.svg.arc()
    .startAngle(0)
    .innerRadius(45)
    .outerRadius(60);
      
var svg2 = d3.select("#l2").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
var meter2 = svg2.append("g")
    .attr("class", "progress-meter");
    
meter2.append("path")
    .attr("class", "background")
    .attr("d", arc2.endAngle(twoPi));    

var foreground2 = meter2.append("path")
    .attr("class", "foreground");

var text2 = meter2.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em").text("N/A");

var i2 = d3.interpolate(0, 1);

d3.transition().duration(duration/2).delay(duration+1).tween("progress2", function() {
        return function(t) {
          progress2 = i2(t);
          foreground2.attr("d", arc2.endAngle(twoPi * progress2));
        };
      });
      
            
var arc3 = d3.svg.arc()
    .startAngle(0)
    .innerRadius(45)
    .outerRadius(60);
      
var svg3 = d3.select("#l3").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
var meter3 = svg3.append("g")
    .attr("class", "progress-meter");
    
meter3.append("path")
    .attr("class", "background")
    .attr("d", arc3.endAngle(twoPi));    

var foreground3 = meter3.append("path")
    .attr("class", "foreground");

var text3 = meter3.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em").text("N/A");


d3.transition().duration(duration/2).delay(duration*1.5+1).tween("progress3", function() {
        return function(t) {
          progress3 = i2(t);
          foreground3.attr("d", arc3.endAngle(twoPi * progress3));
        };
      });


var arc4 = d3.svg.arc()
    .startAngle(0)
    .innerRadius(45)
    .outerRadius(60);
      
var svg4 = d3.select("#l4").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    
var meter4 = svg4.append("g")
    .attr("class", "progress-meter");
    
meter4.append("path")
    .attr("class", "background")
    .attr("d", arc4.endAngle(twoPi));    

var foreground4 = meter4.append("path")
    .attr("class", "foreground");

var text4 = meter4.append("text")
    .attr("text-anchor", "middle")
    .attr("dy", "0.35em").text("Ma ??");

var i3 = d3.interpolate(0, 0.2);
d3.transition().duration(duration/2).delay(duration*2+1).tween("progress4", function() {
        return function(t) {
          progress4 = i3(t);
          foreground4.attr("d", arc3.endAngle(twoPi * progress4));
        };
      });
	
//Google analytics
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-31234791-1']);
_gaq.push(['_trackPageview']);
 (function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();


