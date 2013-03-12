(function() {

    var container_id = "cakes_per_member";

    var margin = {top: 0, right: 10, bottom: 20, left: 120},
        width = 640 - margin.left - margin.right,
        bar_height = 12, bar_margin = 3, bar_width = 100;

    var format_count = d3.format(".0%");

    d3.json("/charts/cakes_per_member/").header("X-Requested-With", "XMLHttpRequest").get(function(error, data) {

        var svg = d3.select("#" + container_id).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", data.length * (bar_height + 2 * bar_margin) + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var x = d3.scale.linear()
            .range([0, 6 * bar_width])
            .domain([0, 6]);

        var y = d3.scale.linear()
            .range([
                bar_height + 2 * bar_margin + 5,
                (data.length + 1) * (bar_height + 2 * bar_margin) + 5
            ])
            .domain([0, data.length]);

        data.forEach(function(d) {
            d.past = +d.past;
            d.future = +d.future;
        });

        svg.selectAll(".bar.past")
            .data(data)
          .enter().append("rect")
            .attr("class", "bar past")
            .style("fill", "#2F69BF")
            .attr("x", 0)
            .attr("width", function(d) { return x(d.past); })
            .attr("y", function(d, i) { return y(i); })
            .attr("height", bar_height);

        svg.selectAll(".bar.future")
            .data(data)
          .enter().append("rect")
            .attr("class", "bar future")
            .style("fill", "#A2BF2F")
            .attr("x", function(d) { return x(d.past); })
            .attr("width", function(d) { return x(d.future); })
            .attr("y", function(d, i) { return y(i); })
            .attr("height", bar_height);

        svg.selectAll(".x.axis text")
            .style("text-anchor", "end")
            .style("font-size", "0.8em")
            .attr("transform", "translate(-18, 10) rotate(-70)");

        svg.append("text")
            .attr("class", "headline col-name")
            .style("font-weight", "bold")
            .attr("x", -margin.left)
            .attr("y", 8)
            .style("font-size", "10px")
            .text("Name");
        svg.append("text")
            .attr("class", "headline col-ccount")
            .style("font-weight", "bold")
            .attr("x", 0)
            .attr("y", 8)
            .style("font-size", "10px")
            .text("Kuchen gebracht/geplant seit Semesterbeginn");

        svg.selectAll("text.name")
            .data(data)
          .enter().append("text")
            .attr("class", "name")
            .attr("x", -margin.left)
            .attr("y", function(d, i) { return y(i) + 8; })
            .style("font-size", "10px")
            .text(function(d) { return d.first_name + " " + d.last_name; });

        svg.selectAll("text.count")
            .data(data)
          .enter().append("text")
            .attr("class", "count")
            .attr("x", function(d) { return x(d.past + d.future) + ((d.past + d.future) ? 5 : 0); })
            .attr("y", function(d, i) { return y(i) + 8; })
            .style("font-size", "10px")
            .text(function(d) { return d.past + "/" + d.future; });
    });
}());
