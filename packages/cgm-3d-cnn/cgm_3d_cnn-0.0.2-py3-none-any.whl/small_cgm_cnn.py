# course grained cnn on 38 proteins (small practice dataset)
from rotations import rotation_combo
from matplotlib import pyplot as plt
import numpy as np
import os
import sys
import random

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

# fill a box
def make_one_box(pre_box):
  box = np.zeros([9, 9, 9, 20]) # 4D array filled with 0
  for ind_set in pre_box:
    box[ind_set[0]][ind_set[1]][ind_set[2]][ind_set[3]] += 1
  return box

def get_box_list(): 
  path = "./boxes/"
  fileList = os.listdir(path)
  pre_box_list = []
  center_aa_list = []

  for file in fileList:
    if "boxes" in file:
      pdb_id = file[-8:-4]

      pre_boxes = np.load(path + file, allow_pickle = True)
      for pre_box in pre_boxes:
        pre_box_list.append(pre_box)

      centers = np.load(path + "centers_" + pdb_id + ".npy", allow_pickle = True) # list of center aa's in one file
      for center in centers:
        center_aa_list.append(center)
  
  return pre_box_list, center_aa_list

def dataGenerator(pre_boxes, center_aa_list, batch_size):
  zip_lists = list(zip(pre_boxes, center_aa_list))
  random.shuffle(zip_lists)
  pre_boxes, center_aa_list = list(zip(*zip_lists))

  while True:
      for i in range(0, len(pre_boxes) - batch_size, batch_size):
        box_list = []
        center_list = []
        for j in range(i, i + batch_size): 
          box = make_one_box(pre_boxes[j])
          box_list.append(box)
          center_list.append(center_aa_list[j])

        yield np.asarray(box_list), np_utils.to_categorical(center_list, 20)

# training data
x_train, y_train = get_box_list()

# preparing testing data
x_test = np.load("./testing/boxes_test.npy", allow_pickle = True)
y_test = np.load("./testing/centers_test.npy", allow_pickle = True)
y_data_test = np_utils.to_categorical(y_test, 20)

x_data_test = []
for index_set  in x_test:
  box = make_one_box(index_set)
  x_data_test.append(box)
x_data_test = np.asarray(x_data_test)

model = Sequential()
model.add(Convolution3D(filters = 32, kernel_size = (3, 3, 3), strides = (1, 1, 1), activation = 'relu', input_shape = (9, 9, 9, 20))) # 32 output nodes, kernel_size is your moving window, activation function, input shape = auto calculated
model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
model.add(Convolution3D(32, (3, 3, 3), activation = 'relu'))
model.add(Flatten()) # now our layers have been combined to one
model.add(Dense(500, activation = 'relu')) # 500 nodes in the last hidden layer
model.add(Dense(20, activation = 'softmax')) # output layer has 20 possible classes (amino acids 0 - 19)

#model = multi_gpu_model(model, gpus=4)

model.compile(loss ='categorical_crossentropy',
              optimizer = Adam(lr = .001),
              metrics = ['accuracy'])

batch_size = 8

history = model.fit_generator(
          generator = dataGenerator(x_train, y_train, batch_size),
          # Please fix this!!!! should be new data
          validation_data = dataGenerator(x_test, y_test, batch_size),
          validation_steps = 20,
          steps_per_epoch = len(x_train)/batch_size, 
          epochs = 20, 
          verbose = 1,
         )

score = model.evaluate(x_data_test, y_data_test, verbose = 1, steps = int(len(x_data_test)/batch_size))  
model.save('model.h5')

print("score: ", score)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#graphing the accuracy and loss for both the training and test data
#summarize history for accuracy 

#print(history.history.keys())


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['training', 'validation'], loc = 'upper left')
plt.savefig("Accuracy_small_cgm.pdf")
plt.clf()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['training', 'validaton'], loc = 'upper left')
plt.savefig("Loss_small_cgm.pdf")