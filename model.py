import tensorflow as tf


# TODO: save model weights in separate file

def load_data():
    mnist_dataset = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist_dataset.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return x_train, y_train, x_test, y_test


def build_model():
    global model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation=tf.keras.activations.relu),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation=tf.keras.activations.softmax)
    ])

    model.compile(optimizer='adam',
                  loss=tf.losses.sparse_categorical_crossentropy,
                  metrics=["accuracy", "AUC"])


def train_model(x, y, epochs: int):
    model.fit(x, y, epochs)


def evaluate_model(x_test, y_test):
    model.evaluate(x_test, y_test)


def main():
    epochs = 10
    x_train, y_train, x_test, y_test = load_data()
    build_model()
    train_model(x_train, y_train, epochs)
    evaluate_model(x_test, y_test)


if __name__ == "__main__":
    main()
