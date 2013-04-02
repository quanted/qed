Raphael.fn.connection = function (obj1, obj2, line, bg) {
    if (obj1.line && obj1.from && obj1.to) {
        line = obj1;
        obj1 = line.from;
        obj2 = line.to;
    }
    var bb1 = obj1.getBBox(),
        bb2 = obj2.getBBox(),
        p = [{x: bb1.x + bb1.width / 2, y: bb1.y - 1},
        {x: bb1.x + bb1.width / 2, y: bb1.y + bb1.height + 1},
        {x: bb1.x - 1, y: bb1.y + bb1.height / 2},
        {x: bb1.x + bb1.width + 1, y: bb1.y + bb1.height / 2},
        {x: bb2.x + bb2.width / 2, y: bb2.y - 1},
        {x: bb2.x + bb2.width / 2, y: bb2.y + bb2.height + 1},
        {x: bb2.x - 1, y: bb2.y + bb2.height / 2},
        {x: bb2.x + bb2.width + 1, y: bb2.y + bb2.height / 2}],
        d = {}, dis = [];
    for (var i = 0; i < 4; i++) {
        for (var j = 4; j < 8; j++) {
            var dx = Math.abs(p[i].x - p[j].x),
                dy = Math.abs(p[i].y - p[j].y);
            if ((i == j - 4) || (((i != 3 && j != 6) || p[i].x < p[j].x) && ((i != 2 && j != 7) || p[i].x > p[j].x) && ((i != 0 && j != 5) || p[i].y > p[j].y) && ((i != 1 && j != 4) || p[i].y < p[j].y))) {
                dis.push(dx + dy);
                d[dis[dis.length - 1]] = [i, j];
            }
        }
    }
    if (dis.length == 0) {
        var res = [0, 4];
    } else {
        res = d[Math.min.apply(Math, dis)];
    }
    var x1 = p[res[0]].x,
        y1 = p[res[0]].y,
        x4 = p[res[1]].x,
        y4 = p[res[1]].y;
    dx = Math.max(Math.abs(x1 - x4) / 2, 10);
    dy = Math.max(Math.abs(y1 - y4) / 2, 10);
    var x2 = [x1, x1, x1 - dx, x1 + dx][res[0]].toFixed(3),
        y2 = [y1 - dy, y1 + dy, y1, y1][res[0]].toFixed(3),
        x3 = [0, 0, 0, 0, x4, x4, x4 - dx, x4 + dx][res[1]].toFixed(3),
        y3 = [0, 0, 0, 0, y1 + dy, y1 - dy, y4, y4][res[1]].toFixed(3);
    var path = ["M", x1.toFixed(3), y1.toFixed(3), "C", x2, y2, x3, y3, x4.toFixed(3), y4.toFixed(3)].join(",");
    if (line && line.line) {
        line.bg && line.bg.attr({path: path});
        line.line.attr({path: path});
    } else {
        var color = typeof line == "string" ? line : "#000";
        return {
            bg: bg && bg.split && this.path(path).attr({stroke: bg.split("|")[0], fill: "none", "stroke-width": bg.split("|")[1] || 3}),
            line: this.path(path).attr({stroke: color, fill: "none"}),
            from: obj1,
            to: obj2
        };
    }
};

var el;
window.onload = function () {
	var graph_width = 160;
	var graph_height = 400;
	var node_radius = 20;
	var node_horizontal_space = 10;
	var node_vertical_space = Math.round((graph_height - 6 * node_radius)/6);
	var shapes = [];
	var connections = [];
	var shape_index_map = {};
	var shape_shape_map = {};
	r = Raphael("right", graph_width, graph_height);
	$.ajax({
		url:"/ubertool-stats",
		async: false,
		dataType: "json",
		type: 'GET',
		success: function(ubertool_stats) {
			var shape_index = 0;
			var use_stats = ubertool_stats['use'];
			var total_use_stats_nodes = use_stats['total-nodes'];
			var total_use_stats_links = use_stats['total-links'];
			var current_y = (node_radius*2);
			var current_x = node_radius + node_horizontal_space/2;
			var current_x_space = ((graph_width - total_use_stats_nodes * node_radius*2) / (total_use_stats_nodes + 1));
			for(var use_stat in use_stats)
			{
				if(use_stat != 'total-nodes' && use_stat != 'total-links')
				{
					var current_use_config = use_stats[use_stat];
					current_node = r.ellipse(current_x,current_y,(node_radius/2),(node_radius/2));
					shape_index_map[use_stat] = shape_index;
					shape_shape_map[use_stat] = {}
					for(var pest_config in current_use_config)
					{
						var num_links = current_use_config[pest_config];
						shape_shape_map[use_stat][pest_config] = num_links;
					}
					shapes.push(current_node);
					shape_index += 1;
					current_x += current_x_space + 2 * node_radius + node_horizontal_space;
					if(current_x > graph_width - node_radius)
					{
						current_x = graph_width - node_radius;
					}
				}
			}
			var pest_stats = ubertool_stats['pest'];
			var total_pest_stats_nodes = pest_stats['total-nodes'];
			var total_pest_stats_links = pest_stats['total-links'];
			var current_y = current_y + node_vertical_space + node_radius;
			var current_x = node_radius + node_horizontal_space/2;
			var current_x_space = (graph_width - total_pest_stats_nodes * node_radius*2) / (total_pest_stats_nodes + 1);
			for(var pest_stat in pest_stats)
			{
				if(pest_stat != 'total-nodes' && pest_stat != 'total-links')
				{
					var current_pest_config = pest_stats[pest_stat];
					current_node = r.ellipse(current_x,current_y,(node_radius/2),(node_radius/2));
					shape_index_map[pest_stat] = shape_index;
					shape_shape_map[pest_stat] = {};
					for(var pest_config in current_pest_config)
					{
						var num_links = current_pest_config[pest_config];
						shape_shape_map[pest_stat][pest_config] = num_links;
					}
					shapes.push(current_node);
					shape_index += 1;
					current_x += current_x_space + 2 * node_radius + node_horizontal_space;
					if(current_x > graph_width - node_radius)
					{
						current_x = graph_width - node_radius;
					}
				}
			}
			var expo_stats = ubertool_stats['expo'];
			var total_expo_stats_nodes = expo_stats['total-nodes'];
			var total_expo_stats_links = expo_stats['total-links'];
			var current_y = current_y + node_vertical_space + node_radius;
			var current_x = node_radius + node_horizontal_space/2;
			var current_x_space = (graph_width - total_expo_stats_nodes * node_radius) / (total_expo_stats_nodes + 1);
			for(var expo_stat in expo_stats)
			{
				if(expo_stat != 'total-nodes' && expo_stat != 'total-links')
				{
					var current_expo_config = expo_stats[expo_stat];
					current_node = r.ellipse(current_x,current_y,(node_radius/2),(node_radius/2));
					shape_index_map[expo_stat] = shape_index;
					shape_shape_map[expo_stat] = {};
					for(var expo_config in current_expo_config)
					{
						var num_links = current_expo_config[expo_config];
						shape_shape_map[expo_stat][expo_config] = num_links;
					}
					shapes.push(current_node);
					shape_index += 1;
					current_x += current_x_space + 2 * node_radius + node_horizontal_space;
					if(current_x > graph_width - node_radius)
					{
						current_x = graph_width - node_radius;
					}
				}
			}
			var aquatic_stats = ubertool_stats['aquatic'];
			var total_aquatic_stats_nodes = aquatic_stats['total-nodes'];
			var total_aquatic_stats_links = aquatic_stats['total-links'];
			var current_y = current_y + node_vertical_space + node_radius;
			var current_x = node_radius + node_horizontal_space/2;
			var current_x_space = (graph_width - total_aquatic_stats_nodes * node_radius) / (total_aquatic_stats_nodes + 1);
			for(var aquatic_stat in aquatic_stats)
			{
				if(aquatic_stat != 'total-nodes' && aquatic_stat != 'total-links')
				{
					var current_aqua_config = aquatic_stats[aquatic_stat];
					current_node = r.ellipse(current_x,current_y,(node_radius/2),(node_radius/2));
					shape_index_map[aquatic_stat] = shape_index;
					shape_shape_map[aquatic_stat] = {};
					for(var aqua_config in current_aqua_config)
					{
						var num_links = current_aqua_config[aqua_config];
						shape_shape_map[aquatic_stat][aqua_config] = num_links;
					}
					shapes.push(current_node);
					shape_index += 1;
					current_x += current_x_space + 2 * node_radius + node_horizontal_space;
					if(current_x > graph_width - node_radius)
					{
						current_x = graph_width - node_radius;
					}
				}
			}
			var terre_stats = ubertool_stats['terre'];
			var total_terre_stats_nodes = terre_stats['total-nodes'];
			var total_terre_stats_links = terre_stats['total-links'];
			var current_y = current_y + node_vertical_space + node_radius;
			var current_x = node_radius + node_horizontal_space/2;
			var current_x_space = (graph_width - total_terre_stats_nodes * node_radius) / (total_terre_stats_nodes + 1);
			for(var terre_stat in terre_stats)
			{
				if(terre_stat != 'total-nodes' && terre_stat != 'total-links')
				{
					var current_terre_config = terre_stats[terre_stat];
					current_node = r.ellipse(current_x,current_y,(node_radius/2),(node_radius/2));
					shape_index_map[terre_stat] = shape_index;
					shape_shape_map[terre_stat] = {};
					for(var terre_config in current_terre_config)
					{
						var num_links = current_terre_config[terre_config];
						shape_shape_map[terre_stat][terre_config] = num_links;
					}
					shapes.push(current_node);
					shape_index += 1;
					current_x += current_x_space + 2 * node_radius + node_horizontal_space;
					if(current_x > graph_width - node_radius)
					{
						current_x = graph_width - node_radius;
					}
				}
			}
			var eco_stats = ubertool_stats['eco'];
			var total_eco_stats_nodes = eco_stats['total-nodes'];
			var total_eco_stats_links = eco_stats['total-links'];
			var current_y = current_y + node_vertical_space + node_radius;
			var current_x = node_radius + node_horizontal_space/2;
			var current_x_space = (graph_width - total_eco_stats_nodes * node_radius) / (total_eco_stats_nodes + 1);
			for(var eco_stat in eco_stats)
			{
				if(eco_stat != 'total-nodes' && eco_stat != 'total-links')
				{
					var current_eco_config = eco_stats[eco_stat];
					current_node = r.ellipse(current_x,current_y,(node_radius/2),(node_radius/2));
					shape_index_map[eco_stat] = shape_index;
					shape_shape_map[eco_stat] = {};
					for(var eco_config in current_eco_config)
					{
						var num_links = current_eco_config[eco_config];
						shape_shape_map[eco_stat][eco_config] = num_links;
					}
					shapes.push(current_node);
					shape_index += 1;
					current_x += current_x_space + 2 * node_radius + node_horizontal_space;
					if(current_x > graph_width - node_radius)
					{
						current_x = graph_width - node_radius;
					}
				}
			}
		}
	});
    var dragger = function () {
        this.ox = this.type == "rect" ? this.attr("x") : this.attr("cx");
        this.oy = this.type == "rect" ? this.attr("y") : this.attr("cy");
        this.animate({"fill-opacity": .2}, 160);
    },
    move = function (dx, dy) {
        var att = this.type == "rect" ? {x: this.ox + dx, y: this.oy + dy} : {cx: this.ox + dx, cy: this.oy + dy};
        this.attr(att);
        for (var i = connections.length; i--;) {
            r.connection(connections[i]);
        }
        r.safari();
    },
    up = function () {
        this.animate({"fill-opacity": 0}, 160);
    };
	for (var i = 0, ii = shapes.length; i < ii; i++) {
        var color = Raphael.getColor();
        shapes[i].attr({fill: color, stroke: color, "fill-opacity": 100, "stroke-width": 2, cursor: "move"});
        shapes[i].drag(move, dragger, up);
    }
	for(var from_shape_instance in shape_shape_map)
	{
		var from_shape_index = shape_index_map[from_shape_instance];
		var shape_map = shape_shape_map[from_shape_instance];
		var from_shape_array = [];
		for(var to_shape_instance in shape_map)
		{
			var to_shape_index = shape_index_map[to_shape_instance];
			var num_from_to_shape_links = shape_map[to_shape_instance];
			connections.push(r.connection(shapes[from_shape_index],shapes[to_shape_index],"#000"));
		}
	}
    /**
    r = Raphael("right", graph_width, graph_height),
    connections = temp_connections,
    shapes = temp_shapes;
    **/

    //connections.push(r.connection(shapes[0], shapes[1], "#fff"));
    //connections.push(r.connection(shapes[1], shapes[2], "#fff", "#fff|5"));
    //connections.push(r.connection(shapes[1], shapes[3], "#000", "#fff"));
};

