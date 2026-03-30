"""
Comparative Study of Regression Methods
Authors: Yuxiang ZHANG, Kenan Alsafadi
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import math
from typing import Tuple, List, Dict
from scipy import stats
import torch as th
from torch import nn
from torch.utils.data import Dataset, DataLoader
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PROVIDED CLASSES (from the assignment)
# ============================================================================

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

    def get_range(self):
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
        minibatch = Batch(size, self.dim)
        for _ in range(size):
            x, y = self.get_random_sample()
            minibatch.add_sample(x, y)
        return minibatch

def horiz_to_verti(vec):
    return np.atleast_2d(vec).transpose()

def verti_to_horiz(vec):
    return vec.transpose()[0]

class Gaussians:
    def __init__(self, nb_features):
        self.nb_features = nb_features
        self.centers = np.linspace(0.0, 1.0, self.nb_features)
        width_constant = 0.1 / self.nb_features
        self.sigma = np.ones(self.nb_features) * width_constant

    def phi_output(self, x):
        dim_x = np.shape(x)[0]
        input_mat = np.array([verti_to_horiz(x),] * self.nb_features)
        centers_mat = np.array([self.centers,] * dim_x).transpose()
        widths_mat = np.array([self.sigma,] * dim_x).transpose()
        phi = np.exp(-np.divide(np.square(input_mat - centers_mat), widths_mat))
        return phi

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
        y = self.get_value(x)
        noise = self.sigma * np.random.random()
        y_noisy = y + noise
        return y_noisy

class NonLinearLatentFunction(LatentFunction):
    def __init__(self, sigma=0.1):
        super().__init__()
        self.sigma = sigma

    def get_value(self, x):
        return self.c0 - x[0] - math.sin(self.c1 * math.pi * x[0] ** 3) * math.cos(self.c2 * math.pi * x[0] ** 3) * math.exp(-x[0] ** 4)

# ============================================================================
# REGRESSION METHODS
# ============================================================================

# --------------------------
# RBFN Implementation
# --------------------------
class RBFN(Gaussians):
    def __init__(self, nb_features):
        super().__init__(nb_features)
        self.theta = np.zeros(self.nb_features)

    def f(self, x):
        phi = self.phi_output(x)
        return np.dot(phi.T, self.theta)

    def compute_error(self, x_data, y_data):
        return np.sqrt(np.mean((y_data - self.f(x_data))**2))

    def train_batch(self, x_data, y_data):
        """Batch training using least squares"""
        G = self.phi_output(x_data).T
        self.theta = np.linalg.pinv(G.T @ G) @ G.T @ y_data
        return self.theta

# --------------------------
# LWR Implementation
# --------------------------
def bar_design(x):
    return np.hstack((x, np.ones((x.shape[0], 1))))

class LWR(Gaussians):
    def __init__(self, nb_features):
        super().__init__(nb_features)
        self.theta = np.zeros((2, self.nb_features))

    def f(self, x):
        wval = bar_design(x)
        phi = self.phi_output(x)
        linear_model = np.dot(wval, self.theta)
        val = np.dot(linear_model, phi)
        numerator = np.sum(val, axis=1)
        return numerator / np.sum(phi, axis=0)

    def compute_error(self, x_data, y_data):
        return np.sqrt(np.mean((y_data - self.f(x_data))**2))

    def train(self, x_data, y_data):
        for k in range(self.nb_features):
            A = np.zeros((2, 2))
            b = np.zeros((2, 1))
            
            for i in range(x_data.shape[0]):
                x_i = x_data[i].reshape(1, x_data.shape[1])
                y_i = y_data[i]
                phi_k = self.phi_output(x_i)[k]
                x_bar = bar_design(x_i)
                A += phi_k * (x_bar.T @ x_bar)
                b += phi_k * (x_bar.T * y_i)
            
            result = np.dot(np.linalg.pinv(A), b)
            for i in range(2):
                self.theta[i, k] = result[i, 0]

# --------------------------
# Neural Network Implementation
# --------------------------
class NeuralNetwork(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=10, output_dim=1, n_layers=3, lr=0.001):
        super().__init__()
        self.layers = nn.ModuleList()
        
        # Input layer
        self.layers.append(nn.Linear(input_dim, hidden_dim))
        
        # Hidden layers
        for _ in range(n_layers - 1):
            self.layers.append(nn.Linear(hidden_dim, hidden_dim))
            
        # Output layer
        self.layers.append(nn.Linear(hidden_dim, output_dim))
        
        self.activation = nn.ReLU()
        self.optimizer = th.optim.Adam(self.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()
    
    def forward(self, x):
        for i, layer in enumerate(self.layers[:-1]):
            x = self.activation(layer(x))
        return self.layers[-1](x)
    
    def compute_error(self, x_data, y_data):
        x_tensor = th.FloatTensor(x_data)
        y_tensor = th.FloatTensor(y_data)
        with th.no_grad():
            predictions = self.forward(x_tensor).squeeze()
            return th.sqrt(self.loss_fn(predictions, y_tensor)).item()

class RegressionDataset(Dataset):
    def __init__(self, x_data, y_data):
        self.x_data = th.FloatTensor(x_data)
        self.y_data = th.FloatTensor(y_data)
    
    def __len__(self):
        return len(self.x_data)
    
    def __getitem__(self, idx):
        return self.x_data[idx], self.y_data[idx]

def train_neural_network(model, train_loader, epochs=1000):
    start_time = time.time()
    train_losses = []
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch_x, batch_y in train_loader:
            model.optimizer.zero_grad()
            predictions = model(batch_x).squeeze()
            loss = model.loss_fn(predictions, batch_y)
            loss.backward()
            model.optimizer.step()
            epoch_loss += loss.item()
        
        train_losses.append(epoch_loss / len(train_loader))
        
    training_time = time.time() - start_time
    return model, train_losses, training_time

# ============================================================================
# EXPERIMENTAL SETUP
# ============================================================================

def generate_datasets(sizes=[100, 1000, 5000], noises=[0.01, 0.1, 0.5]):
    """Generate datasets with different sizes and noise levels"""
    datasets = {}
    for size in sizes:
        for noise in noises:
            key = f"size_{size}_noise_{noise}"
            lf = NonLinearLatentFunction(sigma=noise)
            batch = lf.get_batch(size)
            datasets[key] = {
                'x': batch.x_data,
                'y': batch.y_data,
                'size': size,
                'noise': noise
            }
    return datasets

def split_dataset(x, y, train_ratio=0.7):
    """Split dataset into training and testing sets"""
    n_samples = len(x)
    indices = np.random.permutation(n_samples)
    split_idx = int(n_samples * train_ratio)
    
    train_idx = indices[:split_idx]
    test_idx = indices[split_idx:]
    
    x_train, y_train = x[train_idx], y[train_idx]
    x_test, y_test = x[test_idx], y[test_idx]
    
    return x_train, y_train, x_test, y_test

def evaluate_method(method_name, x_train, y_train, x_test, y_test, 
                    hyperparams=None):
    """Evaluate a regression method with given hyperparameters"""
    
    if method_name == "RBFN":
        # Hyperparameter: number of features
        n_features = hyperparams.get('n_features', 20)
        
        start_time = time.time()
        model = RBFN(nb_features=n_features)
        model.train_batch(x_train, y_train)
        train_time = time.time() - start_time
        
        test_error = model.compute_error(x_test, y_test)
    
    elif method_name == "LWR":
        # Hyperparameter: number of features
        n_features = hyperparams.get('n_features', 20)
        
        start_time = time.time()
        model = LWR(nb_features=n_features)
        model.train(x_train, y_train)
        train_time = time.time() - start_time
        
        test_error = model.compute_error(x_test, y_test)
    
    elif method_name == "NeuralNetwork":
        # Hyperparameters
        hidden_dim = hyperparams.get('hidden_dim', 20)
        n_layers = hyperparams.get('n_layers', 3)
        lr = hyperparams.get('lr', 0.001)
        epochs = hyperparams.get('epochs', 1000)
        batch_size = hyperparams.get('batch_size', 32)
        
        # Prepare data
        train_dataset = RegressionDataset(x_train, y_train)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        # Create and train model
        model = NeuralNetwork(hidden_dim=hidden_dim, n_layers=n_layers, lr=lr)
        model, train_losses, train_time = train_neural_network(
            model, train_loader, epochs=epochs
        )
        
        test_error = model.compute_error(x_test, y_test)
    
    else:
        raise ValueError(f"Unknown method: {method_name}")
    
    return {
        'test_error': test_error,
        'train_time': train_time,
        'hyperparams': hyperparams
    }

def hyperparameter_tuning(method_name, x_train, y_train, x_val, y_val, 
                         param_grid, n_trials=5):
    """Perform hyperparameter tuning using random search"""
    best_error = float('inf')
    best_params = None
    
    param_names = list(param_grid.keys())
    
    for trial in range(n_trials):
        # Sample random hyperparameters
        params = {}
        for name in param_names:
            if isinstance(param_grid[name][0], int):
                params[name] = np.random.randint(param_grid[name][0], param_grid[name][1])
            else:
                params[name] = np.random.uniform(param_grid[name][0], param_grid[name][1])
        
        # Evaluate
        result = evaluate_method(method_name, x_train, y_train, x_val, y_val, params)
        
        if result['test_error'] < best_error:
            best_error = result['test_error']
            best_params = params
    
    return best_params, best_error

def run_experiment(datasets, methods, n_repeats=5):
    """Run the main experiment"""
    results = {}
    
    for dataset_key, dataset in datasets.items():
        size = dataset['size']
        noise = dataset['noise']
        x = dataset['x']
        y = dataset['y']
        
        results[dataset_key] = {}
        
        for method_name in methods:
            print(f"Processing {dataset_key} with {method_name}...")
            
            # Define hyperparameter grids for each method
            if method_name == "RBFN":
                param_grid = {'n_features': [5, 100]}
            elif method_name == "LWR":
                param_grid = {'n_features': [5, 100]}
            elif method_name == "NeuralNetwork":
                param_grid = {
                    'hidden_dim': [5, 100],
                    'n_layers': [1, 3],
                    'lr': [0.0001, 0.01],
                    'epochs': [500, 2000],
                    'batch_size': [16, 128]
                }
            
            # Storage for repeated experiments
            errors = []
            times = []
            all_params = []
            
            for repeat in range(n_repeats):
                # Split data
                x_train, y_train, x_test, y_test = split_dataset(x, y)
                # Further split training data for validation
                x_train_sub, y_train_sub, x_val, y_val = split_dataset(
                    x_train, y_train, train_ratio=0.8
                )
                
                # Hyperparameter tuning
                best_params, _ = hyperparameter_tuning(
                    method_name, x_train_sub, y_train_sub, x_val, y_val,
                    param_grid, n_trials=3
                )
                
                # Final evaluation with best parameters
                result = evaluate_method(
                    method_name, x_train, y_train, x_test, y_test, best_params
                )
                
                errors.append(result['test_error'])
                times.append(result['train_time'])
                all_params.append(best_params)
            
            # Store results
            results[dataset_key][method_name] = {
                'errors_mean': np.mean(errors),
                'errors_std': np.std(errors),
                'times_mean': np.mean(times),
                'times_std': np.std(times),
                'best_params': all_params[np.argmin(errors)]
            }
    
    return results

def plot_results(results, datasets):
    """Create visualization plots"""
    
    # Extract sizes and noises
    sizes = sorted(set([dataset['size'] for dataset in datasets.values()]))
    noises = sorted(set([dataset['noise'] for dataset in datasets.values()]))
    
    # 1. Error vs Noise level for different sizes
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, size in enumerate(sizes):
        ax = axes[idx]
        for method in ['RBFN', 'LWR', 'NeuralNetwork']:
            errors = []
            error_stds = []
            for noise in noises:
                key = f"size_{size}_noise_{noise}"
                if key in results and method in results[key]:
                    errors.append(results[key][method]['errors_mean'])
                    error_stds.append(results[key][method]['errors_std'])
            
            ax.errorbar(noises, errors, yerr=error_stds, marker='o', 
                       label=method, capsize=5)
        
        ax.set_xlabel('Noise Level')
        ax.set_ylabel('RMSE')
        ax.set_title(f'Dataset Size: {size}')
        ax.set_xscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Error vs Noise Level for Different Dataset Sizes')
    plt.tight_layout()
    plt.savefig('error_vs_noise.pdf', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Training Time vs Dataset Size for different noise levels
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, noise in enumerate(noises):
        ax = axes[idx]
        for method in ['RBFN', 'LWR', 'NeuralNetwork']:
            times = []
            time_stds = []
            for size in sizes:
                key = f"size_{size}_noise_{noise}"
                if key in results and method in results[key]:
                    times.append(results[key][method]['times_mean'])
                    time_stds.append(results[key][method]['times_std'])
            
            ax.errorbar(sizes, times, yerr=time_stds, marker='s', 
                       label=method, capsize=5)
        
        ax.set_xlabel('Dataset Size')
        ax.set_ylabel('Training Time (s)')
        ax.set_title(f'Noise Level: {noise}')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Training Time vs Dataset Size for Different Noise Levels')
    plt.tight_layout()
    plt.savefig('time_vs_size.pdf', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Error vs Training Time (scatter plot)
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    
    sizes = sorted(set([dataset['size'] for dataset in datasets.values()]))
    noises = sorted(set([dataset['noise'] for dataset in datasets.values()]))
    
    markers = {'RBFN': 'o', 'LWR': 's', 'NeuralNetwork': '^'}
    colors = {'RBFN': 'blue', 'LWR': 'green', 'NeuralNetwork': 'red'}
    
    for i, size in enumerate(sizes):
        for j, noise in enumerate(noises):
            ax = axes[i, j]
            key = f"size_{size}_noise_{noise}"
            
            if key in results:
                method_data = []
                
                for method in ['RBFN', 'LWR', 'NeuralNetwork']:
                    if method in results[key]:
                        result = results[key][method]
                        method_data.append({
                            'method': method,
                            'time': result['times_mean'],
                            'error': result['errors_mean'],
                            'time_std': result['times_std'],
                            'error_std': result['errors_std'],
                            'marker': markers[method],
                            'color': colors[method]
                        })
                
                for data in method_data:
                    ax.errorbar(data['time'], data['error'],
                               xerr=data['time_std'], yerr=data['error_std'],
                               fmt=data['marker'], color=data['color'],
                               capsize=4, markersize=8, alpha=0.8,
                               label=data['method'] if j == 0 else "")
                
                for data in method_data:
                    ax.annotate(f"{data['time']:.3f}s\n{data['error']:.4f}",
                               xy=(data['time'], data['error']),
                               xytext=(5, 5), textcoords='offset points',
                               fontsize=7, bbox=dict(boxstyle="round,pad=0.3",
                                                    facecolor='white',
                                                    edgecolor='gray',
                                                    alpha=0.7))
                
                ax.set_xscale('log')
                ax.set_xlabel('Training Time (s)')
                ax.set_ylabel('RMSE')
                ax.set_title(f'Size: {size}, Noise: {noise}')
                ax.grid(True, alpha=0.3, linestyle='--')
    
    for i in range(3):
        axes[i, 0].set_ylabel('RMSE', fontsize=10)

    for j in range(3):
        axes[2, j].set_xlabel('Training Time (s)', fontsize=10)
    
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', 
               bbox_to_anchor=(0.5, 1.02), ncol=3, fontsize=11)
    
    plt.suptitle('Error vs Training Time by Dataset Size and Noise Level', 
                 fontsize=14, y=1.05)
    plt.tight_layout()
    plt.savefig('improved_error_vs_time.pdf', dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_table(results, datasets):
    """Create a summary table of results"""
    print("\n" + "="*80)
    print("SUMMARY OF RESULTS")
    print("="*80)
    
    headers = ["Dataset", "Method", "RMSE (mean±std)", "Time (s, mean±std)", "Best Params"]
    row_format = "{:<20} {:<15} {:<20} {:<25} {:<30}"
    
    print(row_format.format(*headers))
    print("-"*110)
    
    for dataset_key in sorted(results.keys()):
        dataset_info = datasets[dataset_key]
        for method in ['RBFN', 'LWR', 'NeuralNetwork']:
            if method in results[dataset_key]:
                res = results[dataset_key][method]
                rmse_str = f"{res['errors_mean']:.4f}±{res['errors_std']:.4f}"
                time_str = f"{res['times_mean']:.3f}±{res['times_std']:.3f}"
                
                # Format parameters
                params_str = ""
                if method == "RBFN":
                    params_str = f"n_features={res['best_params']['n_features']}"
                elif method == "LWR":
                    params_str = f"n_features={res['best_params']['n_features']}"
                elif method == "NeuralNetwork":
                    params = res['best_params']
                    params_str = f"h={params['hidden_dim']}, l={params['n_layers']}, lr={params['lr']:.4f}"
                
                print(row_format.format(
                    dataset_key, method, rmse_str, time_str, params_str
                ))
    
    print("="*110)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    # Set random seeds for reproducibility
    np.random.seed(42)
    th.manual_seed(42)
    
    # 1. Generate datasets
    print("Generating datasets...")
    datasets = generate_datasets(
        sizes=[100, 1000, 5000],
        noises=[0.01, 0.1, 0.5]
    )
    
    # 2. Define methods to compare
    methods = ['RBFN', 'LWR', 'NeuralNetwork']
    
    # 3. Run experiments
    print("\nRunning experiments...")
    results = run_experiment(datasets, methods, n_repeats=3)
    
    # 4. Create visualizations
    print("\nCreating visualizations...")
    plot_results(results, datasets)
    
    # 5. Print summary table
    create_summary_table(results, datasets)
    
    # 6. Save results to file
    import json
    
    # Convert results to JSON-serializable format
    results_serializable = {}
    for dataset_key in results:
        results_serializable[dataset_key] = {}
        for method in results[dataset_key]:
            results_serializable[dataset_key][method] = {
                'errors_mean': float(results[dataset_key][method]['errors_mean']),
                'errors_std': float(results[dataset_key][method]['errors_std']),
                'times_mean': float(results[dataset_key][method]['times_mean']),
                'times_std': float(results[dataset_key][method]['times_std']),
                'best_params': {k: (float(v) if isinstance(v, (np.float32, np.float64)) else v) 
                              for k, v in results[dataset_key][method]['best_params'].items()}
            }
    
    with open('regression_results.json', 'w') as f:
        json.dump(results_serializable, f, indent=2)
    
    print("\nResults saved to 'regression_results.json'")
    print("\nExperiment completed successfully!")

if __name__ == "__main__":
    main()