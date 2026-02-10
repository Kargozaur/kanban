from asyncio import Queue
from typing import Any


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connection: dict[int, set[Queue]] = {}

    async def subscribe(self, board_id: int) -> Queue:
        queue: Queue = Queue()
        if board_id not in self.active_connection:
            self.active_connection[board_id] = set()
        self.active_connection[board_id].add(queue)
        return queue

    async def unsubscribe(self, board_id: int, queue: Queue) -> None:
        if board_id in self.active_connection:
            self.active_connection[board_id].remove(queue)
            if not self.active_connection[board_id]:
                del self.active_connection[board_id]

    async def broadcast(self, board_id: int, message: dict[str, Any]) -> None:
        if board_id in self.active_connection:
            for queue in self.active_connection[board_id]:
                await queue.put(message)


connection_manager = ConnectionManager()
