# Title
> summary


<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#mulearn" data-toc-modified-id="mulearn-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>mulearn</a></span><ul class="toc-item"><li><span><a href="#Install" data-toc-modified-id="Install-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Install</a></span></li><li><span><a href="#How-to-use" data-toc-modified-id="How-to-use-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>How to use</a></span></li></ul></li></ul></div>

# mulearn

mulearn is a python package implementing the data-driven induction of fuzzy sets described in

- D. Malchiodi and W. Pedrycz, _Learning Membership Functions for Fuzzy Sets through Modified Support Vector Clustering_, in F. Masulli, G. Pasi e R. Yager (Eds.), Fuzzy Logic and Applications. 10th International Workshop, WILF 2013, Genoa, Italy, November 19–22, 2013. Proceedings., Vol. 8256, Springer International Publishing, Switzerland, Lecture Notes on Artificial Intelligence.

## Install

`pip install mulearn`

## How to use

Fill me in please! Don't forget code examples:

```python
%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

source = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

iris_df = pd.read_csv(source, header=None)
iris_df.columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

iris_values = iris_df.iloc[:,0:4].values
iris_labels = iris_df.iloc[:,4].values

pca_2d = PCA(n_components=2)
iris_values_2d = pca_2d.fit_transform(iris_values)
```

```python
def gr_dataset(): 
    for lab, col in zip(('Iris-setosa', 'Iris-versicolor', 'Iris-virginica'),
                        ('blue', 'green', 'red')):
        plt.scatter(iris_values_2d[iris_labels==lab, 0],
                    iris_values_2d[iris_labels==lab, 1],
                    label=lab,
                    c=col)

gr_dataset()
```


![png](docs/images/output_7_0.png)


```python
def to_membership_values(labels, target):
    return [1 if l==target else 0 for l in labels]

mu = {}
for target in ('Iris-setosa', 'Iris-versicolor', 'Iris-virginica'):
    mu[target] = to_membership_values(iris_labels, target)
```

```python
def gr_membership_contour(estimated_membership):
    x = np.linspace(-4, 4, 50)
    y = np.linspace(-4, 4, 50)
    X, Y = np.meshgrid(x, y)
    zs = np.array([estimated_membership((x, y))
                   for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    membership_contour = plt.contour(X, Y, Z,
                                     levels=(.1, .3, .5, .95), colors='k')
    plt.clabel(membership_contour, inline=1)
    
```

```python
from mulearn import FuzzyInductor

f = FuzzyInductor()
f.fit(iris_values_2d, mu['Iris-virginica'])
gr_dataset()
gr_membership_contour(f.estimated_membership_)
plt.show()
```

    100%|██████████| 100/100 [00:16<00:00,  5.91it/s]



![png](docs/images/output_10_1.png)


```python
from mulearn import fuzzifier

f = FuzzyInductor(fuzzifier=(fuzzifier.LinearFuzzifier, {}))
f.fit(iris_values_2d, mu['Iris-virginica'])

gr_dataset()
gr_membership_contour(f.estimated_membership_)
plt.show()
```

    100%|██████████| 100/100 [00:19<00:00,  5.16it/s]



![png](docs/images/output_11_1.png)


```python
f = FuzzyInductor(fuzzifier=(fuzzifier.ExponentialFuzzifier,
                             {'profile': 'alpha', 'alpha': 0.25}))
f.fit(iris_values_2d, mu['Iris-virginica'])

gr_dataset()
gr_membership_contour(f.estimated_membership_)
plt.show()
```

    100%|██████████| 100/100 [00:20<00:00,  4.98it/s]



![png](docs/images/output_12_1.png)


```python
from mulearn import kernel

f = FuzzyInductor(k=kernel.GaussianKernel(.3))
f.fit(iris_values_2d, mu['Iris-virginica'])

gr_dataset()
gr_membership_contour(f.estimated_membership_)
plt.show()
```

    100%|██████████| 100/100 [00:20<00:00,  4.83it/s]



![png](docs/images/output_13_1.png)


```python
from mulearn import optimization as opt

try:
    f = FuzzyInductor(solve_strategy=(opt.solve_optimization_gurobi, {}))
    f.fit(iris_values_2d, mu['Iris-virginica'])

    gr_dataset()
    gr_membership_contour(f.estimated_membership_)
    plt.show()
except (ModuleNotFoundError, ValueError):
    print('Gurobi not available')
```

    Academic license - for non-commercial use only



![png](docs/images/output_14_1.png)


```python
f = FuzzyInductor(fuzzifier=(fuzzifier.ExponentialFuzzifier,
                             {'profile': 'alpha', 'alpha': 0.15}),
                  k=kernel.GaussianKernel(1.5),
                  solve_strategy=(opt.solve_optimization_tensorflow,
                                  {'n_iter': 20}),
                  return_profile=True)
f.fit(iris_values_2d, mu['Iris-virginica'])

gr_dataset()
gr_membership_contour(f.estimated_membership_)
plt.show()
```

    100%|██████████| 20/20 [00:04<00:00,  4.83it/s]



![png](docs/images/output_15_1.png)


```python
plt.plot(f.profile_[0], mu['Iris-virginica'], '.')
plt.plot(f.profile_[1], f.profile_[2])
plt.ylim((-0.1, 1.1))
plt.show()
```


![png](docs/images/output_16_0.png)


```python
sigmas = [.225,.5]
parameters = {'c': [1,10,100],
              'k': [kernel.GaussianKernel(s) for s in sigmas]}
```

```python
from sklearn.model_selection import GridSearchCV
from sklearn.exceptions import FitFailedWarning
import logging
import warnings

logging.getLogger('mulearn').setLevel(logging.ERROR)

f = FuzzyInductor()

with warnings.catch_warnings():
    warnings.simplefilter('ignore', FitFailedWarning)

    virginica = GridSearchCV(f, param_grid=parameters, cv=2)
    virginica.fit(iris_values_2d, mu['Iris-virginica'])
```

    100%|██████████| 100/100 [00:08<00:00, 11.99it/s]
    100%|██████████| 100/100 [00:08<00:00, 11.36it/s]
    100%|██████████| 100/100 [00:09<00:00, 10.92it/s]
    100%|██████████| 100/100 [00:09<00:00, 10.67it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.70it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.83it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.81it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.95it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.41it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.19it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.23it/s]
    100%|██████████| 100/100 [00:10<00:00,  9.42it/s]
    100%|██████████| 100/100 [00:18<00:00,  5.42it/s]


```python
gr_dataset()
gr_membership_contour(virginica.best_estimator_.estimated_membership_)
plt.show()
```


![png](docs/images/output_19_0.png)


```python
import pickle

saved_estimator = pickle.dumps(virginica.best_estimator_)
```

```python
loaded_estimator = pickle.loads(saved_estimator)

gr_dataset()
gr_membership_contour(loaded_estimator.estimated_membership_)
plt.show()
```


![png](docs/images/output_21_0.png)

