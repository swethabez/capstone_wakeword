import tensorflow as tf
from tensorflow.python.platform import build_info as build
print(f"tensorflow version: {tf.__version__}")
print(f"Cuda Version: {build.build_info['cuda_version']}")
print(f"Cudnn version: {build.build_info['cudnn_version']}")