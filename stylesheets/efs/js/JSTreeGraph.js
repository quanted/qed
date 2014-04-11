function DrawTree(options) {

    // Prepare Nodes
    PrepareNode(options.RootNode);

    // Calculate Boxes Positions
    if (options.Layout == "Vertical") {
        PerformLayoutV(options.RootNode);
    } else {
        PerformLayoutH(options.RootNode);
    }

    // Draw Boxes
    options.Container.innerHTML = "";
    DrawNode(options.RootNode, options.Container, options);

    // Draw Lines
    DrawLines(options.RootNode, options.Container);
}

function DrawLines(node, container) {
    if ((!node.Collapsed) && node.Nodes && node.Nodes.length > 0) { // Has children and Is Expanded
        for (var j = 0; j < node.Nodes.length; j++) {
            if(node.ChildrenConnectorPoint.Layout=="Vertical")
                DrawLineV(container, node.ChildrenConnectorPoint, node.Nodes[j].ParentConnectorPoint);
            else
                DrawLineH(container, node.ChildrenConnectorPoint, node.Nodes[j].ParentConnectorPoint);

            // Children
            DrawLines(node.Nodes[j], container);
        }
    }
}

function DrawLineH(container, startPoint, endPoint) {
        var midY = (startPoint.Y + ((endPoint.Y - startPoint.Y) / 2)); // Half path between start en end Y point

        // Start segment
        DrawLineSegment(container, startPoint.X, startPoint.Y, startPoint.X, midY, 1);

        // Intermidiate segment
        var imsStartX = startPoint.X < endPoint.X ? startPoint.X : endPoint.X; // The lower value will be the starting point
        var imsEndX = startPoint.X > endPoint.X ? startPoint.X : endPoint.X; // The higher value will be the ending point
        DrawLineSegment(container, imsStartX, midY, imsEndX, midY, 1);

        // End segment
        DrawLineSegment(container, endPoint.X, midY, endPoint.X, endPoint.Y, 1);
}

function DrawLineV(container, startPoint, endPoint) {
    var midX = (startPoint.X + ((endPoint.X - startPoint.X) / 2)); // Half path between start en end X point

    // Start segment
    DrawLineSegment(container, startPoint.X, startPoint.Y, midX, startPoint.Y, 1);

    // Intermidiate segment
    var imsStartY = startPoint.Y < endPoint.Y ? startPoint.Y : endPoint.Y; // The lower value will be the starting point
    var imsEndY = startPoint.Y > endPoint.Y ? startPoint.Y : endPoint.Y; // The higher value will be the ending point
    DrawLineSegment(container, midX, imsStartY, midX, imsEndY, 1);

    // End segment
    DrawLineSegment(container, midX, endPoint.Y, endPoint.X, endPoint.Y, 1);
}

function DrawLineSegment(container, startX, startY, endX, endY, lineWidth) {

    var lineDiv = document.createElement("div");
    lineDiv.style.top = (startY - 225) + "px";
    lineDiv.style.left = startX + "px";

    if (startX == endX) { // Vertical Line
        lineDiv.style.width = lineWidth + "px";
        lineDiv.style.height = (endY - startY) + "px";
    }
    else{ // Horizontal Line
        lineDiv.style.width = (endX - startX) + "px";
        lineDiv.style.height = lineWidth + "px";
    }

    lineDiv.className = "NodeLine";
    container.appendChild(lineDiv);
}

function DrawNode(node, container, options) {

    var nodeDiv = document.createElement("div");
    nodeDiv.style.top = (node.Top - 225) + "px";
    nodeDiv.style.left = node.Left + "px";
    nodeDiv.style.width = node.Width + "px";
    nodeDiv.style.height = node.Height + "px";

    if (node.Collapsed) {
        nodeDiv.className = "NodeCollapsed";
    } else {
        nodeDiv.className = "Node";
    }

    if (node.Class)
        nodeDiv.className = node.Class;

    if (node.Content)
        nodeDiv.innerHTML = "<div class='NodeContent'>" + node.Content + "</div>";

    if (node.ToolTip)
        nodeDiv.setAttribute("title", node.ToolTip);

    nodeDiv.Node = node;

    // Events
    if (options.OnNodeClick)
        nodeDiv.onclick = options.OnNodeClick;
    if (options.OnNodeDoubleClick)
        nodeDiv.ondblclick = options.OnNodeDoubleClick;

    nodeDiv.onmouseover = function () { // In
        this.PrevClassName = this.className;
        this.className = "NodeHover";
    };

    nodeDiv.onmouseout = function () { // Out
        if (this.PrevClassName) {
            this.className = this.PrevClassName;
            this.PrevClassName = null;
        }
    };

    container.appendChild(nodeDiv);

    // Draw children
    if ((!node.Collapsed) && node.Nodes && node.Nodes.length > 0) { // Has Children and is Expanded
        for (var i = 0; i < node.Nodes.length; i++) {
            DrawNode(node.Nodes[i], container, options);
        }
    }
}

function PerformLayoutV(node) {

    var nodeHeight = 30;
    var nodeWidth = 400;
    var nodeMarginLeft = 50;
    var nodeMarginTop = 30;

    var nodeTop = 0; // defaultValue

    // Before Layout this Node, Layout its children
    if ((!node.Collapsed) && node.Nodes && node.Nodes.length > 0) {
        for (var i = 0; i < node.Nodes.length; i++) {
            PerformLayoutV(node.Nodes[i]);
        }
    }

    if ((!node.Collapsed) && node.Nodes && node.Nodes.length > 0) { // If Has Children and Is Expanded

        // My Top is in the center of my children
        var childrenHeight = (node.Nodes[node.Nodes.length - 1].Top + node.Nodes[node.Nodes.length - 1].Height) - node.Nodes[0].Top;
        nodeTop = (node.Nodes[0].Top + (childrenHeight / 2)) - (nodeHeight / 2);

        // Is my top over my previous sibling?
        // Move it to the bottom
        if (node.LeftNode && ((node.LeftNode.Top + node.LeftNode.Height + nodeMarginTop) > nodeTop)) {
            var newTop = node.LeftNode.Top + node.LeftNode.Height + nodeMarginTop;
            var diff = newTop - nodeTop;
            /// Move also my children
            MoveBottom(node.Nodes, diff);
            nodeTop = newTop;
        }

    } else {
        // My top is next to my top sibling
        if (node.LeftNode)
            nodeTop = node.LeftNode.Top + node.LeftNode.Height + nodeMarginTop;
    }

    node.Top = nodeTop;

    // The Left depends only on the level
    node.Left = (nodeMarginLeft * (node.Level + 1)) + (nodeWidth * (node.Level + 1));
    // Size is constant
    node.Height = nodeHeight;
    node.Width = nodeWidth;

    // Calculate Connector Points
    // Child: Where the lines get out from to connect this node with its children
    var pointX = node.Left + nodeWidth;
    var pointY = nodeTop + (nodeHeight/2);
    node.ChildrenConnectorPoint = { X: pointX, Y: pointY, Layout: "Vertical" };
    // Parent: Where the line that connect this node with its parent end
    pointX = node.Left;
    pointY = nodeTop + (nodeHeight/2);
    node.ParentConnectorPoint = { X: pointX, Y: pointY, Layout: "Vertical" };
}

function PerformLayoutH(node) {

    var nodeHeight = 175;
    var nodeWidth = 175;
    var nodeMarginLeft = 30;
    var nodeMarginTop = 50;

    var nodeLeft = 0; // defaultValue

    // Before Layout this Node, Layout its children
    if ((!node.Collapsed) && node.Nodes && node.Nodes.length>0) {
        for (var i = 0; i < node.Nodes.length; i++) {
            PerformLayoutH(node.Nodes[i]);
        }
    }

    if ((!node.Collapsed) && node.Nodes && node.Nodes.length > 0) { // If Has Children and Is Expanded

        // My left is in the center of my children
        var childrenWidth = (node.Nodes[node.Nodes.length-1].Left + node.Nodes[node.Nodes.length-1].Width) - node.Nodes[0].Left;
        nodeLeft = (node.Nodes[0].Left + (childrenWidth / 2)) - (nodeWidth / 2);

        // Is my left over my left node?
        // Move it to the right
        if(node.LeftNode&&((node.LeftNode.Left+node.LeftNode.Width+nodeMarginLeft)>nodeLeft)) {
            var newLeft = node.LeftNode.Left + node.LeftNode.Width + nodeMarginLeft;
            var diff = newLeft - nodeLeft;
            /// Move also my children
            MoveRigth(node.Nodes, diff);
            nodeLeft = newLeft;
        }
    } else {
        // My left is next to my left sibling
        if (node.LeftNode)
            nodeLeft = node.LeftNode.Left + node.LeftNode.Width + nodeMarginLeft;
    }

    node.Left = nodeLeft;

    // The top depends only on the level
    node.Top = (nodeMarginTop * (node.Level + 1)) + (nodeHeight * (node.Level + 1));
    // Size is constant
    node.Height = nodeHeight;
    node.Width = nodeWidth;

    // Calculate Connector Points
    // Child: Where the lines get out from to connect this node with its children
    var pointX = nodeLeft + (nodeWidth / 2);
    var pointY = node.Top + nodeHeight;
    node.ChildrenConnectorPoint = { X: pointX, Y: pointY, Layout:"Horizontal" };
    // Parent: Where the line that connect this node with its parent end
    pointX = nodeLeft + (nodeWidth / 2);
    pointY = node.Top;
    node.ParentConnectorPoint = { X: pointX, Y: pointY, Layout: "Horizontal" };
}

function MoveRigth(nodes, distance) {
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].Left += distance;
        if (nodes[i].ParentConnectorPoint) nodes[i].ParentConnectorPoint.X += distance;
        if (nodes[i].ChildrenConnectorPoint) nodes[i].ChildrenConnectorPoint.X += distance;
        if (nodes[i].Nodes) {
            MoveRigth(nodes[i].Nodes, distance);
        }
    }
}

function MoveBottom(nodes, distance) {
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].Top += distance;
        if (nodes[i].ParentConnectorPoint) nodes[i].ParentConnectorPoint.Y += distance;
        if (nodes[i].ChildrenConnectorPoint) nodes[i].ChildrenConnectorPoint.Y += distance;
        if (nodes[i].Nodes) {
            MoveBottom(nodes[i].Nodes, distance);
        }
    }
}

function PrepareNode(node, level, parentNode, leftNode, rightLimits) {

    if (level == undefined) level = 0;
    if (parentNode == undefined) parentNode = null;
    if (leftNode == undefined) leftNode = null;
    if (rightLimits == undefined) rightLimits = new Array();

    node.Level = level;
    node.ParentNode = parentNode;
    node.LeftNode = leftNode;

    if ((!node.Collapsed) && node.Nodes && node.Nodes.length > 0) { // Has children and is expanded
        for (var i = 0; i < node.Nodes.length; i++) {
            var left = null;
            if (i == 0 && rightLimits[level]!=undefined) left = rightLimits[level];
            if (i > 0) left = node.Nodes[i - 1];
            if (i == (node.Nodes.length-1)) rightLimits[level] = node.Nodes[i];
            PrepareNode(node.Nodes[i], level + 1, node, left, rightLimits);
        }
    }
}