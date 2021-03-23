from pytorch_lightning.callbacks import ModelCheckpoint

class DVCLiveCompatibleModelCheckpoint(ModelCheckpoint):
   def _get_metric_interpolated_filepath_name(
        self,
        monitor_candidates: Dict[str, Any],
        epoch: int,
        step: int,
        trainer,
        del_filepath: Optional[str] = None,
    ) -> str:
        filepath = self.format_checkpoint_name(epoch, step, monitor_candidates)
        return filepath
