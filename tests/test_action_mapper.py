# vim:set ts=4 sw=4 et:

import unittest

from app.action_mapper import ActionMapper


class ActionMapperTests(unittest.TestCase):

    @classmethod
    def test_init(cls):
        ActionMapper()

    def test_get_action_name(self):
        mapper = ActionMapper()

        checks = [
            (None, None, None),
            ('', '', None),
            ('GET', '/_ping', 'ping'),
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
            ('HEAD', '/v1.35/containers/ff7291fe9e13b4b417/archive?path=/etc', 'containersGetInfoAboutFiles'),
            ('GET', '/v1.35/containers/ff7291fe9e13b4b417/archive', 'containersGetFilesystemArchive'),
            ('GET', '/v1.35/containers/ff7291fe9e13b4b417/archive?path=/etc', 'containersGetFilesystemArchive'),
            ('PUT', '/v1.35/containers/ff7291fe9e13b4b417/archive', 'containersExtractArchiveToDirectory'),
            ('PUT', '/v1.35/containers/ff7291fe9e13b4b417/archive?path=/etc', 'containersExtractArchiveToDirectory'),
            ('POST', '/v1.35/containers/ff7291fe9e13b4b417/prune', 'containersPrune'),
            ('POST', '/v1.35/containers/ff7291fe9e13b4b417/prune?filters=until=10m', 'containersPrune'),
        ]
        for check in checks:
            action = mapper.get_action_name(method=check[0], uri=check[1])
            self.assertEqual(check[2], action)

    def test_get_action_name_invalid_method(self):
        action = ActionMapper().get_action_name(method='EXOTIC', uri='/_ping')
        self.assertEqual(action, None)
