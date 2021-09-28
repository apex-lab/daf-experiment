from psychopy import visual, event
from time import sleep
import numpy as np

def present(win, sentence):
	'''
	Displays a sentence on the screen.
	'''
	background = visual.Rect(win, width = 2, height = 2, color = "black")
	msg = visual.TextStim(win, text = sentence, color = "white", pos = (0,0))
	background.draw()
	msg.draw()
	win.flip()

def display(win, sentences):
	present(win, sentences)

def wait_for_keypress(win, message = ''):
	'''
	Wait until subject presses spacebar.
	'''
	if message:
		present(win, message)
	event.waitKeys(keyList = ["space"]) # wait until subject responds

def ask_whether_delay(win):
	'''
	Asks the subject whether they could detect an auditory feedback delay,
	and returns their response.
	'''
	txt = "Do you think your voice was delayed this time? (press 'y' or 'n')"
	present(win, txt)
	response = event.waitKeys(keyList = ['y', 'n'])
	if 'y' in response:
		return True
	else:
		return False

def fixation_cross(win):
	'''
	Displays a fixation cross for a random amount of time between
	200 and 400 milliseconds.
	'''
	background = visual.Rect(win, width = 2, height = 2, color = "black")
	fixation = visual.TextStim(win, text = '+', color = "white", pos = (0,0))
	background.draw()
	fixation.draw()
	win.flip()
	sleep(np.random.uniform(.2, .4))
