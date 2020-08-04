import numpy
import pickle
import typing

data: typing.Dict[str, typing.Any] = numpy.load("03output1/music0001_0.npy", allow_pickle=True).item()

print(data['mfcc'])
print(type(data['mfcc']))
print(data['mfcc'].shape)
print(data['f0'].shape)