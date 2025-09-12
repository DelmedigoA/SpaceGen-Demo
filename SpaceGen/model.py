import tensorflow as tf
from .preprocessor import *
from .utils import *


# Path to your Keras model
MODEL_PATH = "SpaceGen/SpaceGen_Large.keras"


# Compatibility shim: accept and ignore deprecated/unknown 'time_major'
class LSTMCompat(tf.keras.layers.LSTM):
    def __init__(self, *args, time_major=None, **kwargs):
        super().__init__(*args, **kwargs)


def _load_model(path: str):
    """Load a Keras model, tolerating legacy 'time_major' in LSTM configs."""
    try:
        return tf.keras.models.load_model(path)
    except ValueError as e:
        if "time_major" in str(e):
            return tf.keras.models.load_model(path, custom_objects={"LSTM": LSTMCompat})
        raise


class SpaceGenModel:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model = _load_model(model_path)

    def fix_space(self, text: str) -> str:
        text = clean_sentence(text)
        X = text_to_X(text)
        predictions = self.model.predict(X, verbose=0)
        predicted_labels = [1 if pred[1] > 0.5 else 0 for pred in predictions[0]]
        fixed_text = insert_spaces(text.replace(" ", ""), find_indices(predicted_labels))
        return fixed_text
