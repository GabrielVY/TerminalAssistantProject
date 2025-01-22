import pyaudio
import wave
import numpy
import math
import time

# Settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
SILENCE_THRESHHOLD = 50  # Db


class Microphone:

    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()

        self.stream = None

        self.i = 0
        self.capturing = False
        self.frames = []

        # Timer, measure lenght of recording
        self.time_elapsed = 0
        self.start_time = 0
        self.end_time = 0

    def start_capturing(self):
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        self.i = 0
        self.frames.clear()
        self.capturing = True
        self.start_time = time.time()

    def stop_capturing(self):
        if self.capturing:
            self.stream.stop_stream()
            self.stream.close()
            # self.p.terminate()

            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()

        self.capturing = False

    def capture(self):
        if not self.is_capturing():
            return

        if self.i >= RATE / CHUNK * RECORD_SECONDS:
            self.stop_capturing()
            return

        data = self.stream.read(CHUNK)
        self.frames.append(data)
        self.i += 1

        # Each 2 secounds check the amplitude of the audio, if no one is talking stop caputuring
        # Linear value between 0 -> 1
        if self.time_elapsed >= 2:
            if len(data) > 0:
                if 2 == 4:
                    self.start_time = time.time()
                    blockLinearRms = numpy.sqrt(numpy.mean(data**2))
                    blockLogRms = 20 * math.log10(blockLinearRms)
                    self.time_elapsed = 0

        self.end_time = time.time()
        self.time_elapsed = self.end_time - self.start_time

    def is_capturing(self):
        return self.capturing
    
    def close(self):
        if self.stream:
            self.stream.close()
        self.p.terminate()
