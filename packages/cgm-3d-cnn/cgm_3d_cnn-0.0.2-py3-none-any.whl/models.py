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
# models

# cnn model structure
def model_1(GPUS = 1):
  """ model with three conv layers and one dense layer """
  model = Sequential()
  model.add(Convolution3D(32, kernel_size = (3, 3, 3), strides = (1, 1, 1), activation = 'relu', input_shape = (9, 9, 9, 20))) # 32 output nodes, kernel_size is your moving window, activation function, input shape = auto calculated
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Flatten()) # now our layers have been combined to one
  model.add(Dense(500, activation = 'relu')) # 500 nodes in the last hidden layer
  model.add(Dense(20, activation = 'softmax')) # output layer has 20 possible classes (amino acids 0 - 19)

  model = multi_gpu_model(model, gpus=GPUS)

  model.compile(loss ='categorical_crossentropy', optimizer = Adam(lr = .001), metrics = ['accuracy'])

  return model

def model_2(GPUS = 1):
  """ model with 5 conv layers and one large dense layer """
  model = Sequential()
  model.add(Convolution3D(32, kernel_size = (3, 3, 3), strides = (1, 1, 1), activation = 'relu', input_shape = (9, 9, 9, 20))) # 32 output nodes, kernel_size is your moving window, activation function, input shape = auto calculated
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
  model.add(Flatten()) # now our layers have been combined to one
  model.add(Dense(1000, activation = 'relu')) # 500 nodes in the last hidden layer
  model.add(Dense(20, activation = 'softmax')) # output layer has 20 possible classes (amino acids 0 - 19)

  model = multi_gpu_model(model, gpus=GPUS)

  model.compile(loss ='categorical_crossentropy', optimizer = Adam(lr = .001), metrics = ['accuracy'])

  return model

def model_3(GPUS = 1):
  """ model with three conv layers, one dense layer and more neurons """
  model = Sequential()
  model.add(Convolution3D(60, kernel_size = (3, 3, 3), strides = (1, 1, 1), activation = 'relu', input_shape = (9, 9, 9, 20))) # 32 output nodes, kernel_size is your moving window, activation function, input shape = auto calculated
  model.add(Convolution3D(60, (3, 3, 3), activation = 'relu'))
  model.add(Convolution3D(60, (3, 3, 3), activation = 'relu'))
  model.add(Flatten()) # now our layers have been combined to one
  model.add(Dense(1000, activation = 'relu')) # 500 nodes in the last hidden layer
  model.add(Dense(20, activation = 'softmax')) # output layer has 20 possible classes (amino acids 0 - 19)

  model = multi_gpu_model(model, gpus=GPUS)

  model.compile(loss ='categorical_crossentropy', optimizer = Adam(lr = .001), metrics = ['accuracy'])

  return model