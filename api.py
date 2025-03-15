from livekit.agents import llm


# Define a function that can be called by the assistant
class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
