import torch

conf_mask = torch.FloatTensor([10.0, 1.0, 0.0, 1.0, 1.0])
conf_data = torch.FloatTensor([0.1, 0.9, 0.0, 0.2, 0.2])

loss_fn = torch.nn.MSELoss()  # reduce=False, size_average=False)

x= loss_fn(conf_mask, conf_mask).item()

print(x)