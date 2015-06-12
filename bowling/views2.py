from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
import json
from django.utils.datastructures import SortedDict
from random import randrange
from helper import calculate_score, calculate_10th

def index(request):
  
  # initialize new game on page load for browser sessions
  # init bowling frame, setup pins, first roll = True
  # scorecard dictionary initialized for new game
  
  frame = 1
  request.session['frame'] = frame 
  pins_standing = 10
  request.session['pins_standing'] = pins_standing
  request.session['first_roll'] = True
  request.session['game_state'] = "running" 

  request.session['score'] = {
              1: ['', '', ''],
              2: ['', '', ''],
              3: ['', '', ''],
              4: ['', '', ''],
              5: ['', '', ''],
              6: ['', '', ''],
              7: ['', '', ''],
              8: ['', '', ''],
              9: ['', '', ''],
              10: ['', '', '', ''],
              'gamestate': {
                            'frame': '',
                            'first_roll': True,
                            'second_roll': False,
                            'third_roll': False,
                            'midframe': False,
                            'game_state': '',
                            'pins_standing': pins_standing,
               }
          }

  return render(request, 'index.html')


def game_flow(request):

  '''
  describes flow of bowling game and calls helper.py
  to tabulate score; keeps track of game 'states' like
  current bowling frame, pins standing, first or second roll
  args: none
  returns: scorecard with json data
  '''

  first_roll = request.session.get('first_roll')
  second_roll = request.session.get('second_roll')
  third_roll = request.session.get('third_roll')
  frame = request.session.get('frame')
  pins_standing = request.session.get('pins_standing')
  score = request.session.get('score')
  game_state = request.session.get('game_state')


  if game_state != "running":
    #Game Over.....prompt user to refresh browser
    pass
  else:  
    #continue flow of game
    if first_roll:
      pins_standing = 10

    # used later for 10th frame
    #initializes pin setup for strike scenarios
    if frame == 10:
      if second_roll and score[frame][0] == 'X':
        pins_standing = 10
      if third_roll and score[frame][1] == 'X':
        pins_standing = 10
      if third_roll and score[frame][1] == '/':
        pins_standing = 10

    #randomly hit pins on range 0 to 10
    pins_hit = randrange(0,pins_standing + 1)
    
    """
    uncomment below for unit testing
    """
    #pins_hit = int(request.GET['raw_input'])
    """
    """

    pins_standing = pins_standing - pins_hit
    request.session['pins_standing'] = pins_standing

    #game flow for first 9 frames
    if frame < 10:

      #handle strike scenario
      if first_roll and pins_standing == 0:
        score[frame][0] = "X"
        frame += 1 
        first_roll = True
        midframe = False
      #progress to second roll
      elif first_roll and pins_standing > 0:
        score[frame][0] = pins_hit
        first_roll = False
        midframe = True
      #handle spare scenario
      elif not first_roll and pins_standing == 0:
        score[frame][1] = "/"
        frame += 1
        request.session['frame'] = frame
        first_roll = True
        request.session['first_roll'] = first_roll
        midframe = False
      #end of rolls, progress to next frame
      else:
        score[frame][1] = pins_hit
        frame += 1
        first_roll = True
        midframe = False
 
      score = calculate_score(score, frame, midframe)

      '''
      game flow to handle 10th frame
      ''' 
    else:
      #first roll pins still standing
      if first_roll and pins_standing > 0:
        score[frame][0] = pins_hit
        second_roll = True
        first_roll = False
        third_roll = False
        midframe = True
      #first roll strike
      elif first_roll and pins_standing == 0:
        first_roll = False
        second_roll = True
        third_roll = False
        midframe = False
        score[frame][0] = 'X'

      #second roll scenarios
      elif second_roll and pins_standing > 0:
        #player gets bonus roll attempt for spare
        if score[frame][0] == 'X':
          first_roll = False
          second_roll = False
          third_roll = True
          midframe = True
          score[frame][1] = pins_hit
        #player does not get bonus roll
        else:
          first_roll = False
          second_roll = False
          third_roll = False
          midframe = False
          score[frame][1] = pins_hit

      # handle spare or strike scenario
      # award bonus roll
      elif second_roll and pins_standing == 0:
        if score[frame][0] == 'X':
          score[frame][1] = 'X'
          second_roll = False
          third_roll = True
          first_roll = False
          midframe = False
        else:
          score[frame][1] = '/'
          second_roll = False
          third_roll = True
          first_roll = False
          midframe = False

      #handle third roll scenarios
      elif third_roll and pins_standing > 0:
        score[frame][2] = pins_hit
        first_roll = False
        second_roll = False
        third_roll = False
        midframe = False
      elif third_roll and pins_standing == 0:
        #determine if spare or strike
        if score[frame][1] == 'X':
          score[frame][2] = 'X'
          third_roll = False
          first_roll = False
          second_roll = False
          midframe = False
        elif score[frame][1] == '/':
          score[frame][2] = 'X'
          third_roll = False
          first_roll = False
          second_roll = False
          midframe = False
        else:
          score[frame][2] ='/'
          third_roll = False
          first_roll = False
          second_roll = False
          midframe = False
   
      #update scores, check game state from helper file 
      score, game_state = calculate_10th(score, frame, first_roll, second_roll, third_roll)

    request.session['frame'] = frame
    request.session['first_roll'] = first_roll
    request.session['second_roll'] = second_roll
    request.session['third_roll'] = third_roll
    request.session['score'] = score
    request.session['game_state'] = game_state

    score['gamestate']['frame'] = frame
    score['gamestate']['pins_standing'] = pins_standing
    score['gamestate']['first_roll'] = first_roll
    score['gamestate']['game_state'] = game_state 
    score['gamestate']['midframe'] = midframe  
    score['gamestate']['second_roll'] = second_roll
    score['gamestate']['third_roll'] = third_roll    

    return HttpResponse(json.dumps(score))
