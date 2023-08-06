import numpy as np
import os
import math
from .database import *
from .full_model import generate_full
from .utils import *
from .mfp2DSym import *
from .mfp import *
from .rta2DSym import *
import deepdish as dd
from mpi4py import MPI

comm = MPI.COMM_WORLD

class Material(object):


 def __init__(self,**argv):

  if comm.rank == 0:  
   
   save = True   
   model = argv['model']
   if comm.rank == 0:
    if   model == 'unlisted':
      download_file(argv['file_id'],'material.h5')
      save = False

    elif model == 'database':
      download_file(db['entry_name'],'material.h5')
      save = False

    elif model == 'full':
      data = generate_full(**argv)

    elif model == 'mfp2DSym':
      data = generate_mfp2DSym(**argv)

    elif model == 'mfp':
      data = generate_mfp(**argv)

    elif model == 'rta2DSym':
      data = generate_rta2DSym(**argv)

    elif model == 'mfp_ms':
      data = generate_mfp_ms(**argv)

   if save:
      #np.save('material',data)
      dd.io.save('material.h5',data)

