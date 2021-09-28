from collections import OrderedDict
from sys import stdout
import numpy as np
from time import time

from util import load_harvard_sentences
from util.events import EventMarker
from util.audio import AuditoryFeedback
from util.ui import (
	fixation_cross,
	display,
	wait_for_keypress,
	ask_whether_delay
	)
from util.write import TSVWriter
from psychopy.visual import Window

# specify block design
BLOCKS = OrderedDict()
BLOCKS['baseline'] = (5, 0) # n_trials, milliseconds delay
BLOCKS['random1'] = (0, None) # None denotes random delay
BLOCKS['adaption'] = (0, 200)
BLOCKS['random2'] = (0, None)

# initialize some things
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
log = TSVWriter(subj_num)
np.random.seed(subj_num)
sentences = load_harvard_sentences(randomize = True)
marker = EventMarker()
audio = AuditoryFeedback()
win = Window(
	size = (1920, 1080),
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)
t1 = time()

########################
# instructions
########################
txt = '''
In this experiment, you will be asked to read sentences out loud.
(press spacebar to continue through instructions)
'''
wait_for_keypress(win, txt)
txt = '''
On each trial, you will press the spacebar to begin.
A sentence will then appear on the screen after a brief
fixation period; please read it immediately.
'''
wait_for_keypress(win, txt)
txt = '''
Please start reading the sentence out loud as soon as you see it,
and then press the spacebar as soon as you have finshed reading.
(but not sooner).
'''
wait_for_keypress(win, txt)
txt = '''
On some trials, your speech will be artificially delayed before you hear it.
After each trial, you will be asked if you perceived any such delay.
'''
wait_for_keypress(win, txt)
txt = '''
Please be silent between sentences/trials. We are recording your
brain activity during speech as well as silence,
and both are equally crucial to the experiment.
'''
wait_for_keypress(win, txt)
txt = '''
If you need to get the attention of the experimenter, there is a
button on your desk.
'''
wait_for_keypress(win, txt)
txt = '''
That's it! Please let the experimenter know if you have any questions.
Otherwise, you can continue to the experiment by pressing the spacebar.
'''
wait_for_keypress(win, txt)


########################
# experiment
########################
for block_code in BLOCKS:

	t2 = time()
	print("\nBeginning %s block\n"%block_code)
	print("It's been %d minutes since the experiment started."%((t2 - t1)/60))
	des = BLOCKS[block_code]
	n_trials = des[0]

	for trial in range(n_trials):

		# decide what to do this trial
		delay = np.random.randint(0, 251) if des[1] is None else des[1]
		sentence = sentences.pop(0)

		# keep experimenter in the loop via console
		stdout.write("\rTrial {0:03d}".format(trial) + "/%d"%n_trials)
		stdout.flush()

		# now actually run the trial
		wait_for_keypress(win, message = 'Press spacebar to continue.')
		audio.set_delay(delay)
		fixation_cross(win)
		display(win, sentence) # flips screen
		marker.send(trial) # mark with trial number
		log.write(block_code, trial, delay, sentence)
		wait_for_keypress(win)
		marker.send(127) # end trial
		detected_delay = ask_whether_delay(win)
		resp_tag = 125 if detected_delay else 126
		marker.send(resp_tag)

t2 = time()
print('Experiment Complete.')
print('The experiment took %d minutes.'%((t2 - t1)/60))

##########################
# and we're done!
##########################
txt = '''
That's all! You can press the spacebar to end the experiment.
If the experimenter doesn't come get you immediately, let them
know you're done using the button on your desk.
'''
wait_for_keypress(win, txt)
