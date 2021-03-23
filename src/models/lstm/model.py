import numpy as np
import pandas as pd
import pytorch_lightning as pl
from sklearn.metrics import top_k_accuracy_score

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts, ReduceLROnPlateau
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from src.context import ctx
from src.config import params, config
from src.logger import logger

class LSTMModel(pl.LightningModule):
    def __init__(self, num_items):
        super().__init__()

        self.num_items = num_items

        self.item_embedding = nn.Embedding(
            num_embeddings=self.num_items,
            embedding_dim=params.lstm.model.embedding_dim,
            padding_idx=0,
        )
        self.model = nn.LSTM(
            input_size=params.lstm.model.embedding_dim,
            hidden_size=params.lstm.model.hidden_dim,
            num_layers=params.lstm.model.num_layers,
            batch_first=True,
            dropout=params.lstm.model.dropout,
        )
        self.linear = nn.Linear(params.lstm.model.hidden_dim, num_items)
        
    def forward(self, batch):
        sequence = batch["sequence"]
        sequence_lengths = batch["sequence_lengths"]
        sequence = self.item_embedding(sequence)
        packed_sequence = pack_padded_sequence(sequence, sequence_lengths.cpu(), batch_first=True, enforce_sorted=False)
        hidden_states, last_hidden_state = self.model(packed_sequence)
        padded_sequence, _ = pad_packed_sequence(hidden_states, batch_first=True)
        logits = self.linear(padded_sequence)
        return logits
    
    def training_step(self, batch, batch_idx):
        sequence = batch["sequence"]
        sequence_lengths = batch["sequence_lengths"]
        target = batch["target"]
        logits = self.forward(batch)
        loss = self.criterion(logits, target, sequence_lengths)
        logger.log_metric("train_loss", loss.item())
        return {"loss": loss}
        
    def training_epoch_end(self, outputs):
        train_loss_mean = torch.stack([x["loss"] for x in outputs]).mean()

        logs = {
            "train_loss": train_loss_mean,
        }

        for key, value in logs.items():
            logger.log_metric(key, value.item(), dvc=True)

        logger.next_epoch()
        return

    def validation_step(self, batch, batch_idx):
        sequence = batch["sequence"]
        sequence_lengths = batch["sequence_lengths"]
        target = batch["target"]
        last_items = batch["last_item"]
        logits = self.forward(batch)
        loss = self.criterion(logits, target, sequence_lengths)
        last_item_predictions = torch.softmax(logits[:, -1], dim=1)
        accuracies = {
            f"valid_acc@{k}": top_k_accuracy_score(
                last_items, 
                last_item_predictions, 
                k=k, 
                labels=np.arange(self.num_items)
            )
            for k in [20, 50, 100]
        }
        return {"valid_loss": loss, **accuracies}

    def validation_epoch_end(self, outputs):
        valid_loss_mean = torch.stack([x["valid_loss"] for x in outputs]).mean()

        logs = {
            "valid_loss": valid_loss_mean,
        }

        for k in [20, 50, 100]:
            logs[f"valid_acc@{k}"] = np.mean([x[f"valid_acc@{k}"] for x in outputs])

        for key, value in logs.items():
            logger.log_metric(key, value.item(), dvc=True)

        return

    def criterion(self, logits, targets, sequence_lengths):
        mask = torch.zeros_like(targets).float()
        targets = targets.view(-1)

        predictions = torch.log_softmax(logits, dim=2)
        predictions = predictions.view(-1, self.num_items)

        for row, col in enumerate(sequence_lengths):
            mask[row, :col.item()] = 1.
        mask = mask.view(-1)

        valid_items = int(torch.sum(mask).item())
        predictions = predictions[range(predictions.shape[0]), targets] * mask
        ce_loss = - torch.sum(predictions) / valid_items
        return ce_loss

    def configure_optimizers(self):
        self.optimizer = Adam(self.model.parameters(), lr=params.lstm.optimizer.learning_rate)
        return self.optimizer
