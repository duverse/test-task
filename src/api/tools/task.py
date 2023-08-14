"""
Video processing client task manager

TODO: Move this logic into pip package, that can be installed
 in both API & Celery services.
"""
import copy
import json
from typing import List, Optional
from dataclasses import dataclass

from redis import Redis
from celery import Celery


class UndefinedTaskID(Exception):
    """If the requested pipeline ID is not defined"""


@dataclass
class TaskState:
    """Scheduled task state model"""
    id: str
    start_time: float
    frames_count: Optional[int]

    manager: 'TaskManager'

    @property
    def redis_frames_key(self) -> str:
        """Returns a key in redis where frames is stored"""
        return f'{self.id}_frames'

    @property
    def is_done(self) -> bool:
        """Returns True if processing is done"""
        return self.frames_count == self.processed_frames_count()

    def to_dict(self) -> dict:
        """Serialize state to dict"""
        state_dict = copy.copy(self.__dict__)

        # Remove pipeline manager from state
        del state_dict['manager']

        return state_dict

    def list_frames(self) -> List[dict]:
        """Returns a list of frames stored for current state"""
        result = []
        for frame_json in self.manager.redis.lrange(self.redis_frames_key, 0, -1):
            result.append(json.loads(frame_json))

        return result

    def processed_frames_count(self) -> int:
        """Returns a number of frames that is already processed"""
        return self.manager.redis.llen(self.redis_frames_key)

    @classmethod
    def from_json(cls, data: str, task_manager: 'TaskManager') -> 'TaskState':
        """Load pipeline state from string"""
        return cls(manager=task_manager, **json.loads(data))


class TaskManager:
    """Video processing task client manager"""
    def __init__(self, celery: Celery, redis: Redis):
        self.celery = celery
        self.redis = redis

    def create_task(self, video_path: str) -> TaskState:
        """Start video processing pipeline"""
        celery_task = self.celery.send_task(
            name='app.init_pipeline',
            args=[video_path],
        )

        task_id = celery_task.get()
        return self.get_task(task_id)

    def get_task(self, task_id: str) -> TaskState:
        """Returns pipeline state"""
        state_json = self.redis.get(task_id)
        if not state_json:
            raise UndefinedTaskID(task_id)

        return TaskState.from_json(state_json, task_manager=self)
