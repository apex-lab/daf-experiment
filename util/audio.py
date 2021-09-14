from pyo import SDelay, Input, PinkNoise, Sig, Server
from sys import platform
import warnings

class AuditoryFeedback:
	'''
	Handles auditory feedback delays using Pyo. Actual delay times will 
	have a constant offset from desired delay, which must be measured for 
	your particular system (by recording mic input and sound card output 
	on the same clock).

	You might need to install JACK to use this, and set driver = 'jack',
	depending on your platform. Unfortunately, this probably won't
	play nicely with psychopy sound, since JACK likes to reserve the 
	soundcard. You can try setting an environment variable such as 
	export PYO_SERVER_AUDIO=jack` so psychopy/pyo uses JACK by default,
	and then editing __init__() to use the existing psychopy server (using 
	psychopy.sound with pyo backend).

	Tips for getting low-latency audio in linux:
		https://coroto.gitbook.io/linux-audio-survival-kit/
	'''

	def __init__(self, 
		input_chnl = 0,
		speech_gain = 10., noise_gain = 0., 
		driver = 'jack'
		):
		'''
		Initializes audio input->output graph with an initial delay of zero,
		not including the intrinsic system delay. 

		Can optionally provide gains for speech and noise to optimize 
		masking of bone conductance. 

		Can also specify the audio driver for pyo, so choose something that
		will work on your system. If you don't, the server will fail to boot,
		which throws an error but in another thread so process won't be killed.
		If sound doesn't play but you don't see an exception, that's probably
		what happened. 
		'''

		# start audio server
		if 'linux' in platform and driver.lower != 'jack':
			warnings.warn(
				'''
				pyo usually needs driver == 'jack' to work on linux 
				(since pyo's ALSA backend doesn't like PulseAudio).  
				Server may not boot properly, causing sound not to play.
				'''
				)
		self.server = Server(audio = driver, nchnls = 2).boot().start()

		## set up real-time audio processing graph 
		self._mic = Input(chnl = input_chnl)
		self._delayed = SDelay(self._mic, delay = 0)
		self._noise = PinkNoise() # mask bone conductant feedback
		self._speech_gain = Sig(speech_gain)
		self._noise_gain = Sig(noise_gain)
		out = self._speech_gain*self._delayed + self._noise_gain*self._noise
		self._out = out.mix(2) # add second channel

		# and begin
		self._out.out()

	def stop(self):
		self._out.stop()

	def set_delay(self, t):
		'''
		in milliseconds (not accounting for intrinsic system delay)
		'''
		self._delayed.setDelay(t * 1e-3)

	@property
	def delay(self):
		'''
		current delay in milliseconds (not accounting for system delay)
		'''
		return self._delayed.delay * 1e3

	def set_speech_gain(self, gain):
		self._speech_gain.setValue(gain)

	@property
	def speech_gain(self):
		return self._speech_gain.value

	def set_noise_gain(self, gain):
		self._noise_gain.setValue(gain)

	@property
	def noise_gain(self):
		return self._noise_gain.value

	

	