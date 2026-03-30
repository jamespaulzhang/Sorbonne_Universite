import numpy as np
from typing import Tuple


class Batch:
    def __init__(self, size:int, dim:int=1):
        self.x_data = np.zeros((size, dim))
        self.y_data = np.zeros(size)
        self.current = 0
        self.size = size
        self.dim = dim

    def add_sample(self, x, y) -> None:
        self.x_data[self.current] = x
        self.y_data[self.current] = y
        self.current = self.current + 1

    def get_random_sample(self) -> Tuple[np.array, float]:
        index = np.random.randint(self.size)
        return self.x_data[index].reshape(1, self.x_data.shape[1]), self.y_data[index]

    """ Dangerous to use, needs to reinitialize current
    def has_next(self) -> bool:
        return self.current < self.size

    def get_next(self) -> Tuple[np.array, float]:
        x, y = self.x_data[self.current], self.y_data[self.current]
        self.current = self.current + 1
        return x, y
    """
    
    def get_range(self):
        """
        Return the range of y values in the batch
        """
        my_min = np.infty
        my_max = -np.infty
        for i in range(self.size):
            y = self.y_data[i]
            if y > my_max:
                my_max = y
            if y < my_min:
                my_min = y
        return my_min, my_max
    
    def get_minibatch(self, size):
        """
        Return a minibatch of size elements randomly drawn from the batch
        The same element can be drawn several times
        """
        minibatch = Batch(size, self.dim)
        for _ in range(size):
            x, y = self.get_random_sample()
            minibatch.add_sample(x, y)
        return minibatch
            

