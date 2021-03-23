import pickle

import pytorch_lightning as pl

from src.models.lstm.data import BrightkiteDataModule
from src.models.lstm.model import LSTMModel
from src.logger import init_logger
from src.config import params
from src.utils.lightning import DVCLiveCompatibleModelCheckpoint, DVCLiveNextStepCallback

def train():
    init_logger(tags=["debug"])

    num_items = _get_num_items()
    model = LSTMModel(num_items)
    dm = BrightkiteDataModule()

    checkpoint_callback = DVCLiveCompatibleModelCheckpoint(
        dirpath="artifacts",
        filename="lstm",
        save_top_k=-1,
    )

    dvclive_next_step_callback = DVCLiveNextStepCallback()

    trainer = pl.Trainer(
        checkpoint_callback=checkpoint_callback,
        deterministic=True,
        logger=False,
        max_epochs=params.lstm.optimizer.epochs,
        gpus=-1,
        callbacks=[dvclive_next_step_callback]
    )

    trainer.fit(model, dm)

def _get_num_items():
    encoders = pickle.load(open("artifacts/label_encoders.pkl", "rb"))
    num_items = len(encoders["loc_id"].classes_) + 1
    return num_items

if __name__ == "__main__":
    train()
