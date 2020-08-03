from glob import glob
from pathlib import Path

import numpy

from become_yukarin.config.config import create_from_json as create_config
from become_yukarin.config.sr_config import create_from_json as create_sr_config
from become_yukarin.dataset.dataset import AcousticFeatureProcess
from become_yukarin.dataset.dataset import WaveFileLoadProcess
from become_yukarin.param import Param
from become_yukarin import SuperResolution
from become_yukarin import AcousticConverter

import matplotlib.pyplot as plt

import librosa
# from IPython.display import Audio

model_path = Path('05output/predictor_35000.npz')
config_path = Path('recipe/config.json')
config = create_config(config_path)
acoustic_converter = AcousticConverter(config, model_path)
# acoustic_converter = AcousticConverter(config, model_path, gpu=0)

# rate = sr_config.dataset.param.voice_param.sample_rate
wave = acoustic_converter(voice_path="01input02/music0001_80.wav")
# Audio(data=wave.wave, rate=rate)
librosa.output.write_wav('inference_output0001.wav', wave.wave, wave.sampling_rate, norm=True)
# print(type(wave))
