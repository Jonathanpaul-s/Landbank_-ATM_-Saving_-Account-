import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Generate dummy data (replace this with your real data later)
num_classes = 2
image_shape = (32, 32, 3)
num_samples = 100

X_train = np.random.rand(num_samples, *image_shape)
y_train = np.random.randint(0, num_classes, num_samples)

# Build model
model = keras.Sequential([
    layers.Input(shape=image_shape),
    layers.Conv2D(16, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=5, batch_size=8)

# Save the trained model
model.save("crop_disease_detector.h5")

print("✅ Model trained and saved successfully.")