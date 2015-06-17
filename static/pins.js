$(document).ready(function(){

 //player has possession of ball
 var possession = true;
 var fps = 30;
 var ball_x;
 var ball_y;
 var ball_W = 82;
 var ball_H = 84;
 var collision = false;
 var alley = document.createElement("img");
 alley.src = "/static/alley.png";
 var pin = document.createElement("img");
 pin.src = "/static/pin.png";
 var ball = document.createElement("img");
 ball.src = "/static/ball1.png";
 console.log(ball.width);
 var crash = document.createElement("img");
 crash.src = "/static/crash.png";

 var symbol = document.createElement("img");
 symbol.src = "/static/strike10.png";

 var canvas = document.getElementById("myCanvas");
 var ctx = canvas.getContext("2d");
 ctx.drawImage(alley, 0, 0);

 var animate = false;
 var collisionCount = 0;
 var d = 10;
 var fadeCount = 0;
 var s = 'strike';

  function reDraw() {
   ctx.drawImage(alley,0,0);
    for(var key in pin_position) {
      var x = pin_position[key][0];
      var y = pin_position[key][1];
      ctx.drawImage(pin,x,y);
    }
    if (collision && (collisionCount < 10) ) {
      ctx.drawImage(crash,200,60);
      collisionCount = collisionCount + 1;
    } else if (animate) {
        if (d >= 0 ) {
         symbol.src = "/static/" + s + d + ".png";
         ctx.drawImage(symbol, 50, 50);
         d--;
         setTimeout(function(){animate = false},500);
        }
    } else  {
   // ctx.drawImage(ball,ball_x-50,ball_y-50,ball_W,ball_H);
   }
   ctx.drawImage(ball,ball_x-50,ball_y-50,ball_W,ball_H);
  }

  setInterval(reDraw, 1000 / fps);
      
  function getMousePos(canvas, evt) {
        var rect = canvas.getBoundingClientRect();
        return {
          x: evt.clientX - rect.left,
          y: evt.clientY - rect.top
        };
      }

      canvas.addEventListener('mousemove', function(evt) {
        if (possession) {
         var mousePos = getMousePos(canvas, evt);
          ball_x = mousePos.x;
          ball_y = mousePos.y;
        }
      });

  function randomInt() {
    var num = Math.floor((Math.random() * 10) + 1);
    return num;
  }

  function roll() {
    possession = false;
    if(ball_y < 180) {
      console.log('done!');
    } else if(ball_y < 225) { 
      setTimeout(function() {
        ball_y = ball_y - 2;
        roll();
        ball_W = ball_W - 0.4;
        ball_H = ball_H - 0.4;
        var n = randomInt();
        ball.src = "/static/ball" + n + ".png";
      }, 1);
    } else {
      setTimeout(function() {
        ball_y = ball_y - 4;
        roll();
        ball_W = ball_W - 0.6;
        ball_H = ball_H - 0.6;
        var n = randomInt();
        ball.src = "/static/ball" + n + ".png";
      }, 1);
    }
  }

 function init() {

    collisionCount = 0;
    collision = true;
    setTimeout(function(){possession = true;},300);
    ball.src = "/static/ball1.png";
    ball_x = -100;
    ball_y = 0;
    ball_H = 82;
    ball_W = 84;
 }
/*
 ctx.drawImage(pin, 240, 85);
 ctx.drawImage(pin, 270, 85);
 ctx.drawImage(pin, 300, 85);
 ctx.drawImage(pin, 330, 85);
 
 ctx.drawImage(pin, 255, 95);
 ctx.drawImage(pin, 285, 95);
 ctx.drawImage(pin, 315, 95);
 
 ctx.drawImage(pin, 270, 105);
 ctx.drawImage(pin, 300, 105);

 ctx.drawImage(pin, 285, 115);
*/



 // initialization of globals for new game
 var frame = 1;
 var first_roll = true;
 var pins_standing = 10;
 var strike = false;
 var midframe = false;

 //click handler for bowling alley
 $("#myCanvas").click(function(){
  
 /*************** TOGGLE FOR USER INUPT TESTING *************
  function get_user_input() { 
   if ((midframe) && (pins_standing)) {  
    var user_input = prompt("pins standing: " + pins_standing, "0 - " + pins_standing);
   } else {
    var user_input = prompt("pins standing: " + 10, "0 - 10");
   }
   return user_input;
  }
  var user_input = get_user_input();
  while (user_input > pins_standing) {
    var user_input = get_user_input();
  }
****************************************************************/

  // animate roll of bowling ball
  ball_H = 82;
  ball_W = 84;
  ball_y = 400;
  roll();

  //let ball roll finish
  setTimeout(function(){

   /******    TOGGLE FOR USER INPUT TESTING ********************************/
   //  $.getJSON("/scorecard", {raw_input: user_input}, function (data) {
   $.getJSON("/scorecard", function (data) {
   ///**********************************************************************/ 
    pin_position = data.gamestate.pin_position;
    //reset 'outcomes'
    spare = false;
    strike = false;
    //player knocks down some pins on first roll, but not all
    wash = false;
    // player ends frame with some pins left standing
    washout = false;

    //check if game is not in final frame
    if (frame != 10) {
     //bowling frame has advanced
     if (( data.gamestate.frame == (frame + 1)) && 
           data.gamestate.first_roll == true ) {
      //determine if strike or spare
      if (data.gamestate.pins_standing == 10) {
       if (data[frame][0] == 'X') {strike = true;}
       else if (data[frame][1] == '/') {spare = true;}
       else {
           //...or if pins left standing
           washout = true;
       }
      }
     } 
     //middle of frame and some pins left standing
     else if ((data.gamestate.midframe == true) && (data.gamestate.first_roll == false)) {
      wash = true;
      pins_standing = data.gamestate.pins_standing;
     }
     //game is in tenth frame
     } else {     
      if (data.gamestate.game_state == 'running') {
       // 1st roll strike
       if (data.gamestate.second_roll && data.gamestate.pins_standing == 10) {
        strike = true;
       }
       // second roll strike or spare
       else if (data.gamestate.third_roll && data.gamestate.pins_standing == 10) {
        if (data[frame][1] == '/') {spare = true;} 
        else {strike = true;}
       }
       //pins left standing midframe      
       else if (data.gamestate.midframe && data.gamestate.pins_standing > 0) {
        wash = true;
        pins_standing = data.gamestate.pins_standing;
       }
      } else {
       //display game over png
       $("#alley").attr('src', '/static/game_over.png');
      }
     }

    // needed for handlebars.js to update template
    // the template code, compile the template
    var source = $("#scorecard-template").html();
    var template = Handlebars.compile(source);
    var html = template(data);
    $("#handlebars_container").html(html);
   
  // animation on strike, spare, wash, or washout
  if (strike) {
    d = 10;
    animate = true;
    init();
  }
  else if (spare) {
    d = 10;
    animate = true;
    init();
  }
  else if (wash) {
   init();
  }
  else if (washout) {
    $.getJSON("/reset", 
      {payload: JSON.stringify(data)}, 
      function (response) {
        pin_position = response.gamestate.pin_position;
        console.log('response',response);
      });
    init();
  }
  //end animation section


  //update global with server response
  frame = data.gamestate.frame;
  pins_standing = data.gamestate.pins_standing;
  midframe = data.gamestate.midframe;

  // end getJSON
  });
  // end setTimeout
  }, 500);
 // end click event handler
 });

    var source = $("#scorecard-template").html();
    var template = Handlebars.compile(source);
    var html = template();
    $("#handlebars_container").html(html);
//end jquery document.ready
});
