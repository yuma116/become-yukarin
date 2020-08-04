from glob import glob
from pathlib import Path
import argparse
from progress.bar import Bar
from functools import partial

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


def command():
	parser = argparse.ArgumentParser(description="help")
	parser.add_argument('--iteration_min',default=5000, help="min iteration of the model")
	parser.add_argument('--iteration_max',default=5000, help="max iteration of the model")
	
	args = parser.parse_args()
	return args

def inference(model_itr, bar):
	bar.next()		
	model_path = Path('05output/predictor_'+str(model_itr)+'.npz')
	config_path = Path('recipe/config.json')
	config = create_config(config_path)
	acoustic_converter = AcousticConverter(config, model_path, gpu=0)
	wave = acoustic_converter(voice_path="01input02/music0001_80.wav")
	librosa.output.write_wav('inference_output_'+str(model_itr)+'.wav', wave.wave, wave.sampling_rate, norm=True)


def main(args):
	bar = Bar("", max=(int(args.iteration_max)/5000) - int(args.iteration_min)/5000+1)
	# for itr in range(int(args.iteration_min), int(args.iteration_max)+1, 5000):
	inference_partial = partial(inference, bar=bar)
	list(map(inference_partial, range(int(args.iteration_min), int(args.iteration_max)+1, 5000)))





if __name__ == '__main__':
	main(command())