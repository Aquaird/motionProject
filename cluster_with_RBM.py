import numpy as np
import matplotlib.pyplot as plt
from tfrbm import BBRBM, GBRBM

from tensorflow.examples.tutorials.mnist import input_data



gbrbm = GBRBM(n_visible=240, n_hidden=16, learning_rate=0.01, momentum=0.95, tqdm='notebook')
errs = bbrbm.fit(mnist_images, n_epoches=30, batch_size=10)
plt.plot(errs)
plt.show()

