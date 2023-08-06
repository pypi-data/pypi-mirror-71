﻿Digital lock-in analysis
---------------------------------------------

Perform digital lock-in analysis


Installing this package
-----------------------

Use `pip` to install it by:

.. code-block:: console

    $ pip install pyLIA


Simple examples
---------------

Here is a simple example on how to use the code:

.. code-block:: python

	import pyLIA
	import numpy as np
	import matplotlib.pyplot as plt

	data = np.load('camera.npy') ## Thermal acquisition
	sampling_freq = 400  ## Sampling freqency of the thermal video [Hz]
	load_freq = 55  ## Load freqency of the excitation test [Hz]

	mag, ph = pyLIA.LIA(data,sampling_freq,load_freq)

	plt.figure()
	plt.imshow(mag)
	cbar = plt.colorbar()
	cbar.set_label('[unit]')

	plt.figure()
	plt.imshow(ph)
	cbar = plt.colorbar()
	cbar.set_label('[deg]')
    


Reference:
<https://www.sciencedirect.com/science/article/pii/S0142112320301924>
