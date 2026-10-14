from pydantic import BaseModel, ConfigDict


class OptionCreate(BaseModel):
    text: str


class PollCreate(BaseModel):
    question: str
    options: list[OptionCreate]


class OptionResponse(BaseModel):
    id: int
    text: str
    votes: int

    model_config = ConfigDict(from_attributes=True)


class PollResponse(BaseModel):
    id: int
    question: str
    options: list[OptionResponse]

    model_config = ConfigDict(from_attributes=True)


class VoteResponse(BaseModel):
    message: str
    option: str
    votes: int