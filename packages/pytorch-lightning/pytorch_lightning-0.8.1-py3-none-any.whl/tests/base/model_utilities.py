from torch.utils.data import DataLoader

from tests.base.datasets import TrialMNIST


class ModelTemplateData:
    hparams: ...

    def dataloader(self, train):
        dataset = TrialMNIST(root=self.data_root, train=train, download=True)

        loader = DataLoader(
            dataset=dataset,
            batch_size=self.batch_size,
            num_workers=3,
            shuffle=train,
        )
        return loader


class ModelTemplateUtils:

    def get_output_metric(self, output, name):
        if isinstance(output, dict):
            val = output[name]
        else:  # if it is 2level deep -> per dataloader and per batch
            val = sum(out[name] for out in output) / len(output)
        return val
