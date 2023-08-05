# this module contains rotation functions for a 9 x 9 x 9 cube. 
import math
import random

# axis is the axis across which the rotation occurs
# rot_num is the number of 90 degree rotations needed (0, 1, 2 or 3)
def rotate_box(pre_box, axis, rot_num = 0, box_size = 9): #box size is the number of bins
  """ rotates box along one axis rot_num times """

  box_size -= 1 # with 9 bins, indices are 0-8
  dict = {"x":[1, 2], "y":[0, 2], "z":[0, 1]} # lists the axes to be changed if rotated around key
  new_pre_box = []
  
  for ind_set in pre_box:
    a_1, a_2 = dict[axis][0], dict[axis][1]
    ind_1, ind_2 = ind_set[a_1], ind_set[a_2]
    new_set = ind_set.copy()
  
    if rot_num == 1:
      new_set[a_1] = box_size - ind_2
      new_set[a_2] = ind_1
    
    if rot_num == 2:
      new_set[a_1] = box_size - ind_1
      new_set[a_2] = box_size - ind_2
      
    if rot_num == 3:
      new_set[a_1] = ind_2
      new_set[a_2] = box_size - ind_1

    new_pre_box.append(new_set)
    

  return new_pre_box

def multiple_rotations(i, pre_box, box_size = 9): # i is a value from 0-23 (encodes the 24 possible rotations)
  """ rotates box into one of 24 possible cube orientations """

  prebox_1 = rotate_box(pre_box, "z", i%4, box_size) # remainder conveniently assignes i to one of 4 z-axis rotations.

  # rotate along x or y
  rot_num = math.floor(i/4) # 0-5 (gives one of 6 remaining rotation possibilities)
  if rot_num < 4:
    prebox_2 = rotate_box(prebox_1, "y", rot_num, box_size) # 3 possible rotations around y
  elif rot_num == 4: 
    prebox_2 = rotate_box(prebox_1, "x", 1, box_size) # get one of the remaining two conformations by rotating around x
  elif rot_num == 5:
    prebox_2 = rotate_box(prebox_1, "x", 3, box_size)

  return prebox_2

# chooses one of 24 conformations
def rotation_combo(pre_box, rotations, box_size = 9):
  """ randomly selects one of the 24 orientations of a cube """
  final_preboxes = []
  rot_list = random.sample(range(0, 24), rotations) # get random cube conformations "rotations" number of times.

  for i in rot_list:
    rotated_prebox = multiple_rotations(i, pre_box, box_size)
    final_preboxes.append(rotated_prebox)

  return final_preboxes

  