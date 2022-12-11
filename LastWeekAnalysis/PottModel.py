from itertools import combinations_with_replacement
import numpy as np
from tqdm import tqdm
from copy import deepcopy

x = combinations_with_replacement([-1,0,1], 18**2)
y = deepcopy(x)
length = sum([1 for ignore in y])
Configs = np.zeros((length, 18**2))
for i, elem in tqdm(enumerate(x)):
    Configs[i] = elem
print(Configs[5000])
# print(Configs)