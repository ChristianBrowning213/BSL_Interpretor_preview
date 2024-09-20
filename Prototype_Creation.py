import sklearn
import tensorflow
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
import ast
import os
from keras.utils import to_categorical
import numpy as np

def Get_Dataset (dataset, labels):
    f = open("Dataset_Long.txt", "r")
    f.readline()
    f.readline()
    
    for line in f:
        
        split_line = line.split(",",1)
        labels.append(split_line[0])
        dataset_line = split_line[1]
        list_of_tuples = ast.literal_eval(dataset_line)
        dataset.append( list_of_tuples[0] )
    f.close()   

dataset= []
labels = []
#Now we need to fill dataset and labels
Get_Dataset(dataset,labels)
print("got dataset")

numpy_dataset = np.array(dataset)

from sklearn.model_selection import train_test_split

labels_one_hot = to_categorical(labels, num_classes=23)


data_reshape = numpy_dataset.reshape(numpy_dataset.shape[0], numpy_dataset.shape[1], numpy_dataset.shape[2] * numpy_dataset.shape[3])

datasetTrain, datasetsplit, labelsTrain, labelssplit = sklearn.model_selection.train_test_split(data_reshape, labels_one_hot, test_size=0.2, random_state=56)

datasetValuation, datasetTest, labelValuation, labelTest = sklearn.model_selection.train_test_split(datasetsplit, labelssplit, test_size=0.5, random_state=56)


#data = tensorflow.reshape(testarray, (None, 10, 75*2))

#dataVal = tensorflow.reshape(datasetValuation, (None, 10, 75*2))
from keras.layers import Dropout


#reshaped_data = tensorflow.reshape(dataset, (-1, 10, 75, 2))
print ("SHAPE " + str(datasetTrain.shape) ) 
'''
model = Sequential([
    LSTM(128, input_shape=(10, 150)),
    #LSTM(128, input_shape=(10, 150), dropout=0.2, recurrent_dropout=0.2),
    Dense(64, activation='relu'),
    Dense(31, activation='softmax')
])
'''
#'''
from keras import layers, models

model = models.Sequential([
    layers.LSTM(128, input_shape=(13, 150), return_sequences=True),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.LSTM(128, return_sequences=True),
    layers.Dropout(0.4),
    layers.LSTM(64),
    layers.Dropout(0.4),
    layers.BatchNormalization(),
    layers.Dense(64, activation='relu'),
    layers.Dense(23, activation='softmax')  
])
#'''
'''
model = Sequential([
    LSTM(128, input_shape=(10, 150)),
    Dense(64, activation='relu'),
    
    Dense(31, activation='softmax')
])
'''
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dropout
'''
model = Sequential([
    Conv1D(32, 3, activation='relu', input_shape=(25, 150)),
    MaxPooling1D(2),
    Conv1D(64, 3, activation='relu'),
    MaxPooling1D(2),
    Conv1D(128, 3, activation='relu'),
    MaxPooling1D(2),
    Flatten(),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dense(31, activation='softmax')
])
'''
# Compile the model
from keras.optimizers import SGD
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
#'''
#model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#'''
#'''
optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
#'''

from keras.callbacks import EarlyStopping

#early_stopping = EarlyStopping(monitor='val_loss', patience=50)  # Stop training if val_loss doesn't improve for 3 epochs

early_stopping = EarlyStopping(monitor='val_accuracy', patience=50, restore_best_weights=True, mode = 'max')
#history = model.fit(datasetTrain, labelsTrain, batch_size=32, epochs=100, validation_data=(datasetValuation, labelValuation), callbacks=[early_stopping])

# Train the model
#history = model.fit(datasetTrain, labelsTrain, batch_size=32, epochs=200, validation_data=(datasetValuation, labelValuation))
history = model.fit(datasetTrain, labelsTrain, batch_size=32, epochs=400, validation_data=(datasetValuation, labelValuation), callbacks=[early_stopping])
#
# Evaluate the model
loss, accuracy = model.evaluate(datasetTest, labelTest)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

model.save("Test_Model_long4.h5")

model.save("Test_Model_long4.keras")