# vim:set ts=4 sw=4 et:

import re


class ActionMapper(object):
    """The :class:`app.action_mapper.ActionMapper` class is responsible for mapping `RequestMethod` and `RequestUri` to
    a keyword usable in the application configured rules.

    :var _MAP: Internal structure to map API actions to keyword.
    :vartype _MAP: dict

    ..todo::
      The regex need to be reviewed
    """

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
        },
        'DELETE': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'containersRemove',
            r'^/v\d.\d{2}/images/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'imagesRemove',
            r'^/v\d.\d{2}/networks/[a-zA-Z0-9_-]+(#.*)?$': 'networksRemove',
            r'^/v\d.\d{2}/volumes/[a-zA-Z0-9_-]+(\?.*)?(#.*)?$': 'volumesRemove',
        },
        'HEAD': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersGetInfoAboutFiles',
        },
        'PUT': {
            r'^/v\d.\d{2}/containers/[a-zA-Z0-9_-]+/archive(\?.*)?(#.*)?$': 'containersExtractArchiveToDirectory',
        },
    }

    def get_action_name(self, method=None, uri=None):
        """Return the keyword for a `RequestMethod` and `RequestUri` tuple.

        :param string method: The method.
        :param string method: The uri.
        :return: The keyword for the action
        :rtype: string or None
        """
        if not method or not uri:
            return None

        if method not in self._MAP:
            return None

        for reg, name in self._MAP[method].iteritems():
            if re.match(reg, uri):
                return name
