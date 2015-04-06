         var pc0;

        var blue_to_brown = d3.scale.linear()
          .domain([0, 5])
          .range(["red", "#3498db"])
          .interpolate(d3.interpolateLab);


        d3.csv('../static/csv/data.csv?_=' + Math.random(), function(data) {
        pc0 = d3.parcoords()("#example0")
          .data(data)
            .showControlPoints(false)
            .hideAxis(["Title"])
            .hideAxis(["ID"])
            .composite("darker")
            .width(860)
            .color(function(d) { return blue_to_brown(d['Depth']);})
            .render()
            .alpha(0.35)
            .brushMode("1D-axes")
            .reorderable()
            .interactive();
        });

        $(function () {
          $('[data-toggle="tooltip"]').tooltip()
        });
