import tensorflow as tf


# TODO: download mnist dataset
# TODO: create Keras model
# TODO: train and evaluate
# TODO: save model weights in separate file

def load_data():
    mnist_dataset = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist_dataset.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return x_train, y_train, x_test, y_test


def main():
    if tf.test.gpu_device_name():
        print(f"Default GPU Device: {tf.test.gpu_device_name()}")
    else:
        print("Please install GPU version of TF")


if __name__ == "__main__":
    main()
