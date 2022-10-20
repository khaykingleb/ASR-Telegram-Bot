"""Telegram bot message handlers."""

import io

import nemo.collections.asr as nemo_asr
import numpy as np
import torch
import torchaudio
import torchaudio.transforms as T  # NOQA
import tritonclient.grpc.aio as grpcclient
from aiogram import types
from omegaconf import OmegaConf

from . import bot, dp
from .. import cfg


async def get_wav(voice_buff: io.BytesIO) -> torch.Tensor:  # NOQA
    wav, sample_rate = torchaudio.load(voice_buff)
    resampler = T.Resample(sample_rate, 16_000, dtype=wav.dtype)
    return resampler(wav)


async def get_melspectrogram(wav: torch.Tensor) -> np.array:  # NOQA
    featurizer = nemo_asr.modules.audio_preprocessing.AudioToMelSpectrogramPreprocessor()
    kwargs = {"input_signal": wav, "length": torch.tensor(wav.shape[1]).unsqueeze(-1)}
    melspec, _ = featurizer(**kwargs)
    return np.array(melspec).astype(np.float32)


def ctc_decode(idxs: np.array, blank_token_idx: int = 28) -> str:  # NOQA
    config = OmegaConf.load(cfg.BASE_DIR / "model-repository" / "quartznet" / "config.yaml")
    idx_to_char = {idx: char for idx, char in enumerate(config["labels"])}
    encoded_text = []
    for i, idx in enumerate(idxs):
        idx = int(idx)
        if idx == blank_token_idx:
            continue
        if i > 0:
            if idxs[i] == idxs[i - 1]:
                continue
        encoded_text.append(idx)
    return "".join([idx_to_char[idx] for idx in encoded_text])


async def get_transcript(voice_buff: io.BytesIO) -> str:  # NOQA
    wav = await get_wav(voice_buff)
    melspec = await get_melspectrogram(wav)

    async with grpcclient.InferenceServerClient(url="inference-api:8001") as triton_client:
        input = grpcclient.InferInput("input__0", melspec.shape, "FP32")
        input.set_data_from_numpy(melspec)

        melspec_length = np.array(melspec.shape[-1], dtype=np.int32).repeat(1)
        length = grpcclient.InferInput("input__1", melspec_length.shape, "INT32")
        length.set_data_from_numpy(melspec_length)

        output = grpcclient.InferRequestedOutput("output__0")
        result = await triton_client.infer("quartznet", inputs=[input, length], outputs=[output])
        probs = result.as_numpy("output__0")[0]
        idxs = probs.argmax(1)
        return ctc_decode(idxs)


@dp.message_handler(commands=["help"])
async def help(message: types.Message) -> None:  # NOQA
    await message.answer(
        "{user_name}, this is a bot to transcribe your voice messages 🔉. "
        "To use it, record yourself 🎙️. Within seconds, you'll get the transcription of your speech 🗣️.".format(
            user_name=message.from_user.first_name
        )
    )


@dp.message_handler(content_types=["voice"])
async def get_voice(message: types.Message) -> None:  # NOQA
    info = await bot.get_file(message.voice.file_id)
    voice_buff = await bot.download_file(info.file_path)
    transciption = await get_transcript(voice_buff)
    await bot.send_message(
        chat_id=message.from_user.id,
        text=transciption,
        reply_to_message_id=message.message_id,
    )


@dp.message_handler()
async def echo(message: types.Message) -> None:  # NOQA
    await message.answer(
        "Please, do not send text messages 📝🙅‍♂️. "
        "This is just an inline bot 🤖. You can only transcribe 📃 your voice messages 🗣️. "
        "Use /help for information how to use the bot 🤖."
    )
