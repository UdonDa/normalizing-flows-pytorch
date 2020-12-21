import os

import hydra
import numpy as np
import torch
import sklearn
import torchvision

N_DATASET_SIZE = 65536


def _sample_circles(n):
    samples, _ = sklearn.datasets.make_circles(N_DATASET_SIZE, noise=0.08, factor=0.5)
    return samples * 0.6


def _sample_moons(n):
    samples, _ = sklearn.datasets.make_moons(N_DATASET_SIZE, noise=0.08)
    samples = (samples - 0.5) / 2.0
    return samples


def _sample_normals(n):
    radius = 0.7
    n_normals = 8
    k = np.random.randint(n_normals, size=(n, ))
    cx = radius * np.cos(2.0 * np.pi * k / n_normals)
    cy = radius * np.sin(2.0 * np.pi * k / n_normals)
    dx, dy = np.random.normal(size=(2, n)) * 0.1
    x = cx + dx
    y = cy + dy
    samples = np.stack([x, y], axis=1)
    return samples


def _sample_swiss(n):
    samples, _ = sklearn.datasets.make_swiss_roll(n, noise=0.08)
    samples[:, 0] = samples[:, 0] * 0.07
    samples[:, 1] = samples[:, 1] * 0.07 - 1.0
    samples[:, 2] = samples[:, 2] * 0.07
    return samples


def _sample_s_curve(n):
    samples, _ = sklearn.datasets.make_s_curve(n, noise=0.08)
    samples[:, 0] = samples[:, 0] * 0.7
    samples[:, 1] = (samples[:, 1] - 1.0) * 0.7
    samples[:, 2] = samples[:, 2] * 0.35
    return samples


class FlowDataset(torch.utils.data.Dataset):
    def __init__(self, name='moons'):
        super(FlowDataset, self).__init__()
        self.name = name
        self.iter = 0
        self._initialize()

    def _initialize(self):
        data_root = os.path.join(hydra.utils.get_original_cwd(), 'data')
        if self.name == 'mnist':
            self.dset = torchvision.datasets.MNIST(root=os.path.join(data_root, 'mnist'),
                                                   train=True,
                                                   download=True)
            self.dims = (1, 28, 28)
            self.dtype = 'image'
        elif self.name == 'cifar10':
            self.dset = torchvision.datasets.CIFAR10(root=os.path.join(data_root, 'cifar10'),
                                                     train=True,
                                                     download=True)
            self.dims = (3, 32, 32)
            self.dtype = 'image'
        elif self.name == 'circles':
            self.dset = _sample_circles(N_DATASET_SIZE)
            self.dims = (2, )
            self.dtype = '2d'
            self.iter = N_DATASET_SIZE
        elif self.name == 'moons':
            self.dset = _sample_moons(N_DATASET_SIZE)
            self.dims = (2, )
            self.dtype = '2d'
            self.iter = N_DATASET_SIZE
        elif self.name == 'normals':
            self.dset = _sample_normals(N_DATASET_SIZE)
            self.dims = (2, )
            self.dtype = '2d'
            self.iter = N_DATASET_SIZE
        elif self.name == 'swiss':
            self.dset = _sample_swiss(N_DATASET_SIZE)
            self.dims = (3, )
            self.dtype = '3d'
            self.iter = N_DATASET_SIZE
        elif self.name == 's_curve':
            self.dset = _sample_s_curve(N_DATASET_SIZE)
            self.dims = (3, )
            self.dtype = '3d'
            self.iter = N_DATASET_SIZE
        else:
            raise Exception('unsupported type: "%s"' % self.name)

    def __len__(self):
        return len(self.dset)

    def __getitem__(self, idx):
        if self.dtype == 'image':
            data = self.dset[idx]
            data = np.asarray(data[0], dtype='float32') / 255.0
            data = data * 2.0 - 1.0
            data = np.reshape(data, (self.dims[1], self.dims[2], -1))
            data = np.transpose(data, axes=(2, 0, 1))
        else:
            self.iter -= 1
            data = self.dset[self.iter]
            data = data.astype('float32')
            if self.iter == 0:
                self._initialize()

        return data
