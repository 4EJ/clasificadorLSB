from tensorflow.keras.callbacks import Callback

class CallbackTraining(Callback):
    def __init__(self, total_epochs, training_model_gui):
        super(CallbackTraining, self).__init__()
        self.total_epochs = total_epochs
        self.training_model_gui = training_model_gui

    def on_epoch_end(self, epoch, logs=None):
        epoch = epoch + 1
        percentaje = int((epoch  * 100) / self.total_epochs)
        self.training_model_gui.update_progress_bar(percentaje)
        epoch_performance = 'Epoca ' + str(epoch) + '/' + str(self.total_epochs) + ' - '
        epoch_performance = epoch_performance + 'Exactitud: ' + str(logs['accuracy']) + '\n'
        self.training_model_gui.add_text_details(epoch_performance)
        self.training_model_gui.generate_graphics(logs['accuracy'])