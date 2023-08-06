"""Fixtures for supporting a distributed test run."""
import contextlib
import json
import os
import socket

import pytest
import zc.lockfile

marker = object()


def try_remove(filename):
    try:
        os.unlink(filename)
    except OSError:
        pass


@contextlib.contextmanager
def file_lock(filename, remove=True, timeout=20):
    """A lock that is shared across processes.

    :param filename: the name of the file that will be locked.

    """
    with contextlib.closing(zc.lockfile.SimpleLockFile(filename)) as lockfile:
        yield lockfile._fp

    remove and try_remove(filename)


def unlock_resource(name, resource, lock_dir, services_log):
    """Unlock previously locked resource.

    :param name: name to be used to separate various resources, eg. port, display
    :param resource: resource value which was previously locked
    :param lock_dir: directory for lockfiles to use.
    """
    with locked_resources(name, lock_dir) as bound_resources:
        try:
            bound_resources.remove(resource)
        except ValueError:
            pass
        services_log.debug('resource freed {0}: {1}'.format(name, resource))
        services_log.debug('bound resources {0}: {1}'.format(name, bound_resources))


@contextlib.contextmanager
def locked_resources(name, lock_dir):
    """Contextmanager providing an access to locked shared resource list.

    :param name: name to be used to separate various resources, eg. port, display
    :param lock_dir: directory for lockfiles to use.
    """
    with file_lock(os.path.join(lock_dir, name), remove=False) as fd:
        bound_resources = fd.read().strip()
        if bound_resources:
            try:
                bound_resources = json.loads(bound_resources)
            except ValueError:
                bound_resources = None
        if not isinstance(bound_resources, list):
            bound_resources = []
        yield bound_resources

        fd.seek(0)
        fd.truncate()
        fd.write(json.dumps(bound_resources))
        fd.flush()


def unlock_port(port, lock_dir, services_log):
    """Unlock previously locked port."""
    return unlock_resource('port', port, lock_dir, services_log)


def unlock_display(display, lock_dir, services_log):
    """Unlock previously locked display."""
    return unlock_resource('display', display, lock_dir, services_log)


def lock_resource(name, resource_getter, lock_dir, services_log):
    """Issue a lock for given resource."""
    with locked_resources(name, lock_dir) as bound_resources:
        services_log.debug('bound_resources {0}: {1}'.format(name, bound_resources))

        resource = resource_getter(bound_resources)
        while resource in bound_resources:
            # resource is already taken by someone, retry
            services_log.debug('bound resources {0}: {1}'.format(name, bound_resources))
            resource = resource_getter(bound_resources)
        services_log.debug('free resource choosen {0}: {1}'.format(name, resource))
        bound_resources.append(resource)
        services_log.debug('bound resources {0}: {1}'.format(name, bound_resources))
        return resource


def get_free_port(lock_dir, services_log):
    """Get free port to listen on."""
    def get_port(bound_resources):
        if bound_resources:
            port = max(bound_resources) + 1
        else:
            port = 30000

        while True:
            s = socket.socket()
            try:
                s.bind(('127.0.0.1', port))
                s.close()
                return port
            except socket.error:
                pass
            port += 1

    return lock_resource('port', get_port, lock_dir, services_log)


def get_free_display(lock_dir, services_log):
    """Get free display to listen on."""
    def get_display(bound_resources):
        display = 100
        while True:
            if bound_resources:
                display = max(bound_resources) + 1
            if os.path.exists('/tmp/.X{0}-lock'.format(display)):
                display += 1
                continue
            return display

    return lock_resource('display', get_display, lock_dir, services_log)


@pytest.fixture(scope='session')
def port_getter(request, lock_dir, services_log):
    """Lock getter function."""
    def get_port():
        """Lock a free port and unlock it on finalizer."""
        port = get_free_port(lock_dir, services_log)

        def finalize():
            unlock_port(port, lock_dir, services_log)
        request.addfinalizer(finalize)
        return port
    return get_port


@pytest.fixture(scope='session')
def display_getter(request, lock_dir, services_log):
    """Display getter function."""
    def get_display():
        """Lock a free display and unlock it on finalizer."""
        display = get_free_display(lock_dir, services_log)
        request.addfinalizer(lambda: unlock_display(display, lock_dir, services_log))
        return display
    return get_display
