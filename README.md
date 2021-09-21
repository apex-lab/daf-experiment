# Delayed Auditory Feedback

This script runs a delayed auditory feedback experiment, recording events to an EEG system over TTL (using [RTBox](https://github.com/xiangruili/RTBox_py)). 

## Running the Experiment 

If all you want to do is run the experiment, and you're using Ubuntu/Debian, you can just load the [conda](https://www.anaconda.com/) environment in `environment.yml` and then run `python experiment.py`. You will probably need to install JACK first, since the real-time audio library we use, [pyo](https://github.com/belangeo/pyo), doesn't play nicely with PulseAudio, the default sound driver for most Linux workstations. You can follow [these instructions](https://coroto.gitbook.io/linux-audio-survival-kit/) to install JACK and for some tips on getting low latency audio in Ubuntu (or you can save yourself some trouble and check out [Ubuntu Studio](https://ubuntustudio.org)).

If you're on another platform, you need to have pyo, [PsychoPy](https://github.com/psychopy/psychopy), pynput and pyserial (for RTBox), numpy, and their dependencies installed. So pretty much everything in the [PsychoPy conda environment](https://raw.githubusercontent.com/psychopy/psychopy/master/conda/psychopy-env.yml) plus some change. You can choose any sound driver that works with pyo when you initialize `util.audio.AuditoryFeedback` (see documentation in `util/audio.py`).

## Controlling the Auditory Feedback

If you want to create a new experiment, using the code here to handle your feedback delays for you, the class to pay attention to is `util.audio.AuditoryFeedback`. It's pretty simple to use, as in the example below.

```
from util.audio import AuditoryFeedback
audio = AuditoryFeedback() # starts with no delay
audio.set_delay(100) # 100 ms delay
```

In addition to a vanilla delay, `AuditoryFeedback` also adds some pink noise to mask bone/air conductant feedback, though this behavior can be turned off (or up or down) with `audio.set_noise_gain(0)`. See `util/audio.py` for further documentation. You'll also see that the class itself isn't very complicated, so if you are familiar with pyo, it's easy to edit/add features. 

## Usage Note

The delays specificed using `audio.set_delay(delay)` don't account for the intrinsic system delay (from hardware, OS, etc.). It's impossible for me to say what those will be for any given setup, so you'll have to measure this on your own system by recording the mic input and sound card output on the same clock. The measured delay when `audio.delay == 0` is the system delay.

For reference, a Dell Precision Tower 5810 running Ubuntu 16.04 LTS clocks in at a little over 18 milliseconds delay between input and output using onboard audio and JACK/ALSA (sampling rate = 48k, buffer size = 256). The same machine using a Creative Sound Blaster Audigy 4 acheives a only modest speed boost, clocking in at 12.4 milliseconds (buffer size reduced to 64 frames since the sound card can handle it). Already this performance is [comparable to the setups regularly used in speech motor control/feedback alteration research](https://doi.org/10.1044/2020_JSLHR-19-00419). Installing a low-latency Linux kernel, however, further improves the delay on the same machine, acheiving a mere 4.02 millisecond lag with a 32 frame buffer.

Not that you actually _need_ low latency, as long as you can measure and report your delays accurately. The whole point is to delay your subjects' auditory feedback, after all. But if you want a true baseline condition, it's nice to get the intrinsic hardware/OS delay as low as possible. 
