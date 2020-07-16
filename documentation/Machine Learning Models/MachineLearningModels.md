# Machine Learning Model Analysis
[[_TOC_]]

# Quick Summary
Predictive time series modeling is a more or less standard problem in the field of statistical modeling for which many different approaches exist. One of the main goals during the AMI project is to evaluate some of these candidate model approaches and to eventually decide for one that suits the project task at hand. This underlying document thus presents a quick & dirty analysis of three possible learning approaches and discusses their respective feasibility.  

# Extreme Learning Machines (ELMs)

One possible and very promising emerging approach to combat regression and classification problems is the utilization of Extreme Learning Machines (ELMs). While being not so prominent in traditional ML lectures, ELMs are widely known for a fairly good accuracy and extremely fast performance. The latter follows from the fact that the respective hidden neuron parameters do not need to be tuned during learning and are thus independent of the underlying training data set. More so, the hidden neurons are rather randomly generated which consequently implies a random initialization of its parameters such as input weights, biases, centers, etc. Still, the universal approximation capability holds, for which an arbitrary model accuracy - supposing that there are enough hidden neurons - can be achieved for the regression/classification task at hand.

The probably most distinct property embedded in the ELM nature is the non-iterative linear solution for the respective output weights. This is mainly due to the independence between the input and output weights, unlike in a backpropagation scenario. This ultimately renders ELMs to be very fast compared to similar MLP and SVM solutions. 

Most of the discussed concepts below can be re-read in the following articles: 
* [High-Performance Extreme Learning Machines:
A Complete Toolbox for Big Data Applications](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7140733) 
* [Extreme learning machine: Theory and applications](http://www.di.unito.it/~cancelli/retineu11_12/ELM-NC-2006.pdf) 
* [tfelm: a TensorFlow Toolbox for the Investigation of ELMs and
MLPs Performance](https://csce.ucmss.com/cr/books/2018/LFS/CSREA2018/ICA4128.pdf) 

## ELM Model
ELMs are fast training methods for single layer feed-forward neural networks (SLFN). Once again, this is because input weights W and biases b are randomly set and never adjusted. Consequently, the respective output weights β are independent. Furthermore, the randomness of the input layer weights improves the generalization property w.r.t. the solution of a linear output layer. The so induced orthogonality leads to almost orthogonal and thus weakly correlated hidden layer features. 

In general, we can define an ELM model as follows. Consider a set of N distinct training samples (x_i, t_i) where i ranges between 1 and N. The SLFN output equation with L hidden neurons can then be denoted as

<img src="/documentation/Machine Learning Models/images/SLFN_output.png" alt="SLFN Output Equation" width="200"/>

with φ being the activation function (usually a sigmoid), w_i the input weights and b_i the biases and β_i the respective output weights. Consequently, the relation between the network inputs x_i, the target outputs t_i and the estimated outputs y_i is given by

<img src="/documentation/Machine Learning Models/images/estimated_output.png" alt="Estimated Model Output" width="300"/>

where ε denotes the noise comprised of randon noise and certain dependencies on hidden variables excluded from the inputs x_i. This process can be re-examined in below figure.

<img src="/documentation/Machine Learning Models/images/SLFN_process.png" alt="ELM SLFN Process" width="500"/>


**Hidden Neurons:**
In general, the respective hidden neurons transform the underlying input data into a different representation. This is usually done in two steps:
1) The data is projected into the hidden layer using the input layer weights and biases
2) The projected data is transformed using a non-linear transformation function. 

In particular, using above non-linear transformation, the learning capabilities of the ELM can be greatly increased. After transformation, the data in the hidden layer h can be used to find the output layer weights


## Computation

## Conclusion

# Gaussian Processes

# Extreme Learning Machines

# Conclusion
