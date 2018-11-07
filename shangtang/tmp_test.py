
import torch
import torch.nn.functional as F
conf_mask = torch.FloatTensor([0.0, 1.0, 0.0, 1.0, 1.0])
conf_data = torch.FloatTensor([-20.1, -0.9, 0.0, 0.2,0.5,0.99, 2.2])

import torch
import torch.nn as nn

#inplace为True，将会改变输入的数据 ，否则不会改变原输入，只会产生新的输出
m = nn.LeakyReLU(inplace=True)


output = m(conf_data)
print(output)


print(torch.sigmoid(conf_data))
print(torch.tanh(conf_data))
print(F.softplus(conf_data))