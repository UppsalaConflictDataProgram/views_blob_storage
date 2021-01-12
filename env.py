import os

from environs import Env

env = Env()
env.read_env()

def envpath(path_name,default,base_default = None):
    if base_default is None:
        base_default = os.path.join(env("HOME"),"bstore")

    return os.path.join(env("BASE",base_default),env(path_name,default))
