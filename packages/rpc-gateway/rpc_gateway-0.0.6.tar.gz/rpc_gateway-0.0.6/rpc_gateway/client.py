from typing import Any
import logging
import asyncio
from rpc_gateway import errors, messages, gateway


class Client(gateway.GatewayClient):
    def send_request(self, method: str, data: Any = None) -> messages.Response:
        future = self.message_pump.send_request(method, data)
        return asyncio.get_event_loop().run_until_complete(future)

    def get_instance(self, instance_name) -> Any:
        if not self.connected:
            self.start(wait=False)

        client = self

        class _Proxy:
            def __getattr__(self, item):
                return client.get(instance_name, item)

            def __setattr__(self, key, value):
                return client.set(instance_name, key, value)

        return _Proxy()

    def proxy_method(self, instance_name, method_name):
        def _proxy_method(*args, **kwargs):
            return self.call(instance_name, method_name, args, kwargs)

        return _proxy_method

    def instance_available(self, instance_name: str) -> bool:
        response = self.send_request(messages.Method.AVAILABLE, instance_name)
        return response.data

    def call(self, instance_name, method_name, args, kwargs):
        response = self.send_request(messages.Method.CALL, {
            'instance': instance_name,
            'attribute': method_name,
            'args': args,
            'kwargs': kwargs
        })

        return response.data

    def get(self, instance_name, attribute_name):
        response = self.send_request(messages.Method.GET, {
            'instance': instance_name,
            'attribute': attribute_name
        })

        if response.status == messages.Status.METHOD:
            return self.proxy_method(instance_name, attribute_name)

        return response.data

    def set(self, instance_name, attribute_name, value):
        self.send_request(messages.Method.SET, {
            'instance': instance_name,
            'attribute': attribute_name,
            'value': value
        })

        return value


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    class TestClass:
        foo = 'bar'

        def method(self):
            return 'baz'

    client = Client()
    test: TestClass = client.get_instance('test')
    print(test.foo)
    # print(test.method())
    # print(test)
