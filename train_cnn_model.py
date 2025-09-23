import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load sample data (simulate healthy vs diseased)
dataset_url = "https://storage.googleapis.com/laurencemoroney-blog.appspot.com/horses-or-humans.zip"
data_dir = tf.keras.utils.get_file('horse-or-human', origin=dataset_url, extract=True)

# Setup image data generator
train_dir = data_dir.replace("horse-or-human.zip", "horse-or-human")
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    class_mode='binary'
)

# Create a simple CNN model
model = Sequential([
    Conv2D(16, (3,3), activation='relu', input_shape=(150,150,3)),
    MaxPooling2D(2,2),
    Conv2D(32, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile and train
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_generator, epochs=3)

# Save the model
model.save("crop_disease_model.h5")
print("✅ Model trained and saved as crop_disease_model.h5")