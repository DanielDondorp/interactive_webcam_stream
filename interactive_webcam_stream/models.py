import numpy as np
import tensorflow
from tensorflow import keras
import glob, tqdm
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from skimage import io

class ModelTrainer:
    def __init__(self):
        X_train, X_test, y_train, y_test, le = self.create_dataset()
        model = self.create_model(len(le.classes_))
        model.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 10)
        model.save("model_home")
        classes = le.classes_
        np.save("classes.npy", classes)

    def create_dataset(self, path_to_data = "./data"):
        images = glob.glob(f"{path_to_data}/**/*.jpg")
        X = []
        y = []
        for image in tqdm.tqdm(images):
            im = io.imread(image)
            label = image.split("/")[-2]
            X.append(im)
            y.append(label)

        labels = y
        le = LabelEncoder()
        y = keras.utils.to_categorical(le.fit_transform(labels))
        X, y = shuffle(X ,y)
        X = np.array(X).reshape(len(X), 60, 80, 1)
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        return X_train, X_test, y_train, y_test, le

    def create_model(self, output_size):
        model = keras.models.Sequential()
        model.add(keras.layers.Conv2D(64, kernel_size = 3, activation = "relu", input_shape = (60 ,80 ,1)))
        model.add(keras.layers.Dropout(.2))
        model.add(keras.layers.Conv2D(32, kernel_size = 3, activation = "relu"))
        # model.add(keras.layers.Dropout(.2))
        # model.add(keras.layers.Conv2D(16, kernel_size = 3, activation =  "relu"))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dropout(.2))
        model.add(keras.layers.Dense(output_size, activation = "softmax"))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model