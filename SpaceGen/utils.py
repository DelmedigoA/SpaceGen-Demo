import numpy as np
import pandas as pd
import string
import re
from .preprocessor import Preprocessor as sp

max_len = 853

def text_to_X(text):
    test_text = text.replace(' ', '')
    data = pd.DataFrame([test_text], columns=["correct_sentence"])
    data['wrong_sentence'] = data['correct_sentence'].apply(lambda text: text.replace(' ',''))
    data['bytes_correct'] = data['correct_sentence'].apply(lambda text: sp.to_bytes_list(text))
    data['bytes_wrong'] = data['wrong_sentence'].apply(lambda text: sp.to_bytes_list(text))
    data['decision'] = data[['bytes_wrong','bytes_correct']].apply(lambda row: sp.create_decision_vector(row['bytes_wrong'], row['bytes_correct']), axis=1)
    dec_dict = {'K': 0, 'I': 1}
    data['decision'] = data['decision'].apply(lambda dec: [dec_dict[d] for d in dec])
    data = data[data.bytes_wrong.apply(lambda bytes_wrong: len(bytes_wrong) <= 1000)]
    lngths = [len(bytes_wrong) for bytes_wrong in data.bytes_wrong.tolist()]

    data['bytes_wrong_padded'] = data['bytes_wrong'].apply(lambda bytes_wrong: bytes_wrong + [0]*(max_len-len(bytes_wrong)))
    data['decision_padded'] = data['decision'].apply(lambda decision: decision + [0]*(max_len-len(decision)))
    data['bytes_wrong_padded'] = data['bytes_wrong_padded'].apply(lambda bytes_wrong: np.array(bytes_wrong))
    data['decision_padded'] = data['decision_padded'].apply(lambda decision: np.array(decision))
    data['wrong_sentence_padded'] = data['wrong_sentence'].apply(lambda wrong_sentence: wrong_sentence + '#'*(max_len-len(wrong_sentence)))
    data['bytes_wrong_one_hot'] = data['wrong_sentence_padded'].apply(one_hot_encode)
    data['bytes_wrong_one_hot'] = data['bytes_wrong_one_hot'].apply(lambda bytes_wrong: np.array(bytes_wrong))
    X = np.stack(data.bytes_wrong_one_hot)
    return X

def find_indices(lst):
    indices = []
    for idx, value in enumerate(lst):
        if value == 1:
            indices.append(idx)
    return indices

def insert_spaces(text, indices):
    result = []
    for i, char in enumerate(text):
        if i in indices:
            result.append(" ")
        result.append(char)
    return "".join(result)


def clean_sentence(sentence):
  pattern = r'[^A-Za-z#.\'!, ]'
  return re.sub(pattern, '', sentence)

import numpy as np

def one_hot_encode(text):
    # Define the vocabulary
    vocab = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#.\'!,')

    vocab_size = len(vocab)

    # Create a mapping from character to index
    char_to_index = {char: idx for idx, char in enumerate(vocab)}

    # Initialize the one-hot encoded array
    one_hot_encoded = np.zeros((len(text), vocab_size), dtype=int)

    # Convert each character to one-hot encoded vector
    for i, char in enumerate(text):
        if char in char_to_index:  # Ensure character is in the vocabulary
            one_hot_encoded[i, char_to_index[char]] = 1
        else:
            raise ValueError(f"Character '{char}' not in vocabulary")

    return one_hot_encoded