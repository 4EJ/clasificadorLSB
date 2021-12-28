from tensorflow.keras.callbacks import Callback

class CallbackEvaluator(Callback):
    def __init__(self, batches, training_model_gui):
        super(CallbackEvaluator, self).__init__()
        self.batches = batches
        self.training_model_gui = training_model_gui
    
    def on_predict_batch_end(self, batch, logs=None):
        percentaje = int((batch  * 100) / self.batches)
        self.training_model_gui.update_progress_bar(percentaje)