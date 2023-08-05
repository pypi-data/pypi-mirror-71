import numpy as np
import sys
import os
sys.path.append(os.path.abspath(".."))
from rotations import rotate_box

# testing rotations around x-axis
def test_x_rotations():
  axis = 'x'
  box_size = 2
  pre_box = [[0, 1, 0, 15]] 

  assert rotate_box(pre_box, axis, 0, box_size) == [[0, 1, 0, 15]]
  assert rotate_box(pre_box, axis, 1, box_size) == [[0, 1, 1, 15]]
  assert rotate_box(pre_box, axis, 2, box_size) == [[0, 0, 1, 15]]
  assert rotate_box(pre_box, axis, 3, box_size) == [[0, 0, 0, 15]]

# testing rotations around y-axis
def test_y_rotations():
  axis = 'y'
  box_size = 2
  pre_box = [[0, 1, 0, 15]] 

  assert rotate_box(pre_box, axis, 0, box_size) == [[0, 1, 0, 15]]
  assert rotate_box(pre_box, axis, 1, box_size) == [[1, 1, 0, 15]]
  assert rotate_box(pre_box, axis, 2, box_size) == [[1, 1, 1, 15]]
  assert rotate_box(pre_box, axis, 3, box_size) == [[0, 1, 1, 15]]

  # testing rotations around z-axis
def test_z_rotations():
  axis = 'z'
  box_size = 2
  pre_box = [[0, 1, 0, 15]] 

  assert rotate_box(pre_box, axis, 0, box_size) == [[0, 1, 0, 15]]
  assert rotate_box(pre_box, axis, 1, box_size) == [[0, 0, 0, 15]]
  assert rotate_box(pre_box, axis, 2, box_size) == [[1, 0, 0, 15]]
  assert rotate_box(pre_box, axis, 3, box_size) == [[1, 1, 0, 15]]

def test_not_equal():
  axis = 'z'
  box_size = 2
  pre_box = [[0, 1, 0, 15]] 

  assert rotate_box(pre_box, axis, 0, box_size) != [[1, 1, 0, 15]]
  assert rotate_box(pre_box, axis, 1, box_size) != [[1, 1, 1, 15]]
  assert rotate_box(pre_box, axis, 2, box_size) != [[1, 0, 1, 15]]
  assert rotate_box(pre_box, axis, 3, box_size) != [[1, 0, 0, 15]]

def test_size_1_box():
  box_size = 1
  pre_box = [[0, 0, 0, 15]] 

  assert rotate_box(pre_box, "x", 0, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "x", 1, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "x", 2, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "x", 3, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "x", 3, box_size) != [[0, 0, 1, 15]]

  assert rotate_box(pre_box, "y", 0, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "y", 1, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "y", 2, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "y", 3, box_size) == [[0, 0, 0, 15]]
  assert rotate_box(pre_box, "y", 3, box_size) != [[1, 1, 1, 15]] 

  assert rotate_box(pre_box, "z", 0, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "z", 1, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "z", 2, box_size) == [[0, 0, 0, 15]] 
  assert rotate_box(pre_box, "z", 3, box_size) == [[0, 0, 0, 15]]
  assert rotate_box(pre_box, "z", 3, box_size) != [[1, 1, 0, 15]]  

def test_size_3_box():
  box_size = 3
  pre_box = [[2, 2, 2, 15]] 

  # x rotations
  assert rotate_box(pre_box, "x", 0, box_size) == [[2, 2, 2, 15]] 
  assert rotate_box(pre_box, "x", 1, box_size) == [[2, 0, 2, 15]] 
  assert rotate_box(pre_box, "x", 2, box_size) == [[2, 0, 0, 15]] 
  assert rotate_box(pre_box, "x", 3, box_size) == [[2, 2, 0, 15]] 
  assert rotate_box(pre_box, "x", 3, box_size) != [[0, 2, 2, 15]]

  # y rotations
  assert rotate_box(pre_box, "y", 0, box_size) == [[2, 2, 2, 15]] 
  assert rotate_box(pre_box, "y", 1, box_size) == [[0, 2, 2, 15]] 
  assert rotate_box(pre_box, "y", 2, box_size) == [[0, 2, 0, 15]] 
  assert rotate_box(pre_box, "y", 3, box_size) == [[2, 2, 0, 15]]
  assert rotate_box(pre_box, "y", 3, box_size) != [[1, 2, 1, 15]] 

  # z rotations
  assert rotate_box(pre_box, "z", 0, box_size) == [[2, 2, 2, 15]] 
  assert rotate_box(pre_box, "z", 1, box_size) == [[0, 2, 2, 15]] 
  assert rotate_box(pre_box, "z", 2, box_size) == [[0, 0, 2, 15]] 
  assert rotate_box(pre_box, "z", 3, box_size) == [[2, 0, 2, 15]]
  assert rotate_box(pre_box, "z", 3, box_size) != [[2, 2, 0, 15]]

  # only box in center is filled
  pre_box = [[1, 1, 1, 15]]

  # x rotations
  assert rotate_box(pre_box, "x", 0, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "x", 1, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "x", 2, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "x", 3, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "x", 3, box_size) != [[0, 2, 2, 15]]

  # y rotations
  assert rotate_box(pre_box, "y", 0, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "y", 1, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "y", 2, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "y", 3, box_size) == [[1, 1, 1, 15]]
  assert rotate_box(pre_box, "y", 3, box_size) != [[1, 2, 1, 15]] 

  # z rotations
  assert rotate_box(pre_box, "z", 0, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "z", 1, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "z", 2, box_size) == [[1, 1, 1, 15]] 
  assert rotate_box(pre_box, "z", 3, box_size) == [[1, 1, 1, 15]]
  assert rotate_box(pre_box, "z", 3, box_size) != [[2, 2, 0, 15]]
  