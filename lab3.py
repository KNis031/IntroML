#!/usr/bin/python
# coding: utf-8

# # Lab 3: Bayes Classifier and Boosting

# ## Jupyter notebooks
# 
# In this lab, you can use Jupyter <https://jupyter.org/> to get a nice layout of your code and plots in one document. However, you may also use Python as usual, without Jupyter.
# 
# If you have Python and pip, you can install Jupyter with `sudo pip install jupyter`. Otherwise you can follow the instruction on <http://jupyter.readthedocs.org/en/latest/install.html>.
# 
# And that is everything you need! Now use a terminal to go into the folder with the provided lab files. Then run `jupyter notebook` to start a session in that folder. Click `lab3.ipynb` in the browser window that appeared to start this very notebook. You should click on the cells in order and either press `ctrl+enter` or `run cell` in the toolbar above to evaluate all the expressions.

# ## Import the libraries
# 
# In Jupyter, select the cell below and press `ctrl + enter` to import the needed libraries.
# Check out `labfuns.py` if you are interested in the details.

import numpy as np
from scipy import misc
from imp import reload
from labfuns import *
import random


# ## Bayes classifier functions to implement
# 
# The lab descriptions state what each function should do.


# NOTE: you do not need to handle the W argument for this part!
# in: labels - N vector of class labels
# out: prior - C x 1 vector of class priors
def computePrior(labels, W=None):
    Npts = labels.shape[0]
    
    if W is None:
        W = np.ones((Npts,1))/Npts
        
    else:
        assert(W.shape[0] == Npts)
    classes = np.unique(labels) #what are the seperate classes 
    Nclasses = np.size(classes) #How many diffeent classes
    prior = np.zeros((Nclasses,1))

    # TODO: compute the values of prior for each class!
    # ==========================
    # for idx, class_ in enumerate(classes):
    #     prior_value = np.count_nonzero(labels == class_)/Npts
    #     prior[idx] = prior_value
    tot_weight = np.sum(W)
    for jdx, class_ in enumerate(classes): #vikten för en klass delat med vikten för alla 
        idx = np.where(labels==class_)
        class_weight = np.sum(W[idx])
        prior_value = class_weight/tot_weight
        prior[jdx] = prior_value

    # ==========================

    return prior

# NOTE: you do not need to handle the W argument for this part!
# in:      X - N x d matrix of N data points
#     labels - N vector of class labels
# out:    mu - C x d matrix of class means (mu[i] - class i mean)
#      sigma - C x d x d matrix of class covariances (sigma[i] - class i sigma)
def mlParams(X, labels, W=None):
    assert(X.shape[0]==labels.shape[0])
    Npts,Ndims = np.shape(X)
    classes = np.unique(labels)
    Nclasses = np.size(classes)

    if W is None:
        W = np.ones((Npts,1))/float(Npts)

    mu = np.zeros((Nclasses,Ndims))
    sigma = np.zeros((Nclasses,Ndims,Ndims))

    # TODO: fill in the code to compute mu and sigma!
    # ==========================
    # print("Npts: ", Npts)
    # print("Ndims: ", Ndims)
    # print("Nclasses: ", Nclasses)

    for jdx, class_ in enumerate(classes): #loops the classes and calculates mu with the mean. 
        #idx = y == classes 
        idx = np.where(labels==class_)
        xlc = X[idx,:]
        Wlc = W[idx]
        #mu[jdx] = np.mean(xlc[0], axis=0) #OLD
        mu[jdx] = np.sum(np.multiply(Wlc,xlc[0]), axis=0)/np.sum(Wlc) #NEW
        
        # for m in range(0, Ndims): 
        #     sigma[jdx][m][m] = np.mean(np.power(xlc[:, m] - mu[jdx][m], 2)) 

        # with matrices, OLD
        # temp = xlc[0]-mu[jdx]
        # Npts_k = np.shape(temp)[0]
        # sigma[jdx] = (np.dot(temp.T,temp))/Npts_k
        # sigma[jdx] = np.diag(np.diag(sigma[jdx]))

        # with matrices, NEW
        temp = xlc[0]-mu[jdx]
        sigma[jdx] = (np.dot((np.multiply(Wlc,temp)).T,temp))/np.sum(Wlc)
        sigma[jdx] = np.diag(np.diag(sigma[jdx]))


    #print("mu", mu)
    #print("sigma: ", sigma)
    # ==========================

    return mu, sigma



# in:      X - N x d matrix of M data points
#      prior - C x 1 matrix of class priors
#         mu - C x d matrix of class means (mu[i] - class i mean)
#      sigma - C x d x d matrix of class covariances (sigma[i] - class i sigma)
# out:     h - N vector of class predictions for test points
def classifyBayes(X, prior, mu, sigma):

    Npts = X.shape[0] #number of datapoints 
    Nclasses,Ndims = np.shape(mu) 
    logProb = np.zeros((Nclasses, Npts)) #every points prob for belonging to each class

    # TODO: fill in the code to compute the log posterior logProb!
    # ==========================
    
    for i, point in enumerate(X):
        for class_ in range(0, Nclasses):

            logProb[class_][i] = ((-1/2)*np.log(np.linalg.det(sigma[class_]))) - (1/2*np.dot(np.dot((point-mu[class_]), np.linalg.inv(sigma[class_])), (point-mu[class_]).T) + np.log(prior[class_][0]))

    # ==========================
    
    # one possible way of finding max a-posteriori once
    # you have computed the log posterior
    h = np.argmax(logProb,axis=0)
    return h


# The implemented functions can now be summarized into the `BayesClassifier` class, which we will use later to test the classifier, no need to add anything else here:


# NOTE: no need to touch this
class BayesClassifier(object):
    def __init__(self):
        self.trained = False

    def trainClassifier(self, X, labels, W=None):
        rtn = BayesClassifier()
        rtn.prior = computePrior(labels, W)
        rtn.mu, rtn.sigma = mlParams(X, labels, W)
        rtn.trained = True
        return rtn

    def classify(self, X):
        return classifyBayes(X, self.prior, self.mu, self.sigma)


# ## Test the Maximum Likelihood estimates
# 
# Call `genBlobs` and `plotGaussian` to verify your estimates.


#X, labels = genBlobs(centers=5)
#mu, sigma = mlParams(X,labels)
#print(mu)
#print(sigma)
#plotGaussian(X,labels,mu,sigma)

#print(computePrior(labels))

#print("h ", classifyBayes(X, computePrior(labels), mu, sigma))



# Call the `testClassifier` and `plotBoundary` functions for this part.


#testClassifier(BayesClassifier(), dataset='iris', split=0.2)



#testClassifier(BayesClassifier(), dataset='vowel', split=0.7)



#plotBoundary(BayesClassifier(), dataset='iris',split=0.2)


# ## Boosting functions to implement
# 
# The lab descriptions state what each function should do.


# in: base_classifier - a classifier of the type that we will boost, e.g. BayesClassifier
#                   X - N x d matrix of N data points
#              labels - N vector of class labels
#                   T - number of boosting iterations
# out:    classifiers - (maximum) length T Python list of trained classifiers
#              alphas - (maximum) length T Python list of vote weights
def trainBoost(base_classifier, X, labels, T=10):
    # these will come in handy later on
    Npts,Ndims = np.shape(X)

    classifiers = [] # append new classifiers to this list
    alphas = [] # append the vote weight of the classifiers to this list

    # The weights for the first iteration
    W = np.ones((Npts,1))/float(Npts)

    for i_iter in range(0, T):
        # a new classifier can be trained like this, given the current weights
        classifiers.append(base_classifier.trainClassifier(X, labels, W))

        # do classification for each point
        h = classifiers[-1].classify(X) #calculate hypothesis #prev vote

        error = 0
        for i in range(0, Npts): #calculates error 
            ci = labels[i]
            hi = h[i]
            if hi == ci:
                delta = 1
            else:
                delta = 0 

            error += W[i] * (1-delta)
        
        alpha = (1/2) * (np.log(1 - error) - np.log(error))
        alphas.append(alpha)

        for i in range(0, Npts):
            ci = labels[i]
            hi = h[i]
            if hi == ci:
                W[i] = W[i] * np.exp(-alpha) 
            else:
                W[i] = W[i] * np.exp(alpha)
        
        W_sum = np.sum(W)
        W = W/W_sum #instead of using Z we normalize W in the end. 

        
    return classifiers, alphas

# in:       X - N x d matrix of N data points
# classifiers - (maximum) length T Python list of trained classifiers as above
#      alphas - (maximum) length T Python list of vote weights
#    Nclasses - the number of different classes
# out:  yPred - N vector of class predictions for test points
def classifyBoost(X, classifiers, alphas, Nclasses):
    Npts = X.shape[0]
    Ncomps = len(classifiers)

    # if we only have one classifier, we may just classify directly
    if Ncomps == 1:
        return classifiers[0].classify(X)
    else:
        votes = np.zeros((Npts,Nclasses))

        # TODO: implement classificiation when we have trained several classifiers!
        # here we can do it by filling in the votes vector with weighted votes
        # ==========================
        for t in range(Ncomps):
            classifier = classifiers[t]
            h = classifier.classify(X)

            for i, x in enumerate(h):
                votes[i][x] += alphas[t]
        # ==========================

        # one way to compute yPred after accumulating the votes
        return np.argmax(votes,axis=1)


# The implemented functions can now be summarized another classifer, the `BoostClassifier` class. This class enables boosting different types of classifiers by initializing it with the `base_classifier` argument. No need to add anything here.


# NOTE: no need to touch this
class BoostClassifier(object):
    def __init__(self, base_classifier, T=10):
        self.base_classifier = base_classifier
        self.T = T
        self.trained = False

    def trainClassifier(self, X, labels):
        rtn = BoostClassifier(self.base_classifier, self.T)
        rtn.nbr_classes = np.size(np.unique(labels))
        rtn.classifiers, rtn.alphas = trainBoost(self.base_classifier, X, labels, self.T)
        rtn.trained = True
        return rtn

    def classify(self, X):
        return classifyBoost(X, self.classifiers, self.alphas, self.nbr_classes)


# ## Run some experiments
# 
# Call the `testClassifier` and `plotBoundary` functions for this part.


#testClassifier(BoostClassifier(BayesClassifier(), T=10), dataset='iris',split=0.7)



#testClassifier(BoostClassifier(BayesClassifier(), T=10), dataset='vowel',split=0.7)



#plotBoundary(BoostClassifier(BayesClassifier()), dataset='vowel',split=0.7)


# Now repeat the steps with a decision tree classifier.


#testClassifier(DecisionTreeClassifier(), dataset='iris', split=0.7)



testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='iris',split=0.7)



#testClassifier(DecisionTreeClassifier(), dataset='vowel',split=0.7)



testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='vowel',split=0.7)



#plotBoundary(DecisionTreeClassifier(), dataset='iris',split=0.7)



plotBoundary(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='iris',split=0.7)


# ## Bonus: Visualize faces classified using boosted decision trees
# 
# Note that this part of the assignment is completely voluntary! First, let's check how a boosted decision tree classifier performs on the olivetti data. Note that we need to reduce the dimension a bit using PCA, as the original dimension of the image vectors is `64 x 64 = 4096` elements.


#testClassifier(BayesClassifier(), dataset='olivetti',split=0.7, dim=20)



#testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='olivetti',split=0.7, dim=20)


# You should get an accuracy around 70%. If you wish, you can compare this with using pure decision trees or a boosted bayes classifier. Not too bad, now let's try and classify a face as belonging to one of 40 persons!


#X,y,pcadim = fetchDataset('olivetti') # fetch the olivetti data
#xTr,yTr,xTe,yTe,trIdx,teIdx = trteSplitEven(X,y,0.7) # split into training and testing
#pca = decomposition.PCA(n_components=20) # use PCA to reduce the dimension to 20
#pca.fit(xTr) # use training data to fit the transform
#xTrpca = pca.transform(xTr) # apply on training data
#xTepca = pca.transform(xTe) # apply on test data
# use our pre-defined decision tree classifier together with the implemented
# boosting to classify data points in the training data
#classifier = BoostClassifier(DecisionTreeClassifier(), T=10).trainClassifier(xTrpca, yTr)
#yPr = classifier.classify(xTepca)
# choose a test point to visualize
#testind = random.randint(0, xTe.shape[0]-1)
# visualize the test point together with the training points used to train
# the class that the test point was classified to belong to
#visualizeOlivettiVectors(xTr[yTr == yPr[testind],:], xTe[testind,:])

