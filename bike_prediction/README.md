## Bike Sharing Data Analysis

------

### Introduction

In this project, I'm using one layer simple Neural Network to predict the bike sharing usage in bay area. 

The NN model is built only using numpy

The data comes from the [UCI Machine Learning Database](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset).

The main purpose of this project is to build gradient descent algorithm and backpropgation from scrach and get a good understanding of how to build a neural network.

### Main Techniques Practiced In This Project

> convert catagorical data into continous data using binary encoding
> normalizing data for model efficiency
> train,test,validation split
> Implementing Gradient Descent Algorithm
> Implementing BackPropgatiom 


### Summary

Generally speaking, for the first half of the testing data, my prediction fits well with the testing_target ,but for the second half of the data - starting from Dec 21, my prediction becomes significantly larger than the target. 

My explanation is as follows: As we can see, Dec21 to Dec31 is around Chrismas Day , as people are having vacation during this period of time, their behavior can signicantly differ from other period. My model failed to consider this factor, and thus will not be able to get a good prediction during Chrismas Holiday Season.

### Furture exploration

> Will multiple layer Neural Network overfit the data, or will it give a better prediction ?
> compare advantages of different Gradient Descent Algorithms 
