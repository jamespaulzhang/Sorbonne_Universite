#!/usr/local/bin/python

import math
import numpy as np
from regression_labs.batch import Batch

class LatentFunction:
    def __init__(self):
        self.c0 = np.random.random()*2
        self.c1 = -np.random.random()*4
        self.c2 = -np.random.random()*4
        self.c3 = np.random.random()*4
    
    def get_batch(self, size:int) -> Batch:
        batch = Batch(size)
        x = np.zeros(1)
        for _ in range(size):
            x[0] = np.random.random()
            y = self.get_noisy_value(x)
            batch.add_sample(x, y)
        return batch
    
    def get_noisy_value(self, x):
        """
        Generate a noisy nonlinear data sample from a given data point in the range [0,1]
        :param x: A scalar dependent variable for which to calculate the output y_noisy
        :returns: The output with Gaussian noise added
        """
        y = self.get_value(x)
        noise = self.sigma * np.random.random()
        y_noisy = y + noise
        return y_noisy


class LinearLatentFunction(LatentFunction):

    def __init__(self):
        super().__init__()
        self.sigma = 0.5

    def get_value(self, x):
        """
        The function is one dimensional, this is a specific case, so we always use x[0]
        """
        return self.c3 * x[0] + self.c1

    
class NonLinearLatentFunction(LatentFunction):

    def __init__(self):
        super().__init__()
        self.sigma = 0.1

    def get_value(self, x):
        """
        The function is one dimensional, this is a specific case, so we always use x[0]
        """
        return self.c0 - x[0] - math.sin(self.c1 * math.pi * x[0] ** 3) * math.cos(self.c2 * math.pi * x[0] ** 3) * math.exp(-x[0] ** 4)

    
class NonLinearLatentXDFunction(LatentFunction):

    def __init__(self, dim: int):
        super().__init__()
        self.dim = dim
        self.sigma = 0.1
    
    def get_batch(self, size:int) -> Batch:
        batch = Batch(size, self.dim)
        x = np.zeros(self.dim)
        for _ in range(size):
            for j in range(self.dim):
                x[j] = np.random.random()
            y = self.get_noisy_value(x)
            batch.add_sample(x, y)
        return batch

    def get_value(self, x):
        """
        The function is one dimensional, this is a specific case, so we always use x[0]
        """
        val = self.c0
        for j in range(self.dim):
            val = val - x[j] - math.sin(self.c1 * math.pi * x[j] ** 3) * math.cos(self.c2 * math.pi * x[j] ** 3) * math.exp(-x[j] ** 4)
        return  val
