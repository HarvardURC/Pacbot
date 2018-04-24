from distutils.core import setup
from distutils.extension import Extension
setup(name = 'Encoder', version = '1.0',  ext_modules = [Extension('Encoder',libraries = ['pigpio', 'stdio', 'stdlib'], ['encoder.c'])])