#helper.py

def calculate_score(scorecard, frame, midframe, total):
  
  #function to update the scorecard on completed bowling frames
  #args: next bowling frame to begin, a score tally
  #returns an updated score card including previouis frame total
  print total,'start' 
  last_frame = frame - 1
  score = scorecard

  if frame > 1:
    #tabulate score after last frame spare with pins hit
    if score[last_frame][1] == '/' and midframe:
      score[last_frame][2] = 10 + score[frame][0] + total
      total += 10 + score[frame][0]
    #last frame spare at start of next frame
    elif score[last_frame][1] == '/' and not midframe:
      score[last_frame][2] = ''
    #tabulate score for last frame if no strike or spare
    elif score[last_frame][1] + score[last_frame][0] < 10:
      if frame > 2:
        if score[last_frame-1][0] != 'X' and midframe == False:
          score[last_frame][2] = score[last_frame][0] + score[last_frame][1] + total
          total += score[last_frame][0] + score[last_frame][1]
      if frame == 2:
          if midframe == False:      
            score[last_frame][2] = score[last_frame][0] + score[last_frame][1] + total
            total += score[last_frame][0] + score[last_frame][1]

  if frame > 2:
    # handle spare after strike scenario
    if score[last_frame-1][0] == 'X' and score[last_frame][1] == '/':
      if midframe == False:
        score[last_frame-1][2] = 10 + 10 + total
        total += 10 + 10
    # handle strike after spare scenario
    elif score[last_frame-1][1] == '/' and score[last_frame][0] == 'X':
       if midframe == False:
         score[last_frame-1][2] = 10 + 10 + total
         total += 10 + 10
    #handle strike followed by wash
    elif score[last_frame-1][0] == 'X' and score[last_frame][1] != '/':
      if ((score[last_frame][0] + score[last_frame][1]) < 10):
        if midframe == False:
          score[last_frame-1][2] = score[last_frame][0] + score[last_frame][1] + 10 + total
          total += 10 + score[last_frame][0] + score[last_frame][1]
          score[last_frame][2] = score[last_frame][0] + score[last_frame][1] + total
          total += score[last_frame][0] + score[last_frame][1]

  #handle two strikes in a row (calculated mid frame)
  if frame > 2 and midframe:
    if score[last_frame-1][0] == 'X' and score[last_frame][0] == 'X':
      if score[frame][0] != 'X':
        score[last_frame-1][2] = 10 + 10 + score[frame][0] + total
        total += 10 + 10 + score[frame][0]

  if last_frame > 2:
    if score[last_frame-2][0] == 'X' and midframe == False:
      #handle three  strikes in a row
      if score[last_frame][0] == 'X' and score[last_frame-1][0] == 'X':
        score[last_frame-2][2] = 10 + 10 + 10 + total
        total += 10 + 10 + 10
  
  return score, total

def calculate_10th(score, frame, first_roll, second_roll, third_roll, total):
  
  #unless otherwise changed, game continues to run...
  game_state = "running"

  last_frame = frame - 1
  
  #finalize scorecard for 8th frame if needed
  if score[last_frame-1][0] == 'X' and second_roll:
    #calculate turkey on 8th
    if score[last_frame][0] == 'X' and score[frame][0] == 'X':
      score[last_frame-1][2] = 10 + 10 + 10 + total
      total += 10 + 10 + 10

    #calculate two strikes beginning on 8th
    elif score[last_frame][0] == 'X' and score[frame][0] != 'X':
      score[last_frame-1][2] = 10 + 10 + score[frame][0] + total
      total += 10 + 10 + score[frame][0]


  #finalize scorecard for 9th frame if needed
  if score[last_frame][0] == 'X' and third_roll:
    #turkey on 9th
    if score[frame][0] == 'X' and score[frame][1] == 'X':
      score[last_frame][2] = 10 + 10 + 10 + total
      total += 10 + 10 + 10
    #two strikes beginning on 9th
    elif score[frame][0] == 'X' and score[frame][1] != 'X':
      score[last_frame][2] = 10 + 10 + score[frame][1] + total
      total += 10 + 10 + score[frame][1]
      print "this function"
    #spare in first two rolls of tenth 
    elif score[frame][1] == '/':
      score[last_frame][2] = 10 + 10 + total
      total += 10 + 10
  
  #wash in first two rolls of tenth, ending the game
  if score[last_frame][0] == 'X' and third_roll == False:
    if second_roll == False and first_roll == False:
      if score[frame][0] != 'X' and score[frame][1] != '/':
        score[last_frame][2] = 10 + score[frame][0] + score[frame][1] + total
        total += 10 + score[frame][0] + score[frame][1]
  

  #continued...spare scenarios for 9th frame
  if score[last_frame][1] == '/' and second_roll == True:
    #10 frame first roll strike, following 9th spare
    if score[frame][0] == 'X':
      score[last_frame][2] = 10 + 10 + total
      total += 10 + 10
    if score[frame][0] != 'X':
      score[last_frame][2] = 10 + score[frame][0] + total
      total += score[frame][0] + 10
    

  #tabulating score for 10th frame
  if first_roll == False and second_roll == False:
    if third_roll == False:
      #switch game state to Game Over and...
      game_state = "Game Over"

      #tabulate final score...
      #strike on first roll...
      if score[frame][0] == 'X':
        #turkey
        if score[frame][1] == 'X' and score[frame][2] == 'X':
          score[frame][3] = 10 + 10 + 10 + total
        #strike then spare
        if score[frame][2] == '/':
          score[frame][3] = 10 + 10 + total
        #strike then wash, ending game, no bonus roll
        if score[frame][1] != 'X' and score[frame][2] != '/':
          score[frame][3] = 10 + score[frame][1] + score[frame][2] + total
      #spare in first two rolls...
      if score[frame][1] == '/':
        #strike following spare
        if score[frame][2] == 'X':
          score[frame][3] = 10 + 10 + total
        #third roll wash following spare
        if score[frame][2] != 'X':
          score[frame][3] = 10 + score[frame][2] + total
      #wash on first two rolls, ending game without bonus roll
      if score[frame][0] != 'X' and score[frame][1] != '/':
        score[frame][3] = score[frame][0] + score[frame][1] + total

  return score, game_state, total
