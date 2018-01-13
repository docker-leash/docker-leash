# vim:set ts=4 sw=4 et:

import re


class ActionMapper():

    _MAP = {
        'GET': {
            r'^/_ping$': 'ping',
            r'^/v\d.\d{2}/containers/json(\?.*)?(#.*)?$': 'containersList',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/json(\?.*)?(#.*)?$': 'containersInspect',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/top(\?.*)?(#.*)?$': 'containersListProcess',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/logs(\?.*)?(#.*)?$': 'containersLogs',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/changes$': 'containersChanges',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/export$': 'containersExport',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/stats(\?.*)?(#.*)?$': 'containersStats',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/attach/ws(\?.*)?(#.*)?$': 'containersAttachWebsocket',
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersGetFilesystemArchive',
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
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/prune(\?.*)?(#.*)?$': 'containersPrune',
        },
        'DELETE': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'containersRemove',
        },
        'HEAD': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersGetInfoAboutFiles',
        },
        'PUT': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersExtractArchiveToDirectory',
        },
    }

    def get_action_name(self, method=None, uri=None):
        if not method or not uri:
            return None

        if method not in self._MAP:
            return None

        for reg, name in self._MAP[method].iteritems():
            if re.match(reg, uri):
                return name
