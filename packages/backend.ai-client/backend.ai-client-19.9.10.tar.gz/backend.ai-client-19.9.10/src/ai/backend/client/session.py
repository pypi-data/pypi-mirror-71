import abc
import asyncio
import threading
import queue

import aiohttp

from .config import APIConfig, get_config
from .exceptions import BackendAPIError


__all__ = (
    'BaseSession',
    'Session',
    'AsyncSession',
)


def is_legacy_server():
    '''Determine execution mode.

    Legacy mode: <= v4.20181215
    '''
    with Session() as session:
        ret = session.Kernel.hello()
    bai_version = ret['version']
    legacy = True if bai_version <= 'v4.20181215' else False
    return legacy


class _SyncWorkerThread(threading.Thread):

    sentinel = object()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work_queue = queue.Queue()
        self.done_queue = queue.Queue()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            while True:
                coro = self.work_queue.get()
                if coro is self.sentinel:
                    break
                try:
                    result = loop.run_until_complete(coro)
                except Exception as e:
                    self.done_queue.put_nowait(e)
                else:
                    self.done_queue.put_nowait(result)
                self.work_queue.task_done()
        except (SystemExit, KeyboardInterrupt):
            pass
        finally:
            loop.stop()

    def execute(self, coro):
        self.work_queue.put(coro)
        result = self.done_queue.get()
        self.done_queue.task_done()
        if isinstance(result, Exception):
            raise result
        return result


class BaseSession(metaclass=abc.ABCMeta):
    '''
    The base abstract class for sessions.
    '''

    __slots__ = (
        '_config', '_closed', 'aiohttp_session',
        'Manager', 'Admin',
        'Agent', 'AgentWatcher', 'ScalingGroup',
        'Image', 'Kernel',
        'Domain', 'Group', 'Auth', 'User', 'KeyPair',
        'EtcdConfig',
        'Resource', 'KeypairResourcePolicy',
        'VFolder',
    )

    def __init__(
        self, *,
        config: APIConfig = None,
    ):
        self._closed = False
        self._config = config if config else get_config()

    @abc.abstractmethod
    def close(self):
        '''
        Terminates the session and releases underlying resources.
        '''
        raise NotImplementedError

    @property
    def closed(self) -> bool:
        '''
        Checks if the session is closed.
        '''
        return self._closed

    @property
    def config(self):
        '''
        The configuration used by this session object.
        '''
        return self._config


class Session(BaseSession):
    '''
    An API client session that makes API requests synchronously.
    You may call (almost) all function proxy methods like a plain Python function.
    It provides a context manager interface to ensure closing of the session
    upon errors and scope exits.
    '''

    __slots__ = BaseSession.__slots__ + (
        '_worker_thread',
    )

    def __init__(
        self, *,
        config: APIConfig = None,
    ):
        super().__init__(config=config)
        self._worker_thread = _SyncWorkerThread()
        self._worker_thread.start()

        async def _create_aiohttp_session():
            ssl = None
            if self._config.skip_sslcert_validation:
                ssl = False
            connector = aiohttp.TCPConnector(ssl=ssl)
            return aiohttp.ClientSession(connector=connector)

        self.aiohttp_session = self.worker_thread.execute(_create_aiohttp_session())

        from .base import BaseFunction
        from .admin import Admin
        from .agent import Agent, AgentWatcher
        from .auth import Auth
        from .etcd import EtcdConfig
        from .domain import Domain
        from .group import Group
        from .image import Image
        from .kernel import Kernel
        from .keypair import KeyPair
        from .manager import Manager
        from .resource import Resource
        from .keypair_resource_policy import KeypairResourcePolicy
        from .scaling_group import ScalingGroup
        from .user import User
        from .vfolder import VFolder

        self.Admin = type('Admin', (BaseFunction, ), {
            **Admin.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.admin.Admin` function proxy
        bound to this session.
        '''

        self.Agent = type('Agent', (BaseFunction, ), {
            **Agent.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.Agent` function proxy
        bound to this session.
        '''

        self.AgentWatcher = type('AgentWatcher', (BaseFunction, ), {
            **AgentWatcher.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.AgentWatcher` function proxy
        bound to this session.
        '''

        self.Auth = type('Auth', (BaseFunction, ), {
            **Auth.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.Auth` function proxy
        bound to this session.
        '''

        self.EtcdConfig = type('EtcdConfig', (BaseFunction, ), {
            **EtcdConfig.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.EtcdConfig` function proxy
        bound to this session.
        '''

        self.Domain = type('Domain', (BaseFunction, ), {
            **Domain.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.Domain` function proxy
        bound to this session.
        '''

        self.Group = type('Group', (BaseFunction, ), {
            **Group.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.Group` function proxy
        bound to this session.
        '''

        self.Image = type('Image', (BaseFunction, ), {
            **Image.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.image.Image` function proxy
        bound to this session.
        '''

        self.Kernel = type('Kernel', (BaseFunction, ), {
            **Kernel.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.kernel.Kernel` function proxy
        bound to this session.
        '''

        self.KeyPair = type('KeyPair', (BaseFunction, ), {
            **KeyPair.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.keypair.KeyPair` function proxy
        bound to this session.
        '''

        self.Manager = type('Manager', (BaseFunction, ), {
            **Manager.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.manager.Manager` function proxy
        bound to this session.
        '''

        self.Resource = type('Resource', (BaseFunction, ), {
            **Resource.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.resource.Resource` function proxy
        bound to this session.
        '''

        self.KeypairResourcePolicy = type('KeypairResourcePolicy', (BaseFunction, ), {
            **KeypairResourcePolicy.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.keypair_resource_policy.KeypairResourcePolicy` function proxy
        bound to this session.
        '''

        self.User = type('User', (BaseFunction, ), {
            **User.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.user.User` function proxy
        bound to this session.
        '''

        self.ScalingGroup = type('ScalingGroup', (BaseFunction, ), {
            **ScalingGroup.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.scaling_group.ScalingGroup` function proxy
        bound to this session.
        '''

        self.VFolder = type('VFolder', (BaseFunction, ), {
            **VFolder.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.vfolder.VFolder` function proxy
        bound to this session.
        '''

    def close(self):
        '''
        Terminates the session.  It schedules the ``close()`` coroutine
        of the underlying aiohttp session and then enqueues a sentinel
        object to indicate termination.  Then it waits until the worker
        thread to self-terminate by joining.
        '''
        if self._closed:
            return
        self._closed = True
        self._worker_thread.work_queue.put(self.aiohttp_session.close())
        self._worker_thread.work_queue.put(self.worker_thread.sentinel)
        self._worker_thread.join()

    @property
    def worker_thread(self):
        '''
        The thread that internally executes the asynchronous implementations
        of the given API functions.
        '''
        return self._worker_thread

    def __enter__(self):
        assert not self.closed, 'Cannot reuse closed session'
        if self.config.announcement_handler:
            try:
                payload = self.Manager.get_announcement()
                if payload['enabled']:
                    self.config.announcement_handler(payload['message'])
            except BackendAPIError:
                # The server may be an old one without annoucement API.
                pass
        return self

    def __exit__(self, exc_type, exc_obj, exc_tb):
        self.close()
        return False


class AsyncSession(BaseSession):
    '''
    An API client session that makes API requests asynchronously using coroutines.
    You may call all function proxy methods like a coroutine.
    It provides an async context manager interface to ensure closing of the session
    upon errors and scope exits.
    '''

    __slots__ = BaseSession.__slots__ + ()

    def __init__(
        self, *,
        config: APIConfig = None,
    ):
        super().__init__(config=config)

        ssl = None
        if self._config.skip_sslcert_validation:
            ssl = False
        connector = aiohttp.TCPConnector(ssl=ssl)
        self.aiohttp_session = aiohttp.ClientSession(connector=connector)

        from .base import BaseFunction
        from .admin import Admin
        from .agent import Agent, AgentWatcher
        from .auth import Auth
        from .etcd import EtcdConfig
        from .group import Group
        from .image import Image
        from .kernel import Kernel
        from .keypair import KeyPair
        from .manager import Manager
        from .resource import Resource
        from .keypair_resource_policy import KeypairResourcePolicy
        from .scaling_group import ScalingGroup
        from .user import User
        from .vfolder import VFolder

        self.Admin = type('Admin', (BaseFunction, ), {
            **Admin.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.admin.Admin` function proxy
        bound to this session.
        '''

        self.Agent = type('Agent', (BaseFunction, ), {
            **Agent.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.Agent` function proxy
        bound to this session.
        '''

        self.AgentWatcher = type('AgentWatcher', (BaseFunction, ), {
            **AgentWatcher.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.AgentWatcher` function proxy
        bound to this session.
        '''

        self.Auth = type('Auth', (BaseFunction, ), {
            **Auth.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.Auth` function proxy
        bound to this session.
        '''

        self.EtcdConfig = type('EtcdConfig', (BaseFunction, ), {
            **EtcdConfig.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.EtcdConfig` function proxy
        bound to this session.
        '''

        self.Group = type('Group', (BaseFunction, ), {
            **Group.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.agent.Group` function proxy
        bound to this session.
        '''

        self.Image = type('Image', (BaseFunction, ), {
            **Image.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.image.Image` function proxy
        bound to this session.
        '''

        self.Kernel = type('Kernel', (BaseFunction, ), {
            **Kernel.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.kernel.Kernel` function proxy
        bound to this session.
        '''

        self.KeyPair = type('KeyPair', (BaseFunction, ), {
            **KeyPair.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.keypair.KeyPair` function proxy
        bound to this session.
        '''

        self.Manager = type('Manager', (BaseFunction, ), {
            **Manager.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.manager.Manager` function proxy
        bound to this session.
        '''

        self.Resource = type('Resource', (BaseFunction, ), {
            **Resource.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.resource.Resource` function proxy
        bound to this session.
        '''

        self.KeypairResourcePolicy = type('KeypairResourcePolicy', (BaseFunction, ), {
            **KeypairResourcePolicy.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.keypair_resource_policy.KeypairResourcePolicy` function proxy
        bound to this session.
        '''

        self.User = type('User', (BaseFunction, ), {
            **User.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.user.User` function proxy
        bound to this session.
        '''

        self.ScalingGroup = type('ScalingGroup', (BaseFunction, ), {
            **ScalingGroup.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.scaling_group.ScalingGroup` function proxy
        bound to this session.
        '''

        self.VFolder = type('VFolder', (BaseFunction, ), {
            **VFolder.__dict__,
            'session': self,
        })
        '''
        The :class:`~ai.backend.client.vfolder.VFolder` function proxy
        bound to this session.
        '''

    async def close(self):
        if self._closed:
            return
        self._closed = True
        await self.aiohttp_session.close()

    async def __aenter__(self):
        assert not self.closed, 'Cannot reuse closed session'
        if self.config.announcement_handler:
            try:
                payload = await self.Manager.get_announcement()
                if payload['enabled']:
                    self.config.announcement_handler(payload['message'])
            except BackendAPIError:
                # The server may be an old one without annoucement API.
                pass
        return self

    async def __aexit__(self, exc_type, exc_obj, exc_tb):
        await self.close()
        return False
