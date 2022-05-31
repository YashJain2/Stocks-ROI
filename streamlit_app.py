import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
from sklearn.preprocessing import MinMaxScaler


start = '2010-01-01'
end='2022-12-31'

st.title('Stock Prediction Application')


user_input=st.text_input('Enter Stock initials','TCS.NS')
df=data.DataReader(user_input,'yahoo',start,end)




st.subheader ('Data from 2010-2021')
st.write(df.describe())
  



st.subheader('Closing Price Vs Time')
fig=plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)



st.subheader('Closing Price Vs Time with 100 days Moving Average')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)



st.subheader('Closing Price Vs Time with 200 days Moving Average')
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12,6))
plt.plot(ma200,'g')
plt.plot(ma100,'r')
plt.plot(df.Close,'b')
st.pyplot(fig)




 # Splitting data into training and testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

# print(data_training.shape)
# print(data_testing.shape)


# for stack LSTM method we have to scale down the training and testing data sets

scaler=MinMaxScaler(feature_range=(0,1))
data_training_array=scaler.fit_transform(data_training)
# data_training_array



# x_train=[]
# y_train=[]
# for i in range(100, data_training_array.shape[0]):
#     x_train.append(data_training_array[i-100:i])
#     y_train.append(data_training_array[i,0])
    
# # x_train
# x_train,y_train=np.array(x_train),np.array(y_train)





# load my model

model=load_model('ITC.h5')



past_100_days = data_training.tail(100)


final_df=past_100_days.append(data_testing, ignore_index=True)



input_data=scaler.fit_transform(final_df)
# input_data


x_test=[]
y_test=[]

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])


x_test,y_test=np.array(x_test),np.array(y_test)
# print(x_test.shape)
# print(y_test.shape)


y_predicted = model.predict(x_test)

scaler = scaler.scale_

scale_factor=1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test=y_test*scale_factor


st.subheader('Prediction Vs Original Trend')
fig2 = plt.figure(figsize=(12,8))
plt.plot(y_test,'b',label='Original Price')
plt.plot(y_predicted,'r',label='Predicted Price')
plt.xlabel('TIME')
plt.ylabel('PRICE')
plt.legend()
st.pyplot(fig2)
