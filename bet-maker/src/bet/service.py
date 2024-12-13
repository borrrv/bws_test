import asyncio
import logging

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.grpc_event import grpc_client
from src.utils.cruds import CreateService, GetListService, UpdateService

from .database import Bet
from .enums import StatusBetEnum
from .models import GetOneDTO

logger = logging.getLogger(__name__)


class BetCreateService(CreateService):
    table = Bet
    response_model = GetOneDTO
    exchange = "bet_exchange"
    routing_key = "bet_key"

    @classmethod
    async def create_one(cls, session: AsyncSession, params: BaseModel) -> BaseModel:
        instance = await grpc_client.get_event_by_id(params.event_id)
        if len(instance) == 0:
            raise ValueError("Event not found")
        check_value = await grpc_client.event_check_time(params.event_id)
        if not check_value:
            raise ValueError("Time is up!")
        if params.bet_amount <= 0:
            raise ValueError("Amount must be positive")
        result = await super().create_one(session, params)
        return result


class BetGetListService(GetListService):
    table = Bet
    response_model = GetOneDTO

    @classmethod
    async def get_list(
        cls, session: AsyncSession, query=None, limit: int = 10, offset: int = 0
    ) -> list[BaseModel]:
        bets_list: list[GetOneDTO] = await super().get_list(
            session, query, limit, offset
        )

        async def get_event_for_bet(bet: GetOneDTO):
            event = await grpc_client.get_event_by_id(bet.event_id)
            return bet.event_id, event

        event_data = await asyncio.gather(
            *(get_event_for_bet(bet) for bet in bets_list)
        )

        event_dict = {event_id: event for event_id, event in event_data}
        for bet in bets_list:
            bet.event_id = event_dict.get(bet.event_id)

        return bets_list


class BetUpdateService(UpdateService):
    table = Bet
    enum_dict = {
        1: StatusBetEnum.NOT_PLAYED,
        2: StatusBetEnum.WIN,
        3: StatusBetEnum.LOSE,
    }

    @classmethod
    async def update(cls, session: AsyncSession, params: BaseModel) -> BaseModel:
        query_instance = select(cls.table).where(
            cls.table.event_id == params["event_id"]
        )
        result = await session.execute(query_instance)
        bets = result.scalars().all()
        for bet in bets:
            bet.status = cls.enum_dict[params["status"]]
        await session.commit()
