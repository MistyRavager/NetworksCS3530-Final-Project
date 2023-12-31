from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Dict, Tuple
from enum import Enum


@dataclass_json
@dataclass
class Command:
    client_id: int
    op_id: int
    op: str


class MessageType(Enum):
    # client-replica
    REQUEST = 1
    RESPONSE = 2

    # replica-leader
    PROPOSE = 3
    DECISION = 4

    # leader-acceptor
    P1A = 5
    P1B = 6
    P2A = 7
    P2B = 8


@dataclass_json
@dataclass
class Message:
    type: MessageType


@dataclass_json
@dataclass
class Request(Message):
    command: Command


@dataclass_json
@dataclass
class Response(Message):
    command: Command
    result: str


@dataclass_json
@dataclass
class Propose(Message):
    slot: int
    command: Command


@dataclass_json
@dataclass
class Decision(Message):
    slot: int
    command: Command


@dataclass_json
@dataclass(order=True)
class Ballot:
    num: int
    leader_id: int


@dataclass_json
@dataclass
class P1A(Message):
    acceptor_id: int
    ballot: Ballot


@dataclass_json
@dataclass
class P1B(Message):
    leader_id: int
    acceptor_id: int
    ballot: Ballot
    accepted: List[Tuple[int, Ballot, Command]]


@dataclass_json
@dataclass
class P2A(Message):
    leader_id: int
    ballot: Ballot
    slot: int
    command: Command


@dataclass_json
@dataclass
class P2B(Message):
    leader_id: int
    acceptor_id: int
    ballot: Ballot
    slot: int
    command: Command
