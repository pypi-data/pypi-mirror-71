# atml

atml tries to address the following problem: **Given a new data set, is there any toolkit that could help me quickly and conveniently come up with a good baseline model?**

# try it out

* Install from PyPi

```python
pip install atml
```

* Load the data set or use your own one

```python
import pandas as pd

df = pd.read_csv("./test/data/binary_data.csv")
X = df.drop('Survived', axis=1)

label_columns = ['Survived']
y = df[label_columns]
```

* Instantiate and run with AtmlController with default

```python
from atml import AtmlController

atml_c = AtmlController(with_default=True)
atml_c.run(X, y)
```

* Register a new Model and Hyper parameter space for tuning
```python
from atml import AtmlOrchestrator

atml_o = AtmlOrchestrator(with_default=True)

from sklearn.svm import SVC
sp = [
    {"property": "kernel", "type": "choice", "value": ["linear", "rbf"]},
    {"property": "gamma", "type": "choice", "value": ["scale", "auto"]}     
]
atml_o.auto_learning_socket.register(SVC(), sp)

atml_o.run(X, y)
'''