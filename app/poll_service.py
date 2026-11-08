
from fastapi import HTTPException

from .poll_repo import (create_poll, get_poll_by_id, get_option_by_id, create_vote, get_vote_by_user_and_poll,
                        update_vote, update_poll_question, delete_poll, delete_votes_by_user_id,
                        get_vote_counts_by_poll_id, get_answers_by_user_id, get_all_poll_result_rows)

from .user_client import get_user_by_id

def create_new_poll(question: str, options: list[str]):
    poll_id = create_poll(question, options)

    return get_poll_by_id(poll_id)


def get_existing_poll(poll_id: int):
    poll = get_poll_by_id(poll_id)

    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    return poll

def get_poll_results(poll_id: int):
    get_existing_poll(poll_id)
    options = get_vote_counts_by_poll_id(poll_id)

    return {
        "poll_id": poll_id,
        "options": options,
        "total_votes": sum(option["vote_count"] for option in options),
    }

def get_user_answers(user_id: int):
    answers = get_answers_by_user_id(user_id)

    return {
        "user_id": user_id,
        "answers": answers,
        "total_answered": len(answers),
    }

def get_all_poll_results():
    polls_by_id = {}

    for row in get_all_poll_result_rows():
        poll_id = row["poll_id"]

        if poll_id not in polls_by_id:
            polls_by_id[poll_id] = {
                "poll_id": poll_id,
                "question": row["question"],
                "options": [],
            }

        if row["option_id"] is not None:
            polls_by_id[poll_id]["options"].append({
                "option_id": row["option_id"],
                "option_text": row["option_text"],
                "vote_count": row["vote_count"],
            })

    return list(polls_by_id.values())

def update_existing_poll(poll_id: int, question: str):
    update_poll_question(poll_id, question)
    return get_existing_poll(poll_id)

def delete_existing_poll(poll_id: int) -> None:
    if not delete_poll(poll_id):
        raise HTTPException(status_code=404, detail="Poll not found")

def delete_user_votes(user_id: int) -> None:
    delete_votes_by_user_id(user_id)

def create_new_vote(poll_id: int, option_id: int, user_id: int):
    validate_user(user_id)
    poll = get_poll_by_id(poll_id)

    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    option = get_option_by_id(option_id)

    if option is None:
        raise HTTPException(
            status_code=404,
            detail="Option not found"
        )

    if option["poll_id"] != poll_id:
        raise HTTPException(
            status_code=400,
            detail="Selected option does not belong to this poll"
        )

    existing_vote = get_vote_by_user_and_poll(poll_id, user_id)

    if existing_vote is not None:
        raise HTTPException(
            status_code=409,
            detail="User has already voted. Use PUT to update the vote."
        )

    vote_id = create_vote(poll_id, option_id, user_id)

    return {
        "id": vote_id,
        "poll_id": poll_id,
        "option_id": option_id,
        "user_id": user_id
    }


def update_existing_vote(poll_id: int, option_id: int, user_id: int):
    validate_user(user_id)
    poll = get_poll_by_id(poll_id)

    if poll is None:
        raise HTTPException(
            status_code=404,
            detail="Poll not found"
        )

    option = get_option_by_id(option_id)

    if option is None:
        raise HTTPException(
            status_code=404,
            detail="Option not found"
        )

    if option["poll_id"] != poll_id:
        raise HTTPException(
            status_code=400,
            detail="Selected option does not belong to this poll"
        )

    existing_vote = get_vote_by_user_and_poll(poll_id, user_id)

    if existing_vote is None:
        raise HTTPException(
            status_code=404,
            detail="Vote not found"
        )

    update_vote(poll_id, user_id, option_id)

    return {
        "id": existing_vote["id"],
        "poll_id": poll_id,
        "option_id": option_id,
        "user_id": user_id
    }


def validate_user(user_id: int):
    response = get_user_by_id(user_id)

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Could not validate user"
        )

    try:
        user = response.json()

    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail="Invalid response from User Service",
        ) from exc

    if not isinstance(user, dict) or not isinstance(user.get("is_registered"), bool):
        raise HTTPException(
            status_code=502,
            detail="Invalid response from User Service",
        )

    if user["is_registered"] is False:
        raise HTTPException(
            status_code=403,
            detail="User is not registered"
        )

    return user

