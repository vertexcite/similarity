# Copyright 2021 The TensorFlow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from tensorflow_similarity.distances import Distance, distance_canonicalizer
from tensorflow_similarity.types import FloatTensor


class Search(ABC):
    def __init__(
        self,
        distance: Distance | str,
        dim: int,
        verbose: int = 0,
        name: str | None = None,
        **kwargs,
    ):
        """Initializes a nearest neigboors search index.

        Args:
            distance: the distance used to compute the distance between
            embeddings.

            dim: the size of the embeddings.

            verbose: be verbose.
        """
        self.distance: Distance = distance_canonicalizer(distance)
        self.dim = dim
        self.verbose = verbose
        self.name = name if name is not None else self.__class__.__name__

    @abstractmethod
    def add(self, embedding: FloatTensor, idx: int, verbose: int = 1, **kwargs):
        """Add a single embedding to the search index.

        Args:
            embedding: The embedding to index as computed by
            the similarity model.

            idx: Embedding id as in the index table.
            Returned with the embedding to allow to lookup
            the data associated with a given embedding.

        """

    @abstractmethod
    def batch_add(self, embeddings: FloatTensor, idxs: Sequence[int], verbose: int = 1, **kwargs):
        """Add a batch of embeddings to the search index.

        Args:
            embeddings: List of embeddings to add to the index.

            idxs (int): Embedding ids as in the index table. Returned with
            the embeddings to allow to lookup the data associated
            with the returned embeddings.

            verbose: Be verbose. Defaults to 1.
        """

    @abstractmethod
    def lookup(self, embedding: FloatTensor, k: int = 5) -> tuple[list[int], list[float]]:
        """Find embedding K nearest neighboors embeddings.

        Args:
            embedding: Query embedding as predicted by the model.
            k: Number of nearest neighboors embedding to lookup. Defaults to 5.
        """

    @abstractmethod
    def batch_lookup(self, embeddings: FloatTensor, k: int = 5) -> tuple[list[list[int]], list[list[float]]]:
        """Find embeddings K nearest neighboors embeddings.

        Args:
            embedding: Batch of query embeddings as predicted by the model.
            k: Number of nearest neighboors embedding to lookup. Defaults to 5.
        """

    @abstractmethod
    def save(self, path: str):
        """Serializes the index data on disk

        Args:
            path: where to store the data
        """

    @abstractmethod
    def load(self, path: str):
        """load index on disk

        Args:
            path: where to store the data
        """

    @abstractmethod
    def reset(self):
        "Remove all data, as if the instance were just created empty"

    def get_config(self) -> dict[str, Any]:
        """Contains the search configuration.

        Returns:
            A Python dict containing the configuration of the search obj.
        """
        config = {
            "distance": self.distance.name,
            "dim": self.dim,
            "verbose": self.verbose,
            "name": self.name,
            "canonical_name": self.__class__.__name__,
        }

        return config

    @abstractmethod
    def is_built(self):
        "Returns whether or not the index is built and ready for querying." ""
