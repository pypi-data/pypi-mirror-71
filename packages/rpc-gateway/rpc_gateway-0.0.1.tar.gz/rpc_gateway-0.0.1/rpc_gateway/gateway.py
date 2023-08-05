from typing import Optional, List, Dict
import logging
import asyncio
import websockets
from rpc_gateway import messages, errors
from rpc_gateway.message_pump import MessagePump

logger = logging.getLogger(__name__)


class GatewayConnection:
    def __init__(self, gateway: 'Gateway', connection: websockets.WebSocketServerProtocol):
        self.gateway = gateway
        self.connection = connection
        self.message_pump = MessagePump(connection, lambda message: gateway.handle_request(self, message))
        self.instances: List[str] = []

    async def start(self):
        await self.message_pump.start()

    async def stop(self):
        await self.message_pump.stop()

    def register_instances(self, instances):
        self.instances = list(set(*self.instances, *instances))


class Gateway:
    SERVER_MESSAGES = (messages.Method.GET, messages.Method.SET, messages.Method.CALL)

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.logger = logger.getChild(self.__class__.__name__)
        self.gateway_connections: Dict[websockets.WebSocketCommonProtocol, GatewayConnection] = {}
        self.websocket: Optional[websockets.WebSocketServer] = None
        self.websocket_task: Optional[asyncio.Task] = None
        self.event_loop = asyncio.get_event_loop()
        self.instances: Dict[str, GatewayConnection] = {}

    def start(self, wait = True):
        self.event_loop.run_until_complete(self._start(wait))

    async def _start(self, wait = True):
        self.logger.info(f'Starting on ws://{self.host}:{self.port}')
        self.websocket = await websockets.serve(self.on_connection, self.host, self.port)
        self.websocket_task = asyncio.Task(self.websocket.wait_closed())

        if wait:
            await self._wait()

    def wait(self):
        self.event_loop.run_until_complete(self._wait())

    async def _wait(self):
        if self.websocket_task is not None:
            await self.websocket_task

        self.logger.info(f'Done')

    def stop(self):
        self.event_loop.run_until_complete(self._stop())

    async def _stop(self):
        await asyncio.gather(*[gateway_connection.stop() for w, gateway_connection in self.gateway_connections.items()])
        self.websocket_task.cancel()

    async def on_connection(self, connection: websockets.WebSocketServerProtocol, path: str):
        gateway_connection = self.gateway_connections[connection] = GatewayConnection(self, connection)
        await gateway_connection.start()
        self.gateway_connections.pop(connection)

    #
    # Request Handlers
    #

    async def handle_forward_request(self, gateway_connection: GatewayConnection, request: messages.Request) -> messages.Response:
        self.logger.debug(f'Forwarding request to server: {request}')
        server = self.instances[request.data['instance']]
        response = await server.message_pump.request(request, raise_error=False)
        self.logger.debug(f'Forwarding response to client: {response}')

        return response

    async def handle_available_request(self, gateway_connection: GatewayConnection, request: messages.Request) -> messages.Response:
        available = request.data['instance'] in self.instances
        return messages.Response(data=available)

    async def handle_register_request(self, gateway_connection: GatewayConnection, request: messages.Request) -> messages.Response:
        self.logger.debug(f'Registering instances: {request.data}')
        gateway_connection.register_instances(request.data)
        for instance_name in request.data:
            self.instances[instance_name] = gateway_connection

        return messages.Response()

    # this is called by the GatewayConnection MessagePump when a new request is received
    async def handle_request(self, gateway_connection: GatewayConnection, request: messages.Request) -> messages.Response:
        if request.method in self.SERVER_MESSAGES:
            return await self.handle_forward_request(gateway_connection, request)

        if request.method == messages.Method.AVAILABLE:
            return await self.handle_available_request(gateway_connection, request)

        if request.method == messages.Method.REGISTER:
            return await self.handle_register_request(gateway_connection, request)

        return messages.Response(id=request.id, data=errors.InvalidMethodError(f'Invalid method: {request.method}'))


class GatewayClient:
    def __init__(self, gateway_url: str = 'ws://localhost:8888'):
        self.logger = logger.getChild(self.__class__.__name__)
        self.gateway_url = gateway_url
        self.message_pump = MessagePump(request_handler=self._handle_request)
        self.event_loop = asyncio.get_event_loop()

    @property
    def connected(self) -> bool:
        return self.message_pump.connection is not None

    def start(self, wait=True):
        self.event_loop.run_until_complete(self._start(wait))

    async def _start(self, wait=True):
        self.connection = await websockets.connect(self.gateway_url)
        await self.message_pump.start(wait=False, connection=self.connection)
        await self._on_start()

        if wait:
            await self._wait()

    def wait(self):
        self.event_loop.run_until_complete(self._wait())

    async def _wait(self):
        await self.message_pump.wait()

    async def _on_start(self):
        pass

    def stop(self):
        self.event_loop.run_until_complete(self._stop())

    async def _stop(self):
        await self.message_pump.stop()

    async def _handle_request(self, request: messages.Request) -> messages.Response:
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    gateway = Gateway()
    gateway.start()