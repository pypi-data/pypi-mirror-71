import numpy as np
import sys
import os
sys.path.append(os.path.abspath(".."))
from rotations import multiple_rotations
# testing the rotation functions in rotations.py 

def test_z_rotations():
  box_size = 2
  pre_box = [[0, 1, 0, 15]] 

  # when i = 0, 1, 2 and 3, rotations are arround z-axis
  assert multiple_rotations(0, pre_box, box_size) == [[0, 1, 0, 15]]
  assert multiple_rotations(1, pre_box, box_size) == [[0, 0, 0, 15]]
  assert multiple_rotations(2, pre_box, box_size) == [[1, 0, 0, 15]]
  assert multiple_rotations(3, pre_box, box_size) == [[1, 1, 0, 15]]

def test_y_rotations():
  box_size = 2
  pre_box = [[0, 1, 0, 15]]

  assert multiple_rotations(4, pre_box, box_size) == [[1, 1, 0, 15]]
  assert multiple_rotations(8, pre_box, box_size) == [[1, 1, 1, 15]]
  assert multiple_rotations(12, pre_box, box_size) == [[0, 1, 1, 15]]

def test_x_rotations():
  box_size = 2
  pre_box = [[0, 1, 0, 15]]

  assert multiple_rotations(16, pre_box, box_size) == [[0, 1, 1, 15]]
  assert multiple_rotations(20, pre_box, box_size) == [[0, 0, 0, 15]]

def test_rotation_combo_1():
  box_size = 2
  pre_box = [[0, 1, 0, 15]]

  # rotations: 1x, 1z, 2y, 3z, 1x
  r1 = multiple_rotations(16, pre_box, box_size)
  r2 = multiple_rotations(1, r1, box_size)
  r3 = multiple_rotations(8, r2, box_size)
  r4 = multiple_rotations(3, r3, box_size)
  r5 = multiple_rotations(16, r4, box_size)

  assert r5 == pre_box

  # should not be equal
  r1 = multiple_rotations(16, pre_box, box_size)
  r2 = multiple_rotations(2, r1, box_size)
  r3 = multiple_rotations(8, r2, box_size)
  r4 = multiple_rotations(3, r3, box_size)
  r5 = multiple_rotations(16, r4, box_size)

  assert r5 != pre_box

def test_rotation_combo_2(): 
  box_size = 2
  pre_box = [[0, 1, 0, 15]]

  # rotations: 1y compared to 1z, 1x, 3z
  r1 = multiple_rotations(4, pre_box, box_size)
  r2 = multiple_rotations(17, pre_box, box_size)
  r2 = multiple_rotations(3, r2, box_size)
 
  assert r1 == r2

  # should not be equal
  r1 = multiple_rotations(4, pre_box, box_size)
  r2 = multiple_rotations(16, pre_box, box_size)
  r2 = multiple_rotations(2, r2, box_size)

  assert r1 != r2

