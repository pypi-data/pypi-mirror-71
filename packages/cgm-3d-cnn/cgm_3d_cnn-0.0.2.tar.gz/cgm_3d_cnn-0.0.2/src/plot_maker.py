from matplotlib import pyplot as plt
# plot-maker

#graphing the accuracy and loss for both the training and test data
def get_plots(history):
  """ creates simple plots of accuracy and loss for training and validation """
  #summarize history for accuracy 
  plt.plot(history.history['accuracy'])
  plt.plot(history.history['val_accuracy'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['training', 'validation'], loc = 'upper left')
  plt.savefig("Accuracy_cgm_flips.pdf")
  plt.clf()

  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['training', 'validaton'], loc = 'upper left')
  plt.savefig("Loss_cgm_flips.pdf")