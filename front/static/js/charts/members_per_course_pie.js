var pie_conf = {
    radius: 120,
    left: 10,
    right: 200,
    top: 0,
    bottom: 0
}

var lgnd_conf = {
    left: 10,
    top: 40
}

var width = pie_conf.radius * 2 + pie_conf.left + pie_conf.right;
var height = pie_conf.radius * 2 + pie_conf.top + pie_conf.bottom;

var color = d3.scale.ordinal()
    .range(["#2f69bf", "#a2bf2f", "#bf5a2f", "#bfa22f", "#772fbf", "#bf2f2f", "#00327f", "#667f00"]);

var arc = d3.svg.arc()
    .outerRadius(pie_conf.radius - 10)
    .innerRadius(0);

var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) { return d.mcount; });

var svg = d3.select("#members_per_course").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + (pie_conf.left + pie_conf.radius) + "," + (pie_conf.top + pie_conf.radius) + ")");


/*** Prepare data ***/

d3.json("/charts/members_per_course/").header("X-Requested-With", "XMLHttpRequest").get(function(error, data) {

    data.forEach(function(d) {
        d.mcount = +d.mcount;
    });


    /*** Pie Chart ***/

    var g = svg.selectAll(".arc")
        .data(pie(data))
      .enter().append("g")
        .attr("class", "arc")
        .attr("data-course", function(d) { return d.data.course; })
        .on("mouseover", onmouseover)
        .on("mouseout", onmouseout);

    g.append("path")
        .attr("d", arc)
        .attr("data-legend", function(d) { return d.data.course_full + "(" + d.data.mcount + ")"; })
        .attr("data-legend-pos", function(d, i) { return i; })
        .style("stroke", "#ffffff")
        .style("stroke-width", "1px")
        .style("fill", function(d, i) { return color(i); })

    function onmouseover(d, i) {
        var offset = arc_offset(d, 10);
        d3.select(this)
          .transition()
            .duration(200)
            .attr("transform", "translate(" + offset.x + "," + (-offset.y) + ")");
        svg.select('g.legend').selectAll('text').filter(function(dd, ii) { return ii == i; })
          .transition()
            .duration(2000)
            .style("font-weight", "bold");
    }

    function onmouseout(d, i) {
        d3.select(this)
          .transition()
            .duration(200)
            .attr("transform", "translate(0,0)");
        svg.select('g.legend').selectAll('text').filter(function(dd, ii) { return ii == i; })
          .transition()
            .duration(200)
            .style("font-weight", "normal");
    }


    /*** Legend ***/

    var legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", "translate(" + (pie_conf.radius + lgnd_conf.left) + "," + (lgnd_conf.top - pie_conf.radius) + ")")
        .style("fill", "#ffffff")
        .style("font-size", "12px")
        .call(d3.legend)
      .selectAll("text")
        .attr("data-course", function(d) { return d.course; })
        .style("fill", "#000000");

});


/*** Helper functions ***/

// Convert d3 angles to polar angles
function angle_conv(angle) {
    return (2.5 * Math.PI - angle) % (2 * Math.PI);
}

// Calculate arc offset in cartesian coordinate system
function arc_offset(d, distance) {
    var angle = d.startAngle + (d.endAngle - d.startAngle) / 2;
    return {x: distance * Math.cos(angle_conv(angle)), y: distance * Math.sin(angle_conv(angle))}
}
