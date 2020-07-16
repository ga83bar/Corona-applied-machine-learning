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

## Computation
Before discussing the simple computation technique behind ELMs, it is reasonable to first discuss the processes behind the respective hidden neurons as well as a compact matrix notation. 

**Hidden Neurons:**
In general, the hidden neurons transform the underlying input data into a different representation. This is usually done in two steps:
1) The data is projected into the hidden layer using the input layer weights and biases
2) The projected data is transformed using a non-linear transformation function. 

In particular, using above non-linear transformation, the learning capabilities of the ELM can be greatly increased. After transformation, the data in the hidden layers h_I can be used to find the output layer weights. Another practical advantage is that the respective transformation functions are not constrained by type, that is they can be selected to be very different and even non-existent. Furthermore, since the neurons are linear, they consequently adapt and learn linear dependencies between data features and targets which happens directly without any nonlinear approximation at all. With that in mind, it becomes clear that the number of neurons must equal the number of data features. 

Note however, that other types of neurons have also found application in ELMs such as RBF neurons with nonlinear projection functions. These can be used to compute predictions based on similar training data samples in order to solve tasks with some more complex dependencies between data features and targets.

**Compact Matrix Notation:**
ELMs exhibit a closed form solution in which the hidden neurons are comprised in a matrix H. The network structure itself though is not noticable in practice meaning that there is only a single matrix that describes the projection between two - usually linear - spaces. The projections for the input (X⋅W) and the output (H⋅β) are connected through a nonlinear transformation as follows.

<img src="/documentation/Machine Learning Models/images/nonlinear_trafo.png" alt="Nonlinear Transformation" width="100"/>

The number of hidden neurons thus consequently regulates the size of the matrices W, H and β. However, the network neurons are never treated separately. With different types of hidden neurons, the first projection and transformation are performed independently for each type of neuron. Then the resulting sub-matrices H_1 are concatenated along the second dimension. For two types of hidden neurons it follows that 

<img src="/documentation/Machine Learning Models/images/H_1.png" alt="H Notation" width="300"/>

where linear neurons are added by simply copying the inputs into the hidden layer outpus

<img src="/documentation/Machine Learning Models/images/H_2.png" alt="Extended H Notation" width="300"/>

**Solution Computation:**
In general, ELM problems are usually over-determined (N>L) with the number of training data samples being much larger than the number of selected hidden neurons. In all other cases (N<=L), regularization should be used in order to obtain a better generalization performance. 

Nevertheless, a unique solution can be found using the pseudoinverse: 

<img src="/documentation/Machine Learning Models/images/H_solution.png" alt="Solution Computation" width="140"/>

## Conclusion
In order to summarize, ELMs have very promising and efficient properties. They have been proven to be very useful for regression tasks as needed in our project. Nevertheless, there have been some reports on negative effects such as 

* Bad initial randomization
* Speedy performance but low accuracy
* Need of regularization options

In particular, it has to be pointed out that ELMs only operate on one hidden layer in contrast to general DL approaches. In order to achieve a very high accuracy and approximation, this might not be necessarily the best performing choice considering the amount of COVID-19 data that we have gathered throughout the collection process. 

Nevertheless, there are two very high-performance Matlab and Python implementations of ready-to-use toolboxes discussed in above articles. They promise automatic model structure selection as well as the application of regularization techniques. Furthermore, many approaches using self-written Python code have emerged online. 

However, the main argument that seems to disqualify ELMs - from a user point of view - is that only one group member has even had any experience at all using them. Furthermore, even though the concepts of ELMs seem promising and effective, most of the ML experience was simply gained in Python using tensorflow and pytorch. The goal thus remains to find a time series modeling approach which exploits the vast availability of pre-built functions in these aforementioned frameworks.  

# Gaussian Processes (GP)

Another very promising approach which solves regressional time series problems is the use of Gaussian Processes (GP) for which a handful of implementations is given in the scikit ML library. In particular, there have already been attempts to model and forecast CO2 emissions using GPs, see [here](https://stats.stackexchange.com/questions/377999/why-are-gaussian-processes-valid-statistical-models-for-time-series-forecasting). This not only motivates to further investigate GPs for our project but also demonstrates a successful application, ultimately rendering this approach as highly plausible to achieve our specified project target. 

## GP Model
GPs are a very generic class of supervised learning methods which are designed to solve regression but also probabilitsic classification problems. In general, a GP is a stochastic process and thus a collection of random variables in the time or space domain. Note that every such finite collection of random variables has a multivariate normal distribution, that is every finite linear combination of these random variables is strictly normally distributed. As such, every GP can be compactly described by the joint distribution of all those random variables and is thus strictly specified by its mean and covariance functionals.

A GP can thus be described as a functional mapping of random variables x_i

<img src="/documentation/Machine Learning Models/images/GP_mapping.png" alt="GP Mapping" width="200"/>

with its respective mean function m(x)

<img src="/documentation/Machine Learning Models/images/GP_mean.png" alt="GP Mean" width="200"/>

and covariance function k(x, x')

<img src="/documentation/Machine Learning Models/images/GP_cov.png" alt="GP Covariance" width="200"/>

ML algorithms that make use of GPs most often use lazy learning approaches in order to measure the similarity between evaluation points. To this, the so-called kernel function is examined which aids to predict the value for a future, e.g. time series point. The so obtained prediction is not just an estimation but also containes some uncertainty information which is embedded in the one-dimensional Gaussian distribution. The same holds for multidimensional predictions where the GP is multivariate and for which the respective multivariate Gaussian distributions are the corresponding marginal distributions at the current evaluation point. 

## Pros and Cons
The advantages of GP models can mainly be summarized as:
* Prediction interpolates between the observations for regular kernels
* Prediction is probabilistic and allows for an analysis of confidence intervals which in turn aids to decide whether refitting is necessary. The latter one can thus be solved in an online fashion. 
* Versatitlity due to the possibility to choose differently specified kernels. 

However, some disadvantages of GP models are:
* Non-sparsity: The models use the whole sample and feature information in order to perform a prediction
* Low efficiency in high-dimensional spaces (especially when the number of features exceeds a few dozens)

## Conclusion
While GP models bring many different advantages and also are quite broady represented in the desired toolboxes to be used during the project, once again only few group members have actively dealt with both the theory and practical implementation of such models. As such, diving deeper in the more complex stochastic modeling will certainly take up more time than we initially desired to give for the ML core selection. As such, we decide that more time should be spent analyzing, optimizing and troubleshooting the model output which is frankly the more important part for a successful model application. To this, the more simple the model the better and since most of the group members have gained experience in DL modeling scenarios, GP models will not be further considered.  



# LSTM RNN 

# Conclusion
