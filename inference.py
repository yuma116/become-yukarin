from glob import glob
from pathlib import Path
import argparse
from progress.bar import Bar
from functools import partial
import pathlib

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
	parser.add_argument('--input_file',default=5000, help="input file (.wav) for the inference")
	parser.add_argument('--output_dir',default=5000, help="output directory of the inference")
	
	args = parser.parse_args()
	return args

def inference(model_itr, bar,input_file , output_dir):
	bar.next()		
	model_path = Path('05output/predictor_'+str(model_itr)+'.npz')
	config_path = Path('recipe/config.json')
	config = create_config(config_path)
	acoustic_converter = AcousticConverter(config, model_path, gpu=0)
	wave = acoustic_converter(voice_path=input_file)
	output_file = pathlib.PurePath(output_dir, 'i_'+str(model_itr)+'.wav')

	librosa.output.write_wav(str(output_file), wave.wave, wave.sampling_rate, norm=True)


def main(args):
	"""
	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	output_dir = pathlib.Path(args.output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)
	bar = Bar("", max=(int(args.iteration_max)/5000) - int(args.iteration_min)/5000+1)
	# for itr in range(int(args.iteration_min), int(args.iteration_max)+1, 5000):
	inference_partial = partial(inference, bar=bar, input_file=args.input_file, output_dir=args.output_dir)
	list(map(inference_partial, range(int(args.iteration_min), int(args.iteration_max)+1, 5000)))





if __name__ == '__main__':
	main(command())