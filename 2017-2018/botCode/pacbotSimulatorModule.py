#!/usr/bin/env python3

import os
import robomodules as rm
from messages import *

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

class pacbotSimulatorModule(rm.protoModule):
    
