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
	BRA: {fillKey: 'gt50' },
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

	
//Google analytics
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-31234791-1']);
_gaq.push(['_trackPageview']);
 (function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();


