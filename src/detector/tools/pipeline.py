"""
Video processing pipeline manager

TODO: Move this logic into pip package, that can be installed
 in both API & Celery services.
"""
import json
import string
import time
from typing import List, Optional
from dataclasses import dataclass

import nanoid
from redis import Redis
from celery import Celery


class UndefinedPipelineID(Exception):
    """If the requested pipeline ID is not defined"""


@dataclass
class PipelineState:
    """Pipeline state model"""
    id: str
    start_time: float
    frames_count: Optional[int]

    manager: 'PipelineManager'

    @property
    def frames_redis_list(self) -> str:
        """Returns a key in redis where frames is stored"""
        return f'{self.id}_frames'

    @property
    def is_done(self) -> bool:
        """Returns True if processing is done"""
        return self.frames_count == self.processed_frames_count()

    def to_dict(self) -> dict:
        """Serialize state to dict"""
        state_dict = self.__dict__

        # Remove pipeline manager from state
        del state_dict['manager']

        return state_dict

    def to_json(self) -> str:
        """Serialize pipeline state"""
        return json.dumps(self.to_dict())

    def commit(self):
        """Update state"""
        self.manager.update_state(self)

    def append_frame(self, objects: dict):
        """Appends processed frame to current state"""
        self.manager.redis.rpush(self.frames_redis_list, json.dumps(objects))

    def list_frames(self) -> List[dict]:
        """Returns a list of frames stored for current state"""
        result = []
        for frame_json in self.manager.redis.lrange(self.frames_redis_list, 0, -1):
            result.append(json.loads(frame_json))

        return result

    def processed_frames_count(self) -> int:
        """Returns a number of frames that is already processed"""
        return self.manager.redis.llen(self.frames_redis_list)

    @classmethod
    def from_json(cls, data: str, pipeline_manager: 'PipelineManager') -> 'PipelineState':
        """Load pipeline state from string"""
        return cls(manager=pipeline_manager, **json.loads(data))


class PipelineManager:
    """Video processing pipeline manager"""
    def __init__(self, celery: Celery, redis: Redis):
        self.celery = celery
        self.redis = redis

    def create_state(self) -> PipelineState:
        """Initializes pipeline ID"""
        # Generate pipeline ID
        pipeline_id = nanoid.generate(string.ascii_letters, 12)

        # Initialize new state
        state = PipelineState(
            id=pipeline_id,
            start_time=time.time(),
            frames_count=None,
            manager=self,
        )

        # Save state
        state.commit()

        return state

    def update_state(self, state: PipelineState):
        """Update pipeline state"""
        self.redis.set(state.id, state.to_json())

    def get_state(self, state_id: str) -> PipelineState:
        """Returns pipeline state"""
        state_json = self.redis.get(state_id)
        if not state_json:
            raise UndefinedPipelineID(state_id)

        return PipelineState.from_json(state_json, pipeline_manager=self)
