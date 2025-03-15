from livekit.agents import llm
from typing import Annotated
import logging
from db_driver import DBDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)


DB = DBDriver()


# Define a function that can be called by the assistant
class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
