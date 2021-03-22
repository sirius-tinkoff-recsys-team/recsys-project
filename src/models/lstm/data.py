import pandas as pd
import pytorch_lightning as pl

import torch
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence

from src.context import ctx
from src.config import params, config

def _extract_key_from_dict_list(d, key):
    return [i[key] for i in d]

def _pad_and_pack(sequence, sequence_lengths):
    sequence = list(map(torch.tensor, sequence))
    sequence = pad_sequence(sequence, batch_first=True)
    return sequence

def collate_fn(items):
    batch = dict()
    sequence_lengths = torch.tensor(_extract_key_from_dict_list(items, "sequence_lengths"))
    batch["sequence_lengths"] = sequence_lengths
    if "sequence" in items[0]:
        sequence = _extract_key_from_dict_list(items, "sequence")
        batch["sequence"] = _pad_and_pack(sequence, sequence_lengths)
    if "target" in items[0]:
        sequence = _extract_key_from_dict_list(items, "target")
        batch["target"] = _pad_and_pack(sequence, sequence_lengths)
    if "last_item" in items[0]:
        last_item = torch.tensor(_extract_key_from_dict_list(items, "last_item"))
        batch["last_item"] = last_item
    return batch

class BrightkiteDataset:
    def __init__(self, frame, kind="train"):
        assert kind in ["train", "valid"]
        self.frame = frame
        self.kind = kind
        self.present_indices = self.frame.index.get_level_values(0).unique()

    def __getitem__(self, idx):
        user_history = self.frame.loc[self.present_indices[idx]]
        loc_id_sequence = user_history.loc_id.values
        item = dict()
        if self.kind == "train":
            item["sequence"] = loc_id_sequence[:-2]
            item["target"] = loc_id_sequence[1:-1]
            item["sequence_lengths"] = len(loc_id_sequence) - 2
        else:
            item["sequence"] = loc_id_sequence[:-1]
            item["target"] = loc_id_sequence[1:]
            item["last_item"] = loc_id_sequence[-1]
            item["sequence_lengths"] = len(loc_id_sequence) - 1
        return item

    def __len__(self):
        return len(self.present_indices)

class BrightkiteDataModule(pl.LightningDataModule):
    def train_dataloader(self):
        train_frame = pd.read_csv(ctx.data_dir / "processed" / "train.csv", index_col=[0, 1])
        self.train_dataset = BrightkiteDataset(
            frame=train_frame,
            kind="train"
        )
        return DataLoader(
            dataset=self.train_dataset,
            batch_size=params.lstm.data.batch_size_train,
            num_workers=config.resources.dl_train.num_workers,
            collate_fn=collate_fn,
        )
    
    def val_dataloader(self):
        # valid_frame = pd.read_csv(ctx.data_dir / "processed" / "test.csv", index_col=[0, 1])
        train_frame = pd.read_csv(ctx.data_dir / "processed" / "train.csv", index_col=[0, 1])
        self.valid_dataset = BrightkiteDataset(
            frame=train_frame,
            kind="valid"
        )
        return DataLoader(
            dataset=self.valid_dataset,
            batch_size=params.lstm.data.batch_size_valid,
            num_workers=config.resources.dl_valid.num_workers,
            collate_fn=collate_fn,
        )
