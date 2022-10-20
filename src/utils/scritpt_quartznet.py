"""Transform PyTorch QuartzNet model into TorchScript."""

import nemo.collections.asr as nemo_asr
import torch

from .. import cfg

MODELS_PATH = cfg.BASE_DIR / "model-repository"
MODELS_PATH.mkdir(parents=True, exist_ok=True)


def main() -> None:  # NOQA
    quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")
    quartznet.export(MODELS_PATH / "quartznet" / "1" / "model.pt")

    featurizer = quartznet.preprocessor.featurizer
    wav = torch.rand(1, 2000)
    featurizer_traced_script = torch.jit.trace(
        featurizer,
        (wav, torch.tensor(wav.shape[1]).unsqueeze(-1)),
        check_trace=False,
    )
    featurizer_traced_script.save(MODELS_PATH / "featurizer.pt")


if __name__ == "__main__":  # NOQA
    main()
