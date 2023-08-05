from typing import Optional, Dict, Any, Callable, Awaitable
import asyncio
import pickle
import logging
import websockets
from rpc_gateway import messages, errors

logger = logging.getLogger(__name__)
RequestHandlerType = Callable[[messages.Request], Awaitable[messages.Response]]
MAX_MESSAGE_ID = 99999
last_message_id = 0


def next_message_id() -> int:
    global last_message_id
    last_message_id += 1
    return last_message_id % MAX_MESSAGE_ID


class MessagePump:
    next_id = 0

    def __init__(self,
                 connection: Optional[websockets.WebSocketCommonProtocol] = None,
                 request_handler: Optional[RequestHandlerType] = None,
                 message_queues: Optional[Dict[int, asyncio.Queue]] = None):
        self.id = MessagePump.next_id
        MessagePump.next_id += 1
        self.logger = logger.getChild(self.__class__.__name__)
        self.connection = connection
        self.request_handler = request_handler
        self.event_loop = asyncio.get_event_loop()
        self.message_pump_task: Optional[asyncio.Task] = None
        self.message_queues = {} if message_queues is None else message_queues
        self.running = False

    async def start(self, wait=True, connection: Optional[websockets.WebSocketCommonProtocol] = None):
        if connection is not None:
            self.connection = connection

        self.running = True
        self.message_pump_task = asyncio.Task(self.message_pump())

        if wait:
            await self.wait()

    async def wait(self):
        await self.message_pump_task

    async def stop(self):
        self.running = False
        await self.connection.close_connection()
        self.message_pump_task.cancel()

    async def send_message(self, message: messages.Message):
        if self.connection is None:
            raise errors.NotConnectedError('Must be connected to send message: {message}')

        self.logger.debug(f'[{self.id}] > {message}')
        await self.connection.send(message.to_pickle())

    async def send_request(self, method: str, data: Any = None):
        return await self.request(messages.Request(method=method, data=data))

    async def send_response(self, id: int, data: Any = None, status: int = messages.Status.SUCCESS):
        response = messages.Response(id=id, status=status, data=data)
        await self.send_message(response)

    async def send_error_response(self, id: int, error: Exception):
        response = messages.Response(id=id, status=messages.Status.ERROR, data=error)
        await self.send_message(response)

    async def request(self, request: messages.Request, raise_error=True) -> messages.Response:
        request.id = next_message_id()
        queue = self.message_queues[request.id] = asyncio.Queue()
        await self.send_message(request)
        response: messages.Response = await queue.get()
        self.message_queues.pop(request.id)

        if response.status == messages.Status.ERROR and raise_error:
            raise response.data

        return response

    async def handle_request(self, request: messages.Request):
        response = await self.request_handler(request)
        response.id = request.id
        await self.send_message(response)

    async def message_pump(self):
        while self.running:
            message_bytes = await self.connection.recv()
            message = pickle.loads(message_bytes)
            self.logger.debug(f'[{self.id}] < {message}')

            if isinstance(message, messages.Response):  # response
                if message.id not in self.message_queues:
                    raise errors.InvalidMessageIdError(f'No request found for response ID: {message.id}')

                queue = self.message_queues[message.id]
                await queue.put(message)

            elif isinstance(message, messages.Request):  # request
                if self.request_handler is not None:
                    asyncio.create_task(self.handle_request(message))

            else:
                raise errors.InvalidMessageError(f'Invalid message: {message}')
