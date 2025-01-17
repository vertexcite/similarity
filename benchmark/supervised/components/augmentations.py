from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import keras_cv
import tensorflow as tf

AUGMENTATIONS = {}
AUGMENTATIONS["random_resized_crop"] = lambda p: keras_cv.layers.RandomCropAndResize(
    target_size=p.get("target_size", (227, 227)),
    crop_area_factor=p.get("crop_area_factor", (0.15625, 1.0)),
    aspect_ratio_factor=p.get("aspect_ratio_factor", (0.75, 1.333)),
)
AUGMENTATIONS["random_flip"] = lambda p: keras_cv.layers.RandomFlip(
    mode=p.get("mode", "horizontal"),
)
AUGMENTATIONS["center_crop"] = lambda p: tf.keras.layers.Resizing(
    height=p.get("height", 256),
    width=p.get("width", 256),
    crop_to_aspect_ratio=True,
)


# TODO(ovallis): Return type should be tuple[Callable[[FloatTensor], FloatTensor]], but
# mypy doesn't recogonize the return types of the callabels.
def make_augmentations(cfg: Mapping[str, Any]) -> tuple[Any, ...]:
    return tuple([AUGMENTATIONS[aug_id](params) for aug_id, params in cfg.items()])
