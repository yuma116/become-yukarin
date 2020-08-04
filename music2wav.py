import argparse
import pathlib
import os
import soundfile
from progress.bar import Bar



def command():
	parser = argparse.ArgumentParser(description="help")
	parser.add_argument('mode', choices=["wave", "spleeter", "rename", "short"], help="select a mode")
	parser.add_argument('--input', help="input music directory")
	parser.add_argument('--output', help="output directory")
	
	args = parser.parse_args()
	return args

def main(args):

	if args.mode == "wave":
		wave(args)
	elif args.mode == "spleeter":
		spleeter(args)
	elif args.mode == "rename":
		rename(args)
	elif args.mode == "short":
		short(args)

def wave(args):
	"""
	convert files to wave and rename

	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	files = pathlib.Path(args.input)
	i = 1
	for file in files.iterdir():
		parent = str(file.parent)
		filename = pathlib.PurePosixPath(file).stem
		if args.output is None:
			output_file = pathlib.Path(parent+"/output", "/music"+str(i).zfill(4)+".wav")
		else:
			output_file = pathlib.Path(args.output+"/music"+str(i).zfill(4)+".wav")
		output_file.parent.mkdir(parents=True, exist_ok=True)
		os.system("ffmpeg -i "+str(pathlib.PurePath(parent,file.name))+" -ar 24000 "+str(output_file))
		i+=1

def spleeter(args):
	"""
	run spleeter

	:param      args:  The arguments
	:type       args:  { type_description }
	"""

	bar = Bar("", max=len(os.listdir(args.input)))
	files = pathlib.Path(args.input)
	i = 1
	for file in files.iterdir():
		parent = str(file.parent)
		filename = pathlib.PurePosixPath(file).stem
		if args.output is not None:
			output_dir = pathlib.Path(args.output)
		
		output_dir.mkdir(parents=True, exist_ok=True)
		os.system("spleeter separate -i "+str(pathlib.PurePath(parent,file.name))+" -o "+str(output_dir)+" -p spleeter:5stems")
		i+=1
		bar.next()

def rename(args):
	"""
	rename extracted vocal file

	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	dirs = pathlib.Path(args.input)
	# i = 1
	output_dir = pathlib.Path(args.output)
	output_dir.mkdir(parents=True, exist_ok=True)

	for dr in dirs.iterdir():
		filename = dr.name
		filename_in = pathlib.Path(str(dr)+"/piano.wav")
		filename_out = pathlib.PurePath(args.output, filename+".wav")
		os.system("cp "+str(filename_in)+" "+str(filename_out))

def short(args):
	"""
	separate music into 20 sec

	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	files = pathlib.Path(args.input)
	i = 1
	# for all files in the directory
	for file in files.iterdir():
		input_file = str(file)
		music = soundfile.SoundFile(input_file)
		length = int(len(music) / music.samplerate)
		output_dir = pathlib.Path(args.output)
		output_dir.mkdir(parents=True, exist_ok=True)
		# separate music into 20 sec
		for start in range(0, length, 20):
			output_file = str(pathlib.PurePath(output_dir, file.stem+"_"+str(start)+".wav"))
			os.system("ffmpeg -i "+input_file+" -ss "+str(start)+" -to "+str(start+20 if start+20 < length else length)+" -c copy "+output_file)
		i+=1



if __name__ == '__main__':
	main(command())