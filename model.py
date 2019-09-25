import tensorflow as tf


def main():
    if tf.test.gpu_device_name():
        print(f"Default GPU Device: {tf.test.gpu_device_name()}")
    else:
        print("Please install GPU version of TF")


if __name__ == "__main__":
    main()
