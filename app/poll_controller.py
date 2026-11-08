
from fastapi import APIRouter

from .poll_dto import (PollCreateRequest, PollResponse, VoteCreateRequest, VoteResponse, PollUpdateRequest,
                       PollResultsResponse, UserAnswersResponse, PollResultsSummary)
from .poll_service import (create_new_poll, create_new_vote, get_existing_poll, update_existing_vote,
                           update_existing_poll, delete_existing_poll, delete_user_votes, get_poll_results,
                           get_user_answers, get_all_poll_results)


router = APIRouter(prefix="/polls", tags=["Polls"])


@router.post("", response_model=PollResponse, status_code=201)
def create_poll_endpoint(request: PollCreateRequest):
    return create_new_poll(request.question, request.options)

@router.get("/results", response_model=list[PollResultsSummary])
def get_all_poll_results_endpoint():
    return get_all_poll_results()

@router.get("/{poll_id}", response_model=PollResponse)
def get_poll_endpoint(poll_id: int):
    return get_existing_poll(poll_id)

@router.get("/{poll_id}/results", response_model=PollResultsResponse)
def get_poll_results_endpoint(poll_id: int):
    return get_poll_results(poll_id)

@router.get("/users/{user_id}/answers", response_model=UserAnswersResponse)
def get_user_answers_endpoint(user_id: int):
    return get_user_answers(user_id)

@router.patch("/{poll_id}", response_model=PollResponse)
def update_poll_endpoint(poll_id: int, request: PollUpdateRequest):
    return update_existing_poll(poll_id, request.question)

@router.delete("/{poll_id}", status_code=204)
def delete_poll_endpoint(poll_id: int) -> None:
    delete_existing_poll(poll_id)

@router.delete("/users/{user_id}/votes", status_code=204)
def delete_user_votes_endpoint(user_id: int) -> None:
    delete_user_votes(user_id)

@router.post(
    "/{poll_id}/votes",
    response_model=VoteResponse,
    status_code=201
)
def create_vote_endpoint(poll_id: int, request: VoteCreateRequest):
    return create_new_vote(
        poll_id,
        request.option_id,
        request.user_id
    )


@router.put(
    "/{poll_id}/votes",
    response_model=VoteResponse
)
def update_vote_endpoint(poll_id: int, request: VoteCreateRequest):
    return update_existing_vote(
        poll_id,
        request.option_id,
        request.user_id
    )
