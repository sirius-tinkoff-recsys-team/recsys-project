import pickle

import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint

from src.models.lstm.data import BrightkiteDataModule
from src.models.lstm.model import LSTMModel
from src.logger import init_logger
from src.config import params

def train():
    init_logger(tags=["debug"])

    num_items = _get_num_items()
    model = LSTMModel(num_items)
    dm = BrightkiteDataModule()

    checkpoint_callback = ModelCheckpoint(
        dirpath="artifacts",
        filename="lstm",
        save_top_k=-1,
    )

    trainer = pl.Trainer(
        checkpoint_callback=checkpoint_callback,
        deterministic=True,
        logger=False,
        max_epochs=params.lstm.optimizer.epochs,
    )

    trainer.fit(model, dm)

def _get_num_items():
    encoders = pickle.load(open("artifacts/label_encoders.pkl", "rb"))
    num_items = len(encoders["loc_id"].classes_) + 1
    return num_items

if __name__ == "__main__":
    train()
