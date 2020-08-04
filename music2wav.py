import argparse
import pathlib
import os
import soundfile


def command():
	parser = argparse.ArgumentParser(description="help")
	parser.add_argument('mode', choices=["wave", "spleeter", "conv_name", "short"], help="select a mode")
	parser.add_argument('--input', help="input music directory")
	parser.add_argument('--output', help="output directory")
	
	args = parser.parse_args()
	return args

def main(args):

	if args.mode == "wave":
		wave(args)
	elif args.mode == "spleeter":
		spleeter(args)
	elif args.mode == "conv_name":
		conv_name(args)
	elif args.mode == "short":
		short(args)

def wave(args):
	"""
	convert files to wave

	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	files = pathlib.Path(args.input)
	i = 1
	for file in files.iterdir():
		parent = str(file.parent)
		filename = pathlib.PurePosixPath(file).stem
		output_name = "music"+str(i).zfill(4)
		os.system("ffmpeg -i "+str(pathlib.PurePath(parent,file.name))+" -ar 24000 "+str(pathlib.PurePath(parent,output_name))+".wav")
		i+=1

def spleeter(args):
	"""
	run spleeter

	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	files = pathlib.Path(args.input)
	i = 1
	for file in files.iterdir():
		parent = str(file.parent)
		filename = pathlib.PurePosixPath(file).stem
		if args.output is not None:
			output_name = str(args.output)
		else:
			output_name = "music"+str(i).zfill(4)
	
		print("spleeter separate -i "+str(pathlib.PurePath(parent,file.name))+" -o "+output_name+" -p spleeter:5stems")
		os.system("spleeter separate -i "+str(pathlib.PurePath(parent,file.name))+" -o "+output_name+" -p spleeter:5stems")
		i+=1

def conv_name(args):
	"""
	rename extracted vocal file

	:param      args:  The arguments
	:type       args:  { type_description }
	"""
	files = pathlib.Path(args.input)
	i = 1
	for file in files.iterdir():
		parent = str(pathlib.PurePath(file.parent, "music"+str(i).zfill(4)))
		filename = pathlib.PurePosixPath(file).stem
		output_name = str(pathlib.PurePath(args.output, "music"+str(i).zfill(4)+".wav"))
		# print("cp "+str(pathlib.PurePath(parent,"vocals.wav"))+" "+str(output_name))
		os.system("cp "+str(pathlib.PurePath(parent,"vocals.wav"))+" "+str(output_name))
		# os.system("cp "+str(pathlib.PurePath(parent,file.name))+" "+str(output_name))
		i+=1

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
		# separate music into 20 sec
		for start in range(0, length, 20):
			output_file = str(pathlib.PurePath(args.output, file.stem+"_"+str(start)+".wav"))
			os.system("ffmpeg -i "+input_file+" -ss "+str(start)+" -to "+str(start+20 if start+20 < length else length)+" -c copy "+output_file)
		i+=1



if __name__ == '__main__':
	main(command())