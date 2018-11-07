import torch

v = 0.5  # 1-0.0001
v1 = v - 0.01
conf_mask = torch.FloatTensor([0, 0, 0, 0, 0])
b = torch.FloatTensor([0.1, 0.9, 0, 0.2, 0.2])
b2 = torch.FloatTensor([0.1, 0.5, 0, 0.2, 0.2])
loss_fn = torch.nn.BCELoss()  # reduce=False, size_average=False)

x = loss_fn(conf_mask, b).item()
print('-----0&1', x)

x1 = loss_fn(conf_mask[conf_mask == 0], b[conf_mask == 0]).item()
print('-------0', x1)
x2 = loss_fn(conf_mask[conf_mask == 0], b2[conf_mask == 0]).item()
print('-------1', x2)