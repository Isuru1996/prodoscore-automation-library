import logging
from dataclasses import dataclass, field

from automation_lib.core.logger import Logger


@dataclass
class BaseModel:
    model_name: str = "BaseModel"
    logger: logging.Logger = field(init=False, repr=False)

    def __post_init__(self):
        """Initialize logger after dataclass fields are set."""
        self.logger = Logger.get_logger(self.model_name)
