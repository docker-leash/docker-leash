# vim:set ts=4 sw=4 et:
'''
ActionMapper
============
'''

import re


class ActionMapper(object):
    """The :class:`ActionMapper` class is responsible for mapping
    `RequestMethod` and `RequestUri` to
    a keyword usable in the application configured rules.

    :var _MAP: Internal structure to map API actions to keyword.
    :vartype _MAP: dict

    :var _actions: Internal structure to store actions to keywords.
    :vartype _actions: list

    .. todo::
       The regex need to be reviewed.
    """

    _MAP = {
        'GET': {
            r'^/_ping$': 'systemPing',
            r'^/v\d.\d{2}/containers/json(\?.*)?(#.*)?$': 'containersList',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/json(\?.*)?(#.*)?$': 'containersInspect',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/top(\?.*)?(#.*)?$': 'containersListProcess',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/logs(\?.*)?(#.*)?$': 'containersLogs',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/changes$': 'containersChanges',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/export$': 'containersExport',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/stats(\?.*)?(#.*)?$': 'containersStats',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/attach/ws(\?.*)?(#.*)?$': 'containersAttachWebsocket',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersGetFilesystemArchive',
            r'^/v\d.\d{2}/images/json(\?.*)?(#.*)?$': 'imagesList',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+/json$': 'imagesInspect',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+/history$': 'imagesHistory',
            r'^/v\d.\d{2}/images/search(\?.*)?(#.*)?$': 'imagesSearch',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+/get$': 'imagesExport',
            r'^/v\d.\d{2}/images/get(\?.*)?(#.*)?$': 'imagesExportMultiple',
            r'^/v\d.\d{2}/networks(\?.*)?(#.*)?$': 'networksList',
            r'^/v\d.\d{2}/networks/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'networksInspect',
            r'^/v\d.\d{2}/volumes(\?.*)?(#.*)?$': 'volumesList',
            r'^/v\d.\d{2}/volumes/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'volumesInspect',
            r'^/v\d.\d{2}/exec/[a-zA-Z0-9_-]+/json(#.*)?$': 'execInspect',
            r'^/v\d.\d{2}/swarm(#.*)?$': 'swarmInspect',
            r'^/v\d.\d{2}/swarm/unlockkey(#.*)?$': 'swarmUnlockKey',
            r'^/v\d.\d{2}/nodes(\?.*)?(#.*)?$': 'nodesList',
            r'^/v\d.\d{2}/nodes/[a-zA-Z0-9_-]+(#.*)?$': 'nodesInspect',
            r'^/v\d.\d{2}/services(\?.*)?(#.*)?$': 'servicesList',
            r'^/v\d.\d{2}/services/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'servicesInspect',
            r'^/v\d.\d{2}/services/[a-zA-Z0-9_-]+/logs(\?.*)?(#.*)?$': 'servicesLogs',
            r'^/v\d.\d{2}/tasks(\?.*)?(#.*)?$': 'tasksList',
            r'^/v\d.\d{2}/tasks/[a-zA-Z0-9_-]+(#.*)?$': 'tasksInspect',
            r'^/v\d.\d{2}/secrets(\?.*)?(#.*)?$': 'secretsList',
            r'^/v\d.\d{2}/secrets/[a-zA-Z0-9_-]+(#.*)?$': 'secretsInspect',
            r'^/v\d.\d{2}/configs(\?.*)?(#.*)?$': 'configsList',
            r'^/v\d.\d{2}/configs/[a-zA-Z0-9_-]+(#.*)?$': 'configsInspect',
            r'^/v\d.\d{2}/plugins(\?.*)?(#.*)?$': 'pluginsList',
            r'^/v\d.\d{2}/plugins/privileges(\?.*)?(#.*)?$': 'pluginsPrivileges',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+/json(#.*)?$': 'pluginsInspect',
            r'^/v\d.\d{2}/auth(#.*)?$': 'systemRegistryAuth',
            r'^/v\d.\d{2}/info(#.*)?$': 'systemInfo',
            r'^/v\d.\d{2}/version(#.*)?$': 'systemVersion',
            r'^/v\d.\d{2}/events(\?.*)?(#.*)?$': 'systemEvents',
            r'^/v\d.\d{2}/df(#.*)?$': 'systemDataUsage',
            r'^/v\d.\d{2}/distribution/[a-zA-Z0-9_-]+/json(#.*)?$': 'distributionImageInfo',
        },
        'POST': {
            r'^/v\d.\d{2}/containers/create(\?.*)?(#.*)?$': 'containersCreate',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/resize(\?.*)?(#.*)?$': 'containersResizeTTY',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/start(\?.*)?(#.*)?$': 'containersStart',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/stop(\?.*)?(#.*)?$': 'containersStop',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/restart(\?.*)?(#.*)?$': 'containersRestart',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/kill(\?.*)?(#.*)?$': 'containersKill',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/update$': 'containersUpdate',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/rename(\?.*)?(#.*)?$': 'containersRename',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/pause$': 'containersPause',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/unpause$': 'containersUnpause',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/attach(\?.*)?(#.*)?$': 'containersAttach',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/wait(\?.*)?(#.*)?$': 'containersWait',
            r'^/v\d.\d{2}/containers/prune(\?.*)?(#.*)?$': 'containersPrune',
            r'^/v\d.\d{2}/build(\?.*)?(#.*)?$': 'imagesBuild',
            r'^/v\d.\d{2}/build/prune$': 'imagesDeleteBuilderCache',
            r'^/v\d.\d{2}/images/create(\?.*)?(#.*)?$': 'imagesCreate',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+/push(\?.*)?(#.*)?$': 'imagesPush',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+/tag(\?.*)?(#.*)?$': 'imagesTag',
            r'^/v\d.\d{2}/images/prune(\?.*)?(#.*)?$': 'imagesPrune',
            r'^/v\d.\d{2}/commit(\?.*)?(#.*)?$': 'imagesCommit',
            r'^/v\d.\d{2}/images/load(\?.*)?(#.*)?$': 'imagesImport',
            r'^/v\d.\d{2}/networks/create(#.*)?$': 'networksCreate',
            r'^/v\d.\d{2}/networks/[a-zA-Z0-9_-]+/connect(#.*)?$': 'networksConnect',
            r'^/v\d.\d{2}/networks/[a-zA-Z0-9_-]+/disconnect(#.*)?$': 'networksDisconnect',
            r'^/v\d.\d{2}/networks/prune(\?.*)?(#.*)?$': 'networksPrune',
            r'^/v\d.\d{2}/volumes/create(#.*)?$': 'volumesCreate',
            r'^/v\d.\d{2}/volumes/prune(\?.*)?(#.*)?$': 'volumesPrune',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/exec(#.*)?$': 'execCreate',
            r'^/v\d.\d{2}/exec/[a-zA-Z0-9_-]+/start(#.*)?$': 'execStart',
            r'^/v\d.\d{2}/exec/[a-zA-Z0-9_-]+/resize(\?.*)?(#.*)?$': 'execResize',
            r'^/v\d.\d{2}/swarm/init(#.*)?$': 'swarmInitialize',
            r'^/v\d.\d{2}/swarm/join(#.*)?$': 'swarmJoin',
            r'^/v\d.\d{2}/swarm/leave(\?.*)?(#.*)?$': 'swarmLeave',
            r'^/v\d.\d{2}/swarm/update(\?.*)?(#.*)?$': 'swarmUpdate',
            r'^/v\d.\d{2}/swarm/unlock(#.*)?$': 'swarmUnlock',
            r'^/v\d.\d{2}/nodes/[a-zA-Z0-9_-]+/update(\?.*)?(#.*)?$': 'nodesUpdate',
            r'^/v\d.\d{2}/services/create(#.*)?$': 'servicesCreate',
            r'^/v\d.\d{2}/services/[a-zA-Z0-9_-]+/update(\?.*)?(#.*)?$': 'servicesUpdate',
            r'^/v\d.\d{2}/secrets/create(#.*)?$': 'secretsCreate',
            r'^/v\d.\d{2}/secrets/[a-zA-Z0-9_-]+/update(\?.*)?(#.*)?$': 'secretsUpdate',
            r'^/v\d.\d{2}/configs/create(#.*)?$': 'configsCreate',
            r'^/v\d.\d{2}/configs/[a-zA-Z0-9_-]+/update(\?.*)?(#.*)?$': 'configsUpdate',
            r'^/v\d.\d{2}/plugins/pull(\?.*)?(#.*)?$': 'pluginsInstall',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+/enable(\?.*)?(#.*)?$': 'pluginsEnable',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+/disable(#.*)?$': 'pluginsDisable',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+/upgrade(\?.*)?(#.*)?$': 'pluginsUpgrade',
            r'^/v\d.\d{2}/plugins/create(\?.*)?(#.*)?$': 'pluginsCreate',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+/push(\?.*)?(#.*)?$': 'pluginsPush',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+/set(\?.*)?(#.*)?$': 'pluginsConfigure',
            r'^/v\d.\d{2}/session(#.*)?$': 'sessionInteractive',
        },
        'DELETE': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'containersRemove',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'imagesRemove',
            r'^/v\d.\d{2}/networks/[a-zA-Z0-9_-]+(#.*)?$': 'networksRemove',
            r'^/v\d.\d{2}/volumes/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'volumesRemove',
            r'^/v\d.\d{2}/nodes/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'nodesRemove',
            r'^/v\d.\d{2}/services/[a-zA-Z0-9_-]+(#.*)?$': 'servicesRemove',
            r'^/v\d.\d{2}/secrets/[a-zA-Z0-9_-]+(#.*)?$': 'secretsRemove',
            r'^/v\d.\d{2}/configs/[a-zA-Z0-9_-]+(#.*)?$': 'configsRemove',
            r'^/v\d.\d{2}/plugins/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'pluginsRemove',
        },
        'HEAD': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersGetInfoAboutFiles',
        },
        'PUT': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersExtractArchiveToDirectory',
        },
    }

    _actions = {
        'containersList': 'GET',
        'containersCreate': 'POST',
        'containersInspect': 'GET',
        'containersListProcess': 'GET',
        'containersLogs': 'GET',
        'containersChanges': 'GET',
        'containersExport': 'GET',
        'containersStats': 'GET',
        'containersResizeTTY': 'POST',
        'containersStart': 'POST',
        'containersStop': 'POST',
        'containersRestart': 'POST',
        'containersUpdate': 'POST',
        'containersRename': 'POST',
        'containersPause': 'POST',
        'containersUnpause': 'POST',
        'containersAttach': 'POST',
        'containersAttachWebsocket': 'GET',
        'containersWait': 'POST',
        'containersRemove': 'DELETE',
        'containersGetInfoAboutFiles': 'GET',
        'containersGetFilesystemArchive': 'GET',
        'containersExtractArchiveToDirectory': 'PUT',
        'containersPrune': 'POST',
        'imagesList': 'GET',
        'imagesBuild': 'POST',
        'imagesDeleteBuilderCache': 'POST',
        'imagesCreate': 'POST',
        'imagesInspect': 'GET',
        'imagesHistory': 'GET',
        'imagesPush': 'POST',
        'imagesTag': 'POST',
        'imagesRemove': 'DELETE',
        'imagesSearch': 'GET',
        'imagesPrune': 'POST',
        'imagesCommit': 'POST',
        'imagesExport': 'GET',
        'imagesExportMultiple': 'GET',
        'imagesImport': 'POST',
        'networksList': 'GET',
        'networksInspect': 'GET',
        'networksRemove': 'DELETE',
        'networksCreate': 'POST',
        'networksConnect': 'POST',
        'networksDisconnect': 'POST',
        'networksPrune': 'POST',
        'volumesList': 'GET',
        'volumesCreate': 'POST',
        'volumesInspect': 'GET',
        'volumesRemove': 'DELETE',
        'volumesPrune': 'POST',
        'execCreate': 'POST',
        'execStart': 'POST',
        'execResize': 'POST',
        'execInspect': 'GET',
        'swarmInspect': 'GET',
        'swarmInitialize': 'POST',
        'swarmJoin': 'POST',
        'swarmLeave': 'POST',
        'swarmUpdate': 'POST',
        'swarmUnlockKey': 'GET',
        'swarmUnlock': 'POST',
        'nodesList': 'GET',
        'nodesInspect': 'GET',
        'nodesRemove': 'DELETE',
        'nodesUpdate': 'POST',
        'servicesList': 'GET',
        'servicesCreate': 'POST',
        'servicesInspect': 'GET',
        'servicesRemove': 'DELETE',
        'servicesUpdate': 'GET',
        'servicesLogs': 'GET',
        'tasksList': 'GET',
        'tasksInspect': 'GET',
        'secretsList': 'GET',
        'secretsCreate': 'POST',
        'secretsInspect': 'GET',
        'secretsRemove': 'DELETE',
        'secretsUpdate': 'POST',
        'configsList': 'GET',
        'configsCreate': 'POST',
        'configsInspect': 'GET',
        'configsRemove': 'DELETE',
        'configsUpdate': 'POST',
        'pluginsList': 'GET',
        'pluginsPrivileges': 'GET',
        'pluginsInstall': 'POST',
        'pluginsInspect': 'GET',
        'pluginsRemove': 'DELETE',
        'pluginsEnable': 'POST',
        'pluginsDisable': 'POST',
        'pluginsUpgrade': 'POST',
        'systemPing': 'GET',
        'systemRegistryAuth': 'GET',
        'systemInfo': 'GET',
        'systemVersion': 'GET',
        'systemEvents': 'GET',
        'systemDataUsage': 'GET',
        'distributionImageInfo': 'GET',
        'sessionInteractive': 'POST',
    }

    def get_action_name(self, method=None, uri=None):
        """Return the keyword for a `RequestMethod` and `RequestUri` tuple.

        :param str method: The method.
        :param str method: The uri.
        :return: The keyword for the action
        :rtype: str or None
        """
        if not method or not uri:
            return None

        if method not in self._MAP:
            return None

        for reg, name in self._MAP[method].iteritems():
            if re.match(reg, uri):
                return name

        return None

    def is_action(self, action=None):
        """Check if an action is recognized.

        :param str action: The action name to check
        :return: True if the action is recognized
        :rtype: bool
        """
        return action in self._actions.keys()

    def is_readonly(self, action=None):
        """Check if an action is recognized.

        :param str action: The action name to check
        :return: True if the action is recognized or read-only
        :rtype: bool
        """
        return action in self._actions.keys() and self._actions[action] in ('GET', 'HEAD')

    @classmethod
    def action_is_about(cls, action_name, action_parent):
        """Check if an action name is action parent category.

        :param str action_name: The action name to check
        :param str or list action_parent: The action parent to check against
        :return: The parent if found
        :rtype: str
        """
        parents = action_parent if isinstance(action_parent, list) else [action_parent]
        for parent in parents:
            if action_name and parent and action_name.startswith(parent):
                return parent
        return None
