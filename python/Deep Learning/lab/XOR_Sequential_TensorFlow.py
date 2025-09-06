import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

print("XOR Problem - TensorFlow Sequential API")
print("="*50)

# --- Data ---
inputs = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=np.float32)
expected_output = np.array([[0], [1], [1], [0]], dtype=np.float32)

print("Input data:")
print(inputs)
print("\nExpected output:")
print(expected_output)

# --- Build the Sequential Model ---
model = tf.keras.Sequential([
    tf.keras.layers.Dense(2, activation='sigmoid', input_shape=(2,), name='hidden_layer'),
    tf.keras.layers.Dense(1, activation='sigmoid', name='output_layer')
])

# --- Compile the Model ---
model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.5),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# --- Display Model Architecture ---
print("\nModel Architecture:")
model.summary()

# --- Train the Model ---
print("\nTraining the model...")
history = model.fit(
    inputs, expected_output,
    epochs=1000,
    verbose=1,  # Show training progress
    batch_size=4
)

# --- Make Predictions ---
predictions = model.predict(inputs)
print(f"\nFinal Predictions:")
print("Input -> Predicted | Expected | Correct?")
print("-" * 40)
for i in range(len(inputs)):
    pred_val = predictions[i][0]
    expected_val = expected_output[i][0]
    is_correct = "✓" if abs(pred_val - expected_val) < 0.5 else "✗"
    print(f"{inputs[i]} -> {pred_val:.4f} | {expected_val:.1f} | {is_correct}")

