if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import keras
from keras.models import load_model
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.preprocessing.sequence import pad_sequences

model = load_model(os.getcwd() + '/etl-demo/mark_model/best_model.keras')
scaler = StandardScaler()  # Initialize StandardScaler for preprocessing

# Preprocess function for input data
def preprocess_input(data):
    max_sequence_length = 128
    num_chunks = len(data) // max_sequence_length + 1
    predictions = []
    for i in range(num_chunks):
        start_idx = i * max_sequence_length
        end_idx = min((i + 1) * max_sequence_length, len(data))
        chunk = data[start_idx:end_idx]
        padded_chunk = pad_sequences([chunk], maxlen=max_sequence_length, dtype='float32', padding='post', truncating='post')
        preprocessed_chunk = np.asarray(padded_chunk).astype(np.float32).reshape(-1, max_sequence_length, 1)
        predictions.append(model.predict(preprocessed_chunk))
    return predictions

def your_label_mapping_function(index):
    # No stress = false, stress = true
    labels = [False, True]  # Assuming these are your original labels
    return labels[index]


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    input_data_eda = data['w_eda']

    # Preprocess input data
    # input_data_eda_preprocessed = preprocess_input(input_data_eda)
    # print(input_data_eda_preprocessed)
    max_sequence_length = 128
    input_length = len(input_data_eda)
    num_chunks = input_length // max_sequence_length + 1
    predictions = []
    for i in range(num_chunks):
        start_idx = i * max_sequence_length
        end_idx = min((i + 1) * max_sequence_length, input_length)
        chunk = input_data_eda[start_idx:end_idx]
        # data_array = [scaler.fit_transform(np.asarray(i).reshape(-1, 1)) for i in chunk]
        # preprocessed_chunk = np.asarray(data_array).astype(np.float32).reshape(-1, 128, 1)
        padded_chunk = pad_sequences([chunk], maxlen=max_sequence_length, dtype='float32', padding='post', truncating='post')
        preprocessed_chunk = np.asarray(padded_chunk).astype(np.float32).reshape(-1, max_sequence_length, 1)
        # # Perform prediction
        probabilities = model.predict(preprocessed_chunk)
        # Get the index of the maximum probability
        predicted_label_index = np.argmax(probabilities)
        # Map the index to the original label
        predicted_label = your_label_mapping_function(predicted_label_index)  # Replace with your label mapping function
        predictions.append({'chunkNumber': i + 1, 'predicted_label': predicted_label})

    return predictions


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
