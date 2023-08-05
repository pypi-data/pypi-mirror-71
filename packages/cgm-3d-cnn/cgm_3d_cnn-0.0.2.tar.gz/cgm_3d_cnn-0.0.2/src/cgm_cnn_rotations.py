# course grained cnn with rotations
from box_maker import get_box_list
from box_maker import get_test_data
import models
from train_test import train_model
from train_test import get_testing_results
from plot_maker import get_plots

# variables
EPOCHS = 1 # iterations through the data
ROTATIONS = 4 # number of box rotations
BATCH_SIZE = 20 # batch_size must be divisible by "ROTATIONS"
GPUS = 4 # max is 4 GPUs

# data paths
training_path = "../boxes/"
validation_path = "../boxes_38/"
testing_path_x = "../testing/boxes_test.npy"
testing_path_y = "../testing/centers_test.npy"

# training and validation
x_train, y_train = get_box_list(training_path) # preparing training data (boxes, centers)
x_val, y_val = get_box_list(validation_path) # preparing validation data (boxes, centers)
model = models.model_1(GPUS)
history = train_model(model, BATCH_SIZE, EPOCHS, ROTATIONS, x_train, y_train, x_val, y_val)

# testing
x_test, y_test = get_test_data(testing_path_x, testing_path_y)
score = get_testing_results(model, BATCH_SIZE, x_test, y_test)

# results
get_plots(history)
print('Test loss:', score[0])
print('Test accuracy:', score[1])








