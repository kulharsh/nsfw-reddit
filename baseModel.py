from dataset import getRedditData
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import numpy as np
training_sentences, testing_sentences, ytrain, ytest = getRedditData()
print('Data load complete...')
print(len(training_sentences))
#print(ytrain)
#print(len(testing_sentences))
#print(len(ytest))

print('Converting labels')
training_labels_final = np.array(ytrain)
testing_labels_final = np.array(ytest)
print('Converted labels')
vocab_size = 10000
embedding_dim = 16
max_length = 120
trunc_type = 'post'
oov_token = '<OOV>'
print('Starting tokenizer')
tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
print("Tokenizing complete.")
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type)
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen = max_length, truncating=trunc_type)
print("Converting to sequences complete.")

model = tf.keras.Sequential([
	tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
	#tf.keras.layers.Flatten(),
	tf.keras.layers.GlobalAveragePooling1D(),
	tf.keras.layers.Dense(6, activation='relu'),
	tf.keras.layers.Dense(1, activation='sigmoid')
	])
print('Model created')

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

num_epochs = 10
model.fit(padded, ytrain, epochs=num_epochs, validation_data=(testing_padded, ytest))


