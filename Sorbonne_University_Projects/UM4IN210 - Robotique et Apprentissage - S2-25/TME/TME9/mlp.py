import numpy as np


class MLP:
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size, learning_rate=0.01):
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size1) * 0.01
        self.b1 = np.zeros((1, hidden_size1))

        self.W2 = np.random.randn(hidden_size1, hidden_size2) * 0.01
        self.b2 = np.zeros((1, hidden_size2))

        self.W3 = np.random.randn(hidden_size2, output_size) * 0.01
        self.b3 = np.zeros((1, output_size))

        self.learning_rate = learning_rate

    def relu(self, Z):
        return np.maximum(0, Z)

    def relu_derivative(self, Z):
        return (Z > 0).astype(float)

    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))

    def sigmoid_derivative(self, Z):
        return self.sigmoid(Z) * (1 - self.sigmoid(Z))

    def forward(self, X):
        # Forward pass
        self.Z1 = X @ self.W1 + self.b1
        self.A1 = self.sigmoid(self.Z1)

        self.Z2 = self.A1 @ self.W2 + self.b2
        self.A2 = self.sigmoid(self.Z2)

        # Output layer (linear activation)
        self.Z3 = self.A2 @ self.W3 + self.b3

        return self.Z3  # No activation (linear output for regression)

    def compute_loss(self, Y_pred, Y_true):
        # Mean Squared Error (MSE)
        return np.mean((Y_pred - Y_true) ** 2)

    def backward(self, X, Y_true, Y_pred):
        m = X.shape[0]  # Number of samples

        # Compute gradients
        dL_dY = (2 / m) * (Y_pred - Y_true)  # dL/dY_pred

        dL_dW3 = self.A2.T @ dL_dY
        dL_db3 = np.sum(dL_dY, axis=0, keepdims=True)

        dL_dA2 = dL_dY @ self.W3.T
        dL_dZ2 = dL_dA2 * self.sigmoid_derivative(self.Z2)
        dL_dW2 = self.A1.T @ dL_dZ2
        dL_db2 = np.sum(dL_dZ2, axis=0, keepdims=True)

        dL_dA1 = dL_dZ2 @ self.W2.T
        dL_dZ1 = dL_dA1 * self.sigmoid_derivative(self.Z1)
        dL_dW1 = X.T @ dL_dZ1
        dL_db1 = np.sum(dL_dZ1, axis=0, keepdims=True)

        # Update weights and biases
        self.W1 -= self.learning_rate * dL_dW1
        self.b1 -= self.learning_rate * dL_db1
        self.W2 -= self.learning_rate * dL_dW2
        self.b2 -= self.learning_rate * dL_db2
        self.W3 -= self.learning_rate * dL_dW3
        self.b3 -= self.learning_rate * dL_db3

    def train(self, X, Y, epochs=1000, verbose=True):
        for epoch in range(epochs):
            Y_pred = self.forward(X)
            loss = self.compute_loss(Y_pred, Y)
            self.backward(X, Y, Y_pred)

            if epoch % 100 == 0 and verbose:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
