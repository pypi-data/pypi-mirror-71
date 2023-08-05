
console.log("drawing level 1")


var winPlace = null;
var losePlaces = [];

for (var x = 5; x < 410; x+=50){
	var gridX= new Path.Line(new Point(x,5), new Point(x,205))
	gridX.strokeColor =  new Color(0,0,0,0.5);
	gridX.strokeWidth = 1;
}

for (var y = 5; y < 210; y+=50){
	var gridY= new Path.Line(new Point(5,y), new Point(405,y))
	gridY.strokeColor =  new Color(0,0,0,0.5);
	gridY.strokeWidth = 1;
}

DrawAppleAt(3,3)
DrawDeadlyCellAt(0,2);
DrawDeadlyCellAt(1,2);
DrawDeadlyCellAt(2,2);
DrawDeadlyCellAt(2,3);


console.log("level drawing complete!")


function DrawAppleAt(x,y){
	var apple = new Path.Circle({
		center: [0,0],
		radius: 10,
		fillColor: "green",
	});
	
	var stem = new Path({
		segments: [[-4, -12], [0, -8], [5, -15]],
		strokeColor: "#bd5800",
		strokeWidth: 3,
	});
	
	
	apple.translate(x*50 + 5 + 25, y*50 +5 + 25);
	stem.translate(x*50 + 5 + 25, y*50 +5 + 25);
	
	winPlace = new Point(x*50 + 5 + 25, y*50 +5 + 25);
}

function DrawDeadlyCellAt (x,y){
	var deadlyCell = new Path.Rectangle({
		point: [-23,-23],
		size: [46, 46],
		fillColor: 'red'
	});
	
	deadlyCell.translate(x*50 + 5 + 25, y*50 +5 + 25);
	
	losePlaces.push(new Point(x*50 + 5 + 25, y*50 +5 + 25));
}