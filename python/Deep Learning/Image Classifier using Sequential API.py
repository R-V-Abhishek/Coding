import tensorflow as tf
import matplotlib.pyplot as plt

fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

print(train_labels)

# Class names for Fashion MNIST
class_names = ['T-Shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

plt.figure(figsize=(10,10))

for i in range(10):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i])
    plt.xlabel(class_names[train_labels[i]])

plt.tight_layout()
plt.show()

print(train_images.shape)
print(train_labels.shape)
print(test_images.shape) 
print(test_labels.shape)   

# Create a validation set (10,000 samples from training data)
val_images = train_images[-10000:]
val_labels = train_labels[-10000:]
train_images2 = train_images[:-10000]
train_labels2 = train_labels[:-10000]

# Normalize pixel values
train_images2 = train_images2 / 255.0
val_images = val_images / 255.0
test_images = test_images / 255.0

# Build a Sequential model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

print(model.summary())
print(model.layers)

hidden1=model.layers[1]
print(hidden1.name)

weights, biases = hidden1.get_weights()
print(weights)
print(biases)
print(biases.shape)

# Compile the model
model.compile(optimizer='sgd',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
)

history = model.fit(train_images2, train_labels2, epochs = 30, 
                    validation_data = (val_images, val_labels)
 )

import matplotlib.pyplot as plt
import pandas as pd

pd.DataFrame(history.history).plot(figsize = (8,5))
plt.grid(True)
plt.gca().set_ylim(0,1)
plt.show
