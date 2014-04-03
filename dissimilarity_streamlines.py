"""
Experiments of the paper 'The Approximation of the Dissimilarity
Projection' accepted at PRNI2012.

Quantification of the dissimilarity approximation of tractography data
across different prototype selection policies and number of prototypes.

Copyright (c) 2012, Emanuele Olivetti

Distributed under the New BSD license (3-clauses)
"""

import numpy as np
import nibabel as nib
from dipy.tracking.distances import bundles_distances_mam
from dipy.io.dpy import Dpy
from dissimilarity_common import *

if __name__ == '__main__':

    np.random.seed(0)

    prototype_policies = ['random', 'sff','fft']
    color_policies = ['ko--', 'k^-','kx:']
    
    num_prototypes = [3, 5, 10, 15, 20, 25, 30, 35, 40,45,50]
    
    iterations = 50
    
    streams,hdr=nib.trackvis.read('/home/nusrat/dataset_trackvis/101.trk')
    tracks = np.array([s[0] for s in streams], dtype=np.object)
    print "Loading tracks."

    
    rho = compute_correlation(tracks, bundles_distances_mam, prototype_policies, num_prototypes, iterations)
    plot_results(rho, num_prototypes, prototype_policies, color_policies)
