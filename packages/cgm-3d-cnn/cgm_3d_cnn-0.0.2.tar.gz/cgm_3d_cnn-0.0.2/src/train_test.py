from generators import train_dataGenerator
from generators import test_val_dataGenerator

try:
  import keras
  from keras.models import Sequential
  from keras.layers import Dense, Dropout, Activation, Flatten
  from keras.layers import Convolution3D
  from keras.optimizers import Adam
  from keras.callbacks import Callback
  from keras.models import load_model
  from keras.utils import multi_gpu_model
  from keras.utils import np_utils
  from keras.utils import to_categorical

except ImportError:
  import tensorflow
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
  from tensorflow.keras.layers import Convolution3D
  from tensorflow.keras.callbacks import Callback
  from tensorflow.keras.optimizers import Adam
  from tensorflow.keras.models import load_model
  from tensorflow.keras.utils import multi_gpu_model
  from tensorflow.keras.utils import np_utils
  from tensorflow.keras.utils import to_categorical

# Training and testing

# training the model
def train_model(model, batch_size, epochs, rotations, x_train, y_train, x_val, y_val):
  """ calling the model to train """

  history = model.fit_generator(
            generator = train_dataGenerator(x_train, y_train, batch_size, rotations),
            validation_data = test_val_dataGenerator(x_val, y_val, batch_size),
            validation_steps = 20,
            steps_per_epoch = len(x_train)/batch_size, 
            epochs = epochs, 
            verbose = 1,
          )

  return history

# returns testing results
def get_testing_results(model, batch_size, x_test, y_test):
  """ testing the trained model """
  
  score = model.evaluate(x_test, y_test, verbose = 1, steps = int(len(x_test)/batch_size))  
  #score = model.evaluate_generator(x_test, y_test, verbose = 1, steps = int(len(x_test)/batch_size))
  model.save('model.h5')

  return score