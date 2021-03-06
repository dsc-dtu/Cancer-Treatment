import pandas
# from pattern.en import sentiment
# import HTMLParser
import re
import pandas as pd
import tensorflow as tf
from collections import Counter
from nltk.corpus import stopwords
import string
from collections import OrderedDict
from nltk import bigrams
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy as np
# import plotly.plotly as py

# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import recall_score, precision_score, accuracy_score
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.feature_selection import RFE
from tensorflow.python.framework import ops
import requests
from bs4 import BeautifulSoup
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import style
# style.use("ggplot")
import os

from tf_utils import load_dataset, convert_to_one_hot,create_placeholders,initialize_parameters,forward_propagation,compute_cost,random_mini_batches


def model(X_train, Y_train, X_test, Y_test, learning_rate=0.0001,
          num_epochs=2000, minibatch_size=32, print_cost=True):
    ops.reset_default_graph()  # to be able to rerun the model without overwriting tf variables
    tf.set_random_seed(1)  # to keep consistent results
    seed = 3  # to keep consistent results
    (n_x, m) = X_train.shape  # (n_x: input size, m : number of examples in the train set)
    n_y = Y_train.shape[0]  # n_y : output size
    costs = []  # To keep track of the cost

    # Create Placeholders of shape (n_x, n_y)

    X, Y = create_placeholders(n_x, n_y)


    # Initialize parameters

    parameters = initialize_parameters()


    # Forward propagation: Build the forward propagation in the tensorflow graph

    Z3 = forward_propagation(X, parameters)


    # Cost function: Add cost function to tensorflow graph

    cost = compute_cost(Z3, Y)


    # Backpropagation: Define the tensorflow optimizer. Use an AdamOptimizer.

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)


    # Initialize all the variables
    init = tf.global_variables_initializer()

    # Start the session to compute the tensorflow graph
    with tf.Session() as sess:

        # Run the initialization
        sess.run(init)

        # Do the training loop
        for epoch in range(num_epochs):

            epoch_cost = 0  # Defines a cost related to an epoch
            num_minibatches = int(m / minibatch_size)
            # number of minibatches of size minibatch_size in the train set

            #print("Number of minibatch = " + str(num_minibatches))

            minibatches = random_mini_batches(X_train, Y_train, minibatch_size)

            for minibatch in minibatches:
                # Select a minibatch
                (minibatch_X, minibatch_Y) = minibatch

                # IMPORTANT: The line that runs the graph on a minibatch.
                # Run the session to execute the "optimizer" and the "cost", the feedict should contain a minibatch for (X,Y).
                ### START CODE HERE ### (1 line)
                _, minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})
                #print("MinibatchCOst is " +str(minibatch_cost))
                ### END CODE HERE ###

                epoch_cost += minibatch_cost / num_minibatches

            # Print the cost every epoch
            if print_cost == True and epoch % 100 == 0:
                print("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)

        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        # lets save the parameters in a variable
        parameters = sess.run(parameters)
        print("Parameters have been trained!")

        # Calculate the correct predictions
        correct_prediction = tf.equal(tf.argmax(Z3), tf.argmax(Y))

        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        print("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))

        return parameters


