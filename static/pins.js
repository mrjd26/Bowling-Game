$(document).ready(function(){

 // initialization of globals for new game
 var frame = 1;
 var first_roll = true;
 var pins_standing = 10;
 var strike = false;
 var midframe = false;

 //click handler for bowling alley
 $("#alley").click(function(){
  
  ///////////////////////////////////////////////////
  //uncomment below and in views.py for user input testing
  /////////////////////////////////////////////////////////

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

   $.getJSON("/scorecard", {raw_input: user_input}, function (data) {
  /////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////
  ////////////////////////////////////////


  //servercall to progress game and return score in JSON
  //$.getJSON("/scorecard", function (data) {
    
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
       if (data[frame][0] == 'X') {
           strike = true;
        }
        else if (data[frame][1] == '/') {
           spare = true;
        }
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
        if (data[frame][1] == '/') {
         spare = true;
        } else {
         strike = true;
        }
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
   
  // jQuery animation on strike, spare, wash, or washout for 'alley' image
  if (strike) {
   $("#alley").queue(function(next) { $(this).attr('src','/static/strike.png') ; next(); })
              .delay(1000)
              .queue(function(next) { $(this).attr('src','/static/10.png'); next(); });
  }
  else if (spare) {
   
   $("#alley").queue(function(next) { $(this).attr('src','/static/spare.png') ; next(); })
              .delay(1000)
              .queue(function(next) { $(this).attr('src','/static/10.png'); next(); });
  }
  else if (wash) {
    $("#alley").attr('src', '/static/'+pins_standing+'.png');
  }
  else if (washout) {
    $("#alley").queue(function(next) { $(this).attr('src', '/static/'+pins_standing+'.png'); next(); })
               .delay(1500)           
               .queue(function(next) { $(this).attr('src', '/static/10.png'); next(); });
             
  }
  //end jQuery animation section for alley image


  //update global with server response
  frame = data.gamestate.frame;
  pins_standing = data.gamestate.pins_standing;
  midframe = data.gamestate.midframe;

  // end getJSON
  });

 // end click event handler
 });
//end jquery document.ready
});
