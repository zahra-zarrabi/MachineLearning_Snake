import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

df = pd.read_csv('dataset2.csv')
Y_train = df[['direction']]
x_train = df.drop(columns=['Unnamed: 0','direction'])

X_train, X_val, Y_train, Y_val = train_test_split(x_train, Y_train, test_size=0.2, random_state=40)

Y_train=Y_train.replace(['right','left','up','down'],[1,3,0,2])
Y_val=Y_val.replace(['right','left','up','down'],[1,3,0,2])

X_train = np.array(X_train)
Y_train = np.array(Y_train)
X_val = np.array(X_val)
Y_val = np.array(Y_val)

X_train_min = np.min(X_train[:, :4],axis=0)
X_train_max = np.max(X_train[:, :4],  axis=0)
X_train[:, :4] = np.subtract(X_train[:, :4], X_train_min)/(X_train_max - X_train_min)
np.save('x_train_min.npy',X_train_min)
np.save('x_train_max.npy',X_train_max)

X_val_min = np.min(X_val[:,:4],axis=0)
X_val_max = np.max(X_val[:,:4],axis=0)
X_val[:,:4] = np.subtract(X_val[:,:4],X_val_min)/(X_val_max - X_val_min)

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(32,input_dim= 8, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax'),
])

model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001),
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=['accuracy'])

output = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=50)
print(output.history)
model.save('save.h5')