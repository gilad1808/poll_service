
from pydantic import BaseModel, Field
from typing import Annotated

class PollCreateRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    options: list[Annotated[str, Field(min_length=1, max_length=255)]] = Field(
        min_length=2
    )

class PollUpdateRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)

class PollOptionResponse(BaseModel):
    id: int
    option_text: str

class PollResponse(BaseModel):
    id: int
    question: str
    options: list[PollOptionResponse]

class PollOptionResult(BaseModel):
    option_id: int
    option_text: str
    vote_count: int

class PollResultsResponse(BaseModel):
    poll_id: int
    options: list[PollOptionResult]
    total_votes: int

class PollResultsSummary(BaseModel):
    poll_id: int
    question: str
    options: list[PollOptionResult]

class UserPollAnswer(BaseModel):
    poll_id: int
    question: str
    option_id: int
    option_text: str


class UserAnswersResponse(BaseModel):
    user_id: int
    answers: list[UserPollAnswer]
    total_answered: int

class VoteCreateRequest(BaseModel):
    user_id: int = Field(gt=0)
    option_id: int = Field(gt=0)


class VoteResponse(BaseModel):
    id: int
    poll_id: int
    option_id: int
    user_id: int
