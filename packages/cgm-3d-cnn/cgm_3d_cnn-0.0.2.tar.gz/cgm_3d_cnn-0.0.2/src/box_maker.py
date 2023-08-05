import os
import numpy as np

try:
  from keras.utils import np_utils
  from keras.utils import to_categorical
  
except ImportError:
  from tensorflow.keras.utils import np_utils
  from tensorflow.keras.utils import to_categorical

# box-maker

# fill a box
def make_one_box(pre_box):
  """ Makes and fills one expanded final box """
  box = np.zeros([9, 9, 9, 20]) # 4D array filled with 0

  for ind_set in pre_box:
    box[ind_set[0]][ind_set[1]][ind_set[2]][ind_set[3]] += 1

  return box

# returns list of condensed boxes
def get_box_list(path): 
  """ compiles a list of preboxes from multiple files """
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

# preparing testing data
def get_test_data(path_x, path_y):
  """ loads testing data into one list of expanded boxes """
  x_data_test = np.load(path_x, allow_pickle = True)
  y_data_test = np.load(path_y, allow_pickle = True)
  
  x_test = []
  for index_set  in x_data_test:
    box = make_one_box(index_set)
    x_test.append(box)

  x_test = np.asarray(x_test)
  y_test = np_utils.to_categorical(y_data_test, 20)

  return x_test, y_test