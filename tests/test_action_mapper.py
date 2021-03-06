# vim:set ts=4 sw=4 et:
'''
ActionTests
===========
'''

import unittest

from docker_leash.action_mapper import (Action, Namespace)
from docker_leash.action_mapper.router import Router
from docker_leash.exceptions import InvalidRequestException

from . import utils

data_get_action_name_by_method_and_query = [
    (None, None, None),
    ('', '', None),

    # Containers
    ('GET', '/v1.32/containers/json', 'containersList'),
    ('GET', '/v1.35/containers/json', 'containersList'),
    ('GET', '/v1.35/containers/json/', None),
    ('GET', '/v1.35/containers/json?', 'containersList'),
    ('GET', '/v1.35/containers/json/foo', None),
    ('GET', '/v1.35/containers/json/bar', None),
    ('GET', '/v1.35/containers/json#hello', 'containersList'),
    ('GET', '/v1.35/containers/json?limit=2', 'containersList'),
    ('GET', '/v1.35/containers/json?limit=2#hello', 'containersList'),
    ('GET', '/v1.35/containers/json?limit=2&size=true', 'containersList'),
    ('GET', '/v1.35/containers/json?limit=2&size=true#hello', 'containersList'),
    ('POST', '/v1.35/containers/create', 'containersCreate'),
    ('POST', '/v1.32/containers/create', 'containersCreate'),
    ('POST', '/v1.32/containers/create?name=hello_world', 'containersCreate'),
    ('POST', '/v1.32/containers/create#hello', 'containersCreate'),
    ('POST', '/v1.32/containers/create?name=hello_world#hello', 'containersCreate'),
    ('POST', '/v1.32/containers/create/', None),
    ('POST', '/v1.32/containers/create/?name=hello_world#hello', None),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/json', 'containersInspect'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/json?size=5', 'containersInspect'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/top', 'containersListProcess'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/top?ps_args=aux', 'containersListProcess'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/logs', 'containersLogs'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/logs?timestamps=true', 'containersLogs'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/changes', 'containersChanges'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/export', 'containersExport'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/stats', 'containersStats'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/stats?stream=true', 'containersStats'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/resize', 'containersResizeTTY'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/resize?h=25&w=80', 'containersResizeTTY'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/start', 'containersStart'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/start?detachKeys=Z', 'containersStart'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/stop', 'containersStop'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/stop?t=30', 'containersStop'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/restart', 'containersRestart'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/restart?t=30', 'containersRestart'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/kill', 'containersKill'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/kill?signal=SIGKILL', 'containersKill'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/update', 'containersUpdate'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/rename', 'containersRename'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/rename?name=hello_world', 'containersRename'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/pause', 'containersPause'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/unpause', 'containersUnpause'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/attach', 'containersAttach'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/attach?logs=true', 'containersAttach'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/attach/ws', 'containersAttachWebsocket'),
    ('GET', '/v1.32/containers/ff7291fe9e13b4b417/attach/ws?logs=true', 'containersAttachWebsocket'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/wait', 'containersWait'),
    ('POST', '/v1.32/containers/ff7291fe9e13b4b417/wait?condition=removed', 'containersWait'),
    ('DELETE', '/v1.32/containers/ff7291fe9e13b4b417', 'containersRemove'),
    ('DELETE', '/v1.35/containers/ff7291fe9e13b4b417', 'containersRemove'),
    ('DELETE', '/v1.35/containers/ff7291fe9e13b4b417?v=true', 'containersRemove'),
    ('HEAD', '/v1.35/containers/ff7291fe9e13b4b417/archive', 'containersGetInfoAboutFiles'),
    ('HEAD', '/v1.35/containers/ff7291fe9e13b4b417/archive?path=/etc',
     'containersGetInfoAboutFiles'),
    ('GET', '/v1.35/containers/ff7291fe9e13b4b417/archive',
     'containersGetFilesystemArchive'),
    ('GET', '/v1.35/containers/ff7291fe9e13b4b417/archive?path=/etc',
     'containersGetFilesystemArchive'),
    ('PUT', '/v1.35/containers/ff7291fe9e13b4b417/archive',
     'containersExtractArchiveToDirectory'),
    ('PUT', '/v1.35/containers/ff7291fe9e13b4b417/archive?path=/etc',
     'containersExtractArchiveToDirectory'),
    ('POST', '/v1.35/containers/prune', 'containersPrune'),
    ('POST', '/v1.35/containers/prune?filters=until=10m', 'containersPrune'),

    # Images
    ('GET', '/v1.35/images/json', 'imagesList'),
    ('POST', '/v1.35/build', 'imagesBuild'),
    ('POST', '/v1.35/build?dockerfile=Dockerfile', 'imagesBuild'),
    ('POST', '/v1.35/build/prune', 'imagesDeleteBuilderCache'),
    ('POST', '/v1.35/images/create', 'imagesCreate'),
    ('POST', '/v1.35/images/create?tag=latest', 'imagesCreate'),
    ('GET', '/v1.35/images/85f05633ddc1c5/json', 'imagesInspect'),
    ('GET', '/v1.35/images/85f05633ddc1c5/history', 'imagesHistory'),
    ('POST', '/v1.35/images/85f05633ddc1c5/push', 'imagesPush'),
    ('POST', '/v1.35/images//v1.35/images/registry.example.net/traefik/push?tag=alpine/push', 'imagesPush'),
    ('POST', '/v1.35/images/85f05633ddc1c5/tag', 'imagesTag'),
    ('POST', '/v1.35/images/85f05633ddc1c5/tag?tag=latest', 'imagesTag'),
    ('DELETE', '/v1.35/images/85f05633ddc1c5', 'imagesRemove'),
    ('DELETE', '/v1.35/images/85f05633ddc1c5?force=true', 'imagesRemove'),
    ('GET', '/v1.35/images/search', 'imagesSearch'),
    ('GET', '/v1.35/images/search?term=geokrety', 'imagesSearch'),
    ('POST', '/v1.35/images/prune', 'imagesPrune'),
    ('POST', '/v1.35/images/prune?filters=foo', 'imagesPrune'),
    ('POST', '/v1.35/commit', 'imagesCommit'),
    ('POST', '/v1.35/commit?container=ff7291fe9e13b4b417', 'imagesCommit'),
    ('GET', '/v1.35/images/85f05633ddc1c5/get', 'imagesExport'),
    ('GET', '/v1.35/images/get', 'imagesExportMultiple'),
    ('GET', '/v1.35/images/get?names=foo', 'imagesExportMultiple'),
    ('POST', '/v1.35/images/load', 'imagesImport'),
    ('POST', '/v1.35/images/load?quiet=true', 'imagesImport'),
    ('GET', '/v1.35/images/linuxserver/smokeping/json', 'imagesInspect'),
    ('GET', '/v1.35/images/linuxserver/smokeping/history', 'imagesHistory'),
    ('POST', '/v1.35/images/linuxserver/smokeping/push', 'imagesPush'),
    ('POST', '/v1.35/images/linuxserver/smokeping/tag', 'imagesTag'),
    ('POST', '/v1.35/images/linuxserver/smokeping/tag?tag=latest', 'imagesTag'),
    ('DELETE', '/v1.35/images/linuxserver/smokeping', 'imagesRemove'),
    ('DELETE', '/v1.35/images/linuxserver/smokeping?force=true', 'imagesRemove'),
    ('GET', '/v1.35/images/linuxserver/smokeping/get', 'imagesExport'),
    ('GET', '/v1.35/images/linuxserver/smokeping:latest/json', 'imagesInspect'),
    ('GET', '/v1.35/images/traefik:alpine/json', 'imagesInspect'),
    ('GET', '/v1.35/images/linuxserver/smokeping:latest/history', 'imagesHistory'),
    ('POST', '/v1.35/images/linuxserver/smokeping:latest/push', 'imagesPush'),
    ('POST', '/v1.35/images/linuxserver/smokeping:latest/tag', 'imagesTag'),
    ('POST', '/v1.35/images/linuxserver/smokeping:latest/tag?tag=latest', 'imagesTag'),
    ('DELETE', '/v1.35/images/linuxserver/smokeping:latest', 'imagesRemove'),
    ('DELETE', '/v1.35/images/linuxserver/smokeping:latest?force=true', 'imagesRemove'),
    ('GET', '/v1.35/images/linuxserver/smokeping:latest/get', 'imagesExport'),
    ('GET', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7/json', 'imagesInspect'),
    ('GET', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7/history', 'imagesHistory'),
    ('POST', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7/push', 'imagesPush'),
    ('POST', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7/tag', 'imagesTag'),
    ('POST', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7/tag?tag=latest', 'imagesTag'),
    ('DELETE', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7', 'imagesRemove'),
    ('DELETE', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7?force=true', 'imagesRemove'),
    ('GET', '/v1.35/images/linuxserver/sha256:8dd6c1a7e66717ccb8fd01a4254205a717752b4d69007742a4d4d66ab41fa2b7/get', 'imagesExport'),
    ('GET', '/v1.35/images/registry.example.net/traefik:alpine/json', 'imagesInspect'),
    ('GET', '/v1.35/images/registry.example.net/traefik:alpine/history', 'imagesHistory'),
    ('POST', '/v1.35/images/registry.example.net/traefik:alpine/tag', 'imagesTag'),
    ('DELETE', '/v1.35/images/registry.example.net/traefik:alpine', 'imagesRemove'),
    ('GET', '/v1.35/images/registry.example.net/traefik:alpine/get', 'imagesExport'),
    ('DELETE', '/v1.35/images/alpine:latest', 'imagesRemove'),

    # Networks
    ('GET', '/v1.35/networks', 'networksList'),
    ('GET', '/v1.35/networks?filters=foo', 'networksList'),
    ('GET', '/v1.35/networks/7d86d31b1478e7cc', 'networksInspect'),
    ('GET', '/v1.35/networks/7d86d31b1478e7cc?verbose=false', 'networksInspect'),
    ('DELETE', '/v1.35/networks/7d86d31b1478e7cc', 'networksRemove'),
    ('POST', '/v1.35/networks/create', 'networksCreate'),
    ('POST', '/v1.35/networks/7d86d31b1478e7cc/connect', 'networksConnect'),
    ('POST', '/v1.35/networks/7d86d31b1478e7cc/disconnect', 'networksDisconnect'),
    ('POST', '/v1.35/networks/prune', 'networksPrune'),

    # Volumes
    ('GET', '/v1.35/volumes', 'volumesList'),
    ('GET', '/v1.35/volumes?filters=foo', 'volumesList'),
    ('POST', '/v1.35/volumes/create', 'volumesCreate'),
    ('GET', '/v1.35/volumes/foo', 'volumesInspect'),
    ('DELETE', '/v1.35/volumes/foo', 'volumesRemove'),
    ('POST', '/v1.35/volumes/prune', 'volumesPrune'),

    # Exec
    ('POST', '/v1.35/containers/ff7291fe9e13b4b417/exec', 'execCreate'),
    ('POST', '/v1.35/exec/ff7291fe9e13b4b417/start', 'execStart'),
    ('POST', '/v1.35/exec/ff7291fe9e13b4b417/resize', 'execResize'),
    ('POST', '/v1.35/exec/ff7291fe9e13b4b417/resize?h=25&w=80', 'execResize'),
    ('GET', '/v1.35/exec/ff7291fe9e13b4b417/json', 'execInspect'),

    # Swarm
    ('GET', '/v1.35/swarm', 'swarmInspect'),
    ('POST', '/v1.35/swarm/init', 'swarmInitialize'),
    ('POST', '/v1.35/swarm/join', 'swarmJoin'),
    ('POST', '/v1.35/swarm/leave', 'swarmLeave'),
    ('POST', '/v1.35/swarm/leave?force=true', 'swarmLeave'),
    ('POST', '/v1.35/swarm/update?version=1234', 'swarmUpdate'),
    ('GET', '/v1.35/swarm/unlockkey', 'swarmUnlockKey'),
    ('POST', '/v1.35/swarm/unlock', 'swarmUnlock'),

    # Nodes
    ('GET', '/v1.35/nodes', 'nodesList'),
    ('GET', '/v1.35/nodes?filters=foo', 'nodesList'),
    ('GET', '/v1.35/nodes/24ifsmvkjbyhk', 'nodesInspect'),
    ('DELETE', '/v1.35/nodes/24ifsmvkjbyhk', 'nodesRemove'),
    ('DELETE', '/v1.35/nodes/24ifsmvkjbyhk?force=true', 'nodesRemove'),
    ('POST', '/v1.35/nodes/24ifsmvkjbyhk/update', 'nodesUpdate'),
    ('POST', '/v1.35/nodes/24ifsmvkjbyhk/update?version=1234', 'nodesUpdate'),

    # Services
    ('GET', '/v1.35/services', 'servicesList'),
    # Header Parameters: X-Registry-Auth
    ('GET', '/v1.35/services?filters=foo', 'servicesList'),
    ('POST', '/v1.35/services/create', 'servicesCreate'),
    ('GET', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz', 'servicesInspect'),
    ('GET', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz?insertDefaults=true', 'servicesInspect'),
    ('DELETE', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz', 'servicesRemove'),
    ('POST', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz/update', 'servicesUpdate'),
    ('POST', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz/update?version=1234', 'servicesUpdate'),
    ('GET', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz/logs', 'servicesLogs'),
    ('GET', '/v1.35/services/9mnpnzenvg8p8tdbtq4wvbkcz/logs?details=true', 'servicesLogs'),

    # Tasks
    ('GET', '/v1.35/tasks', 'tasksList'),
    ('GET', '/v1.35/tasks?filters=foo', 'tasksList'),
    ('GET', '/v1.35/tasks/0kzzo1i0y4jz6027t0k7aezc7', 'tasksInspect'),

    # Secrets
    ('GET', '/v1.35/secrets', 'secretsList'),
    ('GET', '/v1.35/secrets?filters=foo', 'secretsList'),
    ('POST', '/v1.35/secrets/create', 'secretsCreate'),
    ('GET', '/v1.35/secrets/ktnbjxoalbkvbvedmg1urrz8h', 'secretsInspect'),
    ('DELETE', '/v1.35/secrets/ktnbjxoalbkvbvedmg1urrz8h', 'secretsRemove'),
    ('POST', '/v1.35/secrets/ktnbjxoalbkvbvedmg1urrz8h/update', 'secretsUpdate'),
    ('POST', '/v1.35/secrets/ktnbjxoalbkvbvedmg1urrz8h/update?version=1234', 'secretsUpdate'),

    # Configs
    ('GET', '/v1.35/configs', 'configsList'),
    ('GET', '/v1.35/configs?filters=foo', 'configsList'),
    ('POST', '/v1.35/configs/create', 'configsCreate'),
    ('GET', '/v1.35/configs/ktnbjxoalbkvbvedmg1urrz8h', 'configsInspect'),
    ('DELETE', '/v1.35/configs/ktnbjxoalbkvbvedmg1urrz8h', 'configsRemove'),
    ('POST', '/v1.35/configs/ktnbjxoalbkvbvedmg1urrz8h/update', 'configsUpdate'),
    ('POST', '/v1.35/configs/ktnbjxoalbkvbvedmg1urrz8h/update?version=1234', 'configsUpdate'),

    # Plugins
    ('GET', '/v1.35/plugins', 'pluginsList'),
    ('GET', '/v1.35/plugins?filters=foo', 'pluginsList'),
    ('GET', '/v1.35/plugins/privileges', 'pluginsPrivileges'),
    ('GET', '/v1.35/plugins/privileges?remote=foo', 'pluginsPrivileges'),
    ('POST', '/v1.35/plugins/pull', 'pluginsInstall'),
    ('POST', '/v1.35/plugins/pull?remote=foo', 'pluginsInstall'),
    ('GET', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/json', 'pluginsInspect'),
    ('DELETE', '/v1.35/plugins/5724e2c8652da337ab2eedd19f', 'pluginsRemove'),
    ('DELETE', '/v1.35/plugins/5724e2c8652da337ab2eedd19f?force=true', 'pluginsRemove'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/enable', 'pluginsEnable'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/enable?timeout=0', 'pluginsEnable'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/disable', 'pluginsDisable'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/upgrade', 'pluginsUpgrade'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/upgrade?remote=foo', 'pluginsUpgrade'),
    ('POST', '/v1.35/plugins/create', 'pluginsCreate'),
    ('POST', '/v1.35/plugins/create?name=foo', 'pluginsCreate'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/push', 'pluginsPush'),
    ('POST', '/v1.35/plugins/5724e2c8652da337ab2eedd19f/set', 'pluginsConfigure'),

    # System
    ('GET', '/_ping', 'systemPing'),
    ('GET', '/v1.35/auth', 'systemRegistryAuth'),
    ('GET', '/v1.35/info', 'systemInfo'),
    ('GET', '/v1.35/version', 'systemVersion'),
    ('GET', '/v1.35/events', 'systemEvents'),
    ('GET', '/v1.35/events?filter=foo', 'systemEvents'),
    ('GET', '/v1.35/df', 'systemDataUsage'),

    # Session
    ('POST', '/v1.35/session', 'sessionInteractive'),

    # Distribution
    ('GET', '/v1.35/distribution/85f05633ddc1c5/json', 'distributionImageInfo'),
]


class ActionTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.action_mapper.Action`
    """

    def test_repr(self):
        '''check object representation
        (mainly for code-coverage)
        '''
        self.assertEqual(
            repr(Action('GET', '/_ping')),
            "Action('GET', '/_ping')",
        )

    def test_namespace_register_codecov(self):
        '''code coverage for a usecase not yet widespread
        '''
        @Action.namespace_register
        class Mock(Namespace):
            '''mock'''
            pass
        self.assertIn('mock', Action._namespace_map)

    def test_namespace_images(self):
        '''example for Namespace usage
        '''
        action = Action(
            'GET',
            "/v1.35/images/get?names=registry.example.net%2Ftraefik%3Aalpine&names=mariadb"
        )
        self.assertEqual(
            action.namespace.names(),
            ['registry.example.net/traefik:alpine', 'mariadb'],
        )
        # mainly for code coverage of the caching part
        self.assertIsInstance(
            action.namespace,
            Namespace,
        )



class RouterTests(unittest.TestCase):
    """Validation of :cls:`docker_leash.action_mapper.router.Router`
    """
    def test_repr(self):
        '''check object representation
        (mainly for code-coverage)
        '''
        self.assertEqual(
            repr(Router()),
            '<Router: DELETE: 0, GET: 0, HEAD: 0, POST: 0, PUT: 0>',
        )


def create_get_action_name_by_method_and_query(method, query, expect):
    def do_test(self):
        action = Action(method=method, query=query)
        self.assertEqual(
            expect,
            action.name,
            'expected: {!r}, got: {!r}'.format(expect, action.name)
        )
    return do_test


data_get_action_name_invalid_method = (
    ('EXOTIC', '/_ping'),
    ('GET', 'totally-invalid'),
    ('GET', '/no-match')
)

for i, check in enumerate(data_get_action_name_invalid_method):
    func = utils.create_assertRaises(InvalidRequestException, Action, *check)
    func.__name__ = 'test_get_action_name_invalid_method_{}'.format(
        i,
    )
    func.__doc__ = "Retrieve action name by an invalid method and query"
    setattr(ActionTests, func.__name__, func)

for i, check in enumerate(data_get_action_name_by_method_and_query):
    if check[-1] is None:
        func = utils.create_assertRaises(InvalidRequestException, Action, *check[:-1])
    else:
        func = create_get_action_name_by_method_and_query(*check)
    func.__name__ = 'test_get_action_name_by_method_and_query_{:03d}'.format(
        i,
    )
    setattr(ActionTests, func.__name__, func)


data_invalid_routes = (
    (ValueError, 'GET', '.', 'missingcaps'),
    (ValueError, 'GET', '.', 'INVALIDNAME1'),
    (ValueError, 'GET', '.', 'invalid-name2'),
    (KeyError, 'EXOTIC', '.', 'invalidMethod'),
    (ValueError, 'GET', r'(.', 'invalidRegex'),
)

for i, args in enumerate(data_invalid_routes):
    router = Router()
    func = utils.create_assertRaises(args[0], router.register, *args[1:])
    func.__name__ = 'test_invalid_routes_{}'.format(i)
    setattr(RouterTests, func.__name__, func)


# nosetests compatibility workaround
del func
