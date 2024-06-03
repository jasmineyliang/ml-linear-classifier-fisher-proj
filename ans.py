# -*- coding: utf-8 -*-
"""Submission of HW_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12nnGyIoknUFxp7cw6knK7F6hI6Ul90XY
"""

import numpy as np 
import matplotlib.pyplot as plt
import numpy # import again 
import matplotlib.pyplot # import again 
import numpy.linalg 
import numpy.random

def generate_data(Para1, Para2, seed=0):
    """Generate binary random data
    Para1, Para2: dict, {str:float} for each class, 
      keys are mx (center on x axis), my (center on y axis), 
               ux (sigma on x axis), ux (sigma on y axis), 
               y (label for this class)
    seed: int, seed for NUMPy's random number generator. Not Python's random.
    """
    numpy.random.seed(seed)
    X1 = numpy.vstack((numpy.random.normal(Para1['mx'], Para1['ux'], Para1['N']), 
                       numpy.random.normal(Para1['my'], Para1['uy'], Para1['N'])))
    X2 = numpy.vstack((numpy.random.normal(Para2['mx'], Para2['ux'], Para2['N']), 
                       numpy.random.normal(Para2['my'], Para2['uy'], Para2['N'])))
    Y = numpy.hstack(( Para1['y']*numpy.ones(Para1['N']), 
                       Para2['y']*numpy.ones(Para2['N'])  ))            
    X = numpy.hstack((X1, X2)) 
    X = numpy.transpose(X)
    return X, Y

def plot_mse(X, y, filename):
    """
    X: 2-D numpy array, each row is a sample, not augmented 
    y: 1-D numpy array
    Examples
    -----------------
    >>> X,y = generate_data(\
        {'mx':1,'my':2, 'ux':0.1, 'uy':1, 'y':1, 'N':20}, \
        {'mx':2,'my':4, 'ux':.1, 'uy':1, 'y':-1, 'N':50},\
        seed=10)
    >>> plot_mse(X, y, 'test1.png')
    array([-1.8650779 , -0.03934209,  2.91707992])
    >>> X,y = generate_data(\
    {'mx':1,'my':-2, 'ux':0.1, 'uy':1, 'y':1, 'N':20}, \
    {'mx':-1,'my':4, 'ux':.1, 'uy':1, 'y':-1, 'N':50},\
    seed=10)
    >>> # print (X, y)
    >>> plot_mse(X, y, 'test2.png')
    array([ 0.93061084, -0.01833983,  0.01127093])
    """
    w = np.array([0,0,0]) # just a placeholder
    # your code here

    X = X.transpose()
    X = numpy.vstack((X, numpy.ones(len(y))))
    compound = numpy.matmul(X, numpy.transpose(X))
    all_but_y = numpy.matmul(numpy.linalg.inv(compound), X)
    w = numpy.matmul(all_but_y, y)

    positivex=[]
    positivey=[]
    negativex=[]
    negativey=[]


    for i in range (len(y)):
      outcome = X[0,i] * w[0] +X[1,i]*w[1] + w[2]
      if outcome >=0 :
        positivex.append(X[0,i])
        positivey.append(X[1,i])

      else:
        negativex.append(X[0,i])
        negativey.append(X[1,i])

    positivex =np.array(positivex)
    positivey =np.array(positivey)
    negativex =np.array(negativex)
    negativey =np.array(negativey)

    # limit the range of plot to the dataset only
    matplotlib.pyplot.xlim(numpy.min(X[0]), numpy.max(X[0]))
    matplotlib.pyplot.ylim(numpy.min(X[1]), numpy.max(X[1]))
    
    
    x_ticks = numpy.array([numpy.min(X[0]), numpy.max(X[0])])
    y_ticks = -(x_ticks * w[0] +w[2])/w[1]
    plt.plot(x_ticks, y_ticks)

    plt.plot(positivex,positivey,'.b')
    plt.plot(negativex,negativey,'.r')
    plt.show()

    matplotlib.pyplot.savefig(filename)
    matplotlib.pyplot.close('all') # it is important to always clear the plot
    return w

def plot_fisher(X, y, filename):
  """
    X: 2-D numpy array, each row is a sample, not augmented 
    y: 1-D numpy array
    Examples
    -----------------
    >>> X,y = generate_data(\
        {'mx':1,'my':2, 'ux':0.1, 'uy':1, 'y':1, 'N':20}, \
        {'mx':2,'my':4, 'ux':.1, 'uy':1, 'y':-1, 'N':50},\
        seed=10)
    >>> plot_fisher(X, y, 'test3.png')
    array([-1.61707972, -0.0341108 ,  2.54419773])
    >>> X,y = generate_data(\
        {'mx':-1.5,'my':2, 'ux':0.1, 'uy':2, 'y':1, 'N':200}, \
        {'mx':2,'my':-4, 'ux':.1, 'uy':1, 'y':-1, 'N':50},\
        seed=1)
    >>> plot_fisher(X, y, 'test4.png')
    array([-1.54593468,  0.00366625,  0.40890079])
    """

  w = np.array([0,0,0]) # just a placeholder

  # your code here 
  class1=[]
  class2=[]

  for i in range (len(y)):
    if y[i] ==1 :
      class1.append(X[i])
    else:  
      class2.append(X[i])

  class1 = np.array(class1)
  class2 = np.array(class2)
  m1 = np.mean(class1, axis=0)
  m2 = np.mean(class2, axis=0)
  s1 = np.zeros((2,2))
  s2 = np.zeros((2,2))

  for i in range (len(class1[:,0])) :
    s1 += numpy.outer((class1[i] - m1),((class1[i]- m1).T))

  for i in range (len(class2[:,0])) :
    s2 += numpy.outer((class2[i] - m2),((class2[i]- m2).T))
  
  Sw = s1+s2
  invSw = np.linalg.inv(Sw)
  w = invSw.dot (m1-m2)
  wb=-(m1[0]*w[0]+m2[0]*w[0]+m1[1]*w[1]+m2[1]*w[1])/2
  w = numpy.append(w, wb)
  
  x_ticks = numpy.array([numpy.min(X[:,0]), numpy.max(X[:,0])])
  y_ticks = -(x_ticks * w[0] +w[2])/w[1]

  # limit the range of plot to the dataset only
  matplotlib.pyplot.xlim(numpy.min(X[:,0]), numpy.max(X[:,0]))
  matplotlib.pyplot.ylim(numpy.min(X[:,1]), numpy.max(X[:,1]))
  plt.plot(x_ticks, y_ticks)
  plt.plot(class1[:,0],class1[:,1],'.b')
  plt.plot(class2[:,0],class2[:,1],'.r')
  plt.show()

  matplotlib.pyplot.savefig(filename)
  matplotlib.pyplot.close('all')
  return w

if __name__ == "__main__":
    import doctest
    doctest.testmod()