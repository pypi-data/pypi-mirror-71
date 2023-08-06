from abc import ABC

import pyro
import pyro.distributions as dist
import torch

from ccmf.model.base.model import Model


class LinearRecurrent(Model, ABC):
    def __init__(self, circuit, sigma_x):
        super().__init__(circuit)
        self.sigma_x = sigma_x

    def model(self):
        W = pyro.sample('W', self.prior['W'])
        M = pyro.sample('M', self.prior['M'])
        U = pyro.sample('U', self.prior['U'])
        EV = self.EV(W, M, U)
        EX = torch.cat([U, EV])

        for i, row in enumerate(EX):
            with pyro.poutine.mask(mask=self._mask[i]):
                pyro.sample(f'X{i}', dist.Normal(EX[i], self.sigma_x)).expand(self._mask[i].shape)

    def conditioned_model(self, X):
        return pyro.condition(self.model, data=X)()

    @staticmethod
    def EV(W, M, U):
        return torch.inverse(torch.eye(*M.shape) - M) @ W @ U

    def preprocess(self, X):
        df_X = [X.loc[i] for i in self._circuit.inputs + self._circuit.outputs]
        self._mask = [~torch.tensor(df_Xi.isna().values) for df_Xi in df_X]
        self.prior['U'] = self.prior['U'].expand(torch.Size([len(self._circuit.inputs), X.shape[1]]))
        return {f'X{i}': torch.tensor(df_Xi.fillna(0).values).float() for i, df_Xi in enumerate(df_X)}
