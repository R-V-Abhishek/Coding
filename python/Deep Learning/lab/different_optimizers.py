from tensorflow.keras import layers, models, optimizers
import numpy as np
import matplotlib.pyplot as plt
# I. Create synthetic data
def create_data():
    X = np.random.randn(1000, 10)  # 1000 samples, 10 features
    y = np.random.randn(1000, 1)    # 1000 samples, 1 target (regression task)
    return X, y
# 2. Define a simple deep neural network
def create_model():
    model = models.Sequential([
        layers.Dense(50, activation='relu', input_shape=(10,)),
        layers.Dense(20, activation='relu'),
        layers.Dense(1)
    ])
    return model

def train_model_with_history(model, X, y, optimizer, batch_size, epochs, optimizer_name):
    model.compile(optimizer=optimizer, loss='mse')
    history = []
    for epoch in range(epochs):
        hist = model.fit(X, y, batch_size=batch_size, epochs=1, verbose=0)
        history.append(hist.history['loss'][0])
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {hist.history['loss'][0]:.4f}")

    return history

# 4. Compare performance of SGD and Adam
# Load data
X, y = create_data()
# Create models for SGD and Adam
model_sgd = create_model()
model_adam = create_model()
# Optimizers
optimizer_sgd = optimizers.SGD(learning_rate=0.01)  # SGD optimizer
optimizer_adam = optimizers.Adam(learning_rate=0.001)  # Adam optimizer
# Set training parameters
epochs = 50
batch_size = 32
# Train models and capture loss history, while printing epoch iterations
print( "\nTraining with SGD Optimizer:")
sgd_loss = train_model_with_history(model_sgd, X, y, optimizer_sgd, batch_size, epochs, 'SGD')
print( "\nTraining with Adam Optimizer:")
adam_loss = train_model_with_history(model_adam, X, y, optimizer_adam, batch_size, epochs, 'Adam')

# Plot loss curves
plt.plot(range(1, epochs + 1), sgd_loss, label='SGD', color='blue')
plt.plot(range(1, epochs + 1), adam_loss, label='Adam', color='orange')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('SGD vs Adam Optimizer: Loss Comparison')
plt.legend()
plt.grid(True)
plt.show()