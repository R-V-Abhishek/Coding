import numpy as np

# --- Functions ---
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    # Note: Assumes x is the output of the sigmoid function
    return x * (1 - x)

# --- Data ---
inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
expected_output = np.array([[0], [1], [1], [0]])

# --- Network Architecture ---
inputLayerNeurons, hiddenLayerNeurons, outputLayerNeurons = 2, 2, 1

# --- Initial Weights and Biases (Corrected) ---
hidden_weights = np.random.uniform(size=(inputLayerNeurons, hiddenLayerNeurons))
hidden_bias = np.random.uniform(size=(1, hiddenLayerNeurons))
output_weights = np.random.uniform(size=(hiddenLayerNeurons, outputLayerNeurons))
output_bias = np.random.uniform(size=(1, outputLayerNeurons)) # CORRECTED

# --- Training Parameters ---
lr = 0.1
epochs = 10000

# --- Training Loop (Corrected) ---
for _ in range(epochs):
    # 1. FORWARD PASS
    hidden_layer_activation = np.dot(inputs, hidden_weights) + hidden_bias
    hidden_layer_output = sigmoid(hidden_layer_activation)
    
    output_layer_activation = np.dot(hidden_layer_output, output_weights) + output_bias
    predicted_output = sigmoid(output_layer_activation)
    
    # 2. BACKPROPAGATION
    # Phase 1: Compute error and gradient at the output layer
    error = expected_output - predicted_output
    d_predicted_output = error * sigmoid_derivative(predicted_output)
    
    # Phase 2: Propagate error to the hidden layer
    error_hidden_layer = d_predicted_output.dot(output_weights.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output) # CORRECTED
    
    # 3. UPDATE WEIGHTS AND BIASES (Corrected)
    # Note: Using '+=' here because error was calculated as (expected - predicted).
    # Standard gradient descent uses (predicted - expected) and '-='. The result is the same.
    output_weights += hidden_layer_output.T.dot(d_predicted_output) * lr
    output_bias += np.sum(d_predicted_output, axis=0, keepdims=True) * lr
    hidden_weights += inputs.T.dot(d_hidden_layer) * lr
    hidden_bias += np.sum(d_hidden_layer, axis=0, keepdims=True) * lr

print("Final Predicted Output after training:")
print(predicted_output)