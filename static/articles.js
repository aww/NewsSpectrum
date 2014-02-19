$(document).ready(function(){

    var margin = {top: 20, right: 20, bottom: 40, left: 20},
    width = 960 - margin.left - margin.right,
    height = 120 - margin.top - margin.bottom;

    var svg = d3.select("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
    var plotarea = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    plotarea.append("image")
	.attr("xlink:href", "static/myspectrum.png")
	.attr("x", 0)
	.attr("y", 0)
	.attr("preserveAspectRatio", "none")
	.attr("width", width)
	.attr("height", height);

    var x = d3.scale.linear()
	.range([0, width])
	.domain([4, 24]);
    
    var xAxis = d3.svg.axis()
	.scale(x)
	.orient("top")
	.ticks(10);
    
    plotarea.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0,0)")
	.call(xAxis)
    //.append("text")
    //  .attr("x", 450)
    //  .attr("y", -30)
    //  .attr("dy", ".71em")
    //  .style("text-anchor", "end")
    //  .text("Flesch-Kincaid grade level");

    var labels = plotarea.append("g")
	.attr("transform", "translate(0," + height + ")")
    labels.append("text")
	.attr("x", x(4.2))
	.attr("dy", "-.2em")
        .attr("text-anchor", "start")
	.attr("fill", "white")
	.text("\u2190 lower reading level")
    labels.append("text")
	.attr("x", x(23.8))
	.attr("dy", "-.2em")
        .attr("text-anchor", "end")
	.attr("fill", "white")
	.text("higher reading level \u2192")


    var legend = svg.append("g")
        .attr("transform", "translate(0," + (height + margin.top) + ")")

    var leg_size = legend.append("g")
	.attr("transform", "translate(40,25)")
    leg_size.append("svg:circle")
	.attr("class", "example-spectrum-marker")
	.attr("cx", 0)
	.attr("r", 6);
    leg_size.append("svg:circle")
	.attr("class", "example-spectrum-marker")
	.attr("cx", 25)
	.attr("r", 12);
    leg_size.append("svg:text")
	.text("article length")
	.attr("alignment-baseline", "middle")
	.attr("x", 45);

    var leg_cur = legend.append("g")
	.attr("transform", "translate(" + (width - 100) + ",25)");
    leg_cur.append("svg:polygon")
	.attr("class", "example-spectrum-marker-current")
	.attr("points", "0.0000,-1.0000  0.3143,-0.4326  0.9511,-0.3090  0.5086,0.1652  0.5878,0.8090  0.0000,0.5348  -0.5878,0.8090  -0.5086,0.1652  -0.9511,-0.3090  -0.3143,-0.4326")
	.attr("transform", "scale(12)");
    leg_cur.append("svg:text")
	.text("current article")
	.attr("alignment-baseline", "middle")
	.attr("x", 25);

    var tooltip_width = 400;
    var tooltip = legend.append("g")
	.attr("class", "tooltip-group")
	.attr("visibility", "hidden")
	.attr("transform", "translate(" + ((width + margin.left + margin.right)/2) + ",25)");
    tooltip.append("svg:box")
	.attr("x", -tooltip_width/2)
	.attr("y", 0)
	.attr("width", tooltip_width)
	.attr("height", margin.bottom - 4);
    tooltip.append("svg:text")
	.attr("stroke", "red")
	.attr("alignment-baseline", "middle")
	.attr("text-anchor", "middle");
 
    d3.json(json_url, function(error, data) {
	//x.domain([d3.max(data.articles, function(d) { return d.grade_level; }),
	//          d3.min(data.articles, function(d) { return d.grade_level; })]);
	//x.domain([24, 0])
	
	plotarea.append("line")
	    .attr("x1", x(data.current_grade_level))
	    .attr("x2", x(data.current_grade_level))
	    .attr("y1", 0)
	    .attr("y2", height)
	    .attr("stroke", "black")
	    .attr("stroke-width", 2)
	var mgroups = plotarea.selectAll(".marker-group")
	    .data(data.articles)
	    .enter()
	    .append("svg:g")
	    .attr("class", "marker-group")
	    .attr("transform", function(datum) { return "translate(" + x(datum.grade_level) + "," + (height/2) + "), scale(" + Math.sqrt(datum.body.length/25) + ")"; })
	    .attr("svg:title", function(datum) { return datum.domain; })
	    .each(function(datum) {
		d3.select(this).on("click", function() {
		    $(  "#ifm").attr("src", datum.url);
		    $(".spectrum-marker-current")                     .attr("visibility", "hidden");
		    $(".spectrum-marker")                             .attr("visibility", "visible");
		    d3.select(this).select(".spectrum-marker-current").attr("visibility", "visible");
		    d3.select(this).select(".spectrum-marker")        .attr("visibility", "hidden");
		})
		d3.select(this).on("mouseover", function() {
		    d3.select(this).on("mouseover", function() {
			var ttgrp = d3.select(".tooltip-group");
			ttgrp.attr("visibility", "visible");
			ttgrp.select("text").text(datum.domain)
		    });
		    d3.select(this).on("mouseout", function() {
			d3.select(".tooltip-group").attr("visibility", "hidden");			
		    });
		});
	    });
	mgroups.append("svg:circle")
	    .attr("class", "spectrum-marker")
	    .attr("cx", 0)
	    .attr("cy", 0)
	    .attr("r", 1);
	mgroups.append("svg:polygon")
	    .attr("class", "spectrum-marker-current")
	    .attr("visibility", "hidden")
	    .attr("points", "0.0000,-1.0000  0.3143,-0.4326  0.9511,-0.3090  0.5086,0.1652  0.5878,0.8090  0.0000,0.5348  -0.5878,0.8090  -0.5086,0.1652  -0.9511,-0.3090  -0.3143,-0.4326")
	    .attr("transform", "scale(1.4)");
	var current = mgroups.filter(function(datum) { return datum.url == data.current_url; });
	current.select(".spectrum-marker-current").attr("visibility", "visible");
	current.select(".spectrum-marker")        .attr("visibility", "hidden");
    });


    // The following is from http://stackoverflow.com/questions/325273/make-iframe-to-fit-100-of-containers-remaining-height
    var buffer = 20; //scroll bar buffer
    var iframe = document.getElementById('ifm');
    
    function pageY(elem) {
	return elem.offsetParent ? (elem.offsetTop + pageY(elem.offsetParent)) : elem.offsetTop;
    }
    
    function resizeIframe() {
	var height = document.documentElement.clientHeight;
	height -= pageY(document.getElementById('ifm'))+ buffer ;
	height = (height < 0) ? 0 : height;
	document.getElementById('ifm').style.height = height + 'px';
    }
    
    // .onload doesn't work with IE8 and older.
    if (iframe.attachEvent) {
	iframe.attachEvent("onload", resizeIframe);
    } else {
	iframe.onload=resizeIframe;
    }

    window.onresize = resizeIframe;

});
