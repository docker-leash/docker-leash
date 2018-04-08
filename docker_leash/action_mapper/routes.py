'''Docker routes rules

Inspiration from: moby/api/server/router/
'''

from .router import Router


routes = Router()  # pylint: disable=C0103

# containers
routes.register('GET', r'/containers/json$', 'containersList')
routes.register('GET', r'/containers/([a-zA-Z0-9_-]+)/json$', 'containersInspect')
routes.register('GET', r'/containers/([a-zA-Z0-9_-]+)/top$', 'containersListProcess')
routes.register('GET', r'/containers/([a-zA-Z0-9_-]+)/logs$', 'containersLogs')
routes.register('GET', r'/containers/([a-zA-Z0-9_-]+)/changes$', 'containersChanges')
routes.register('GET', r'/containers/([a-zA-Z0-9_-]+)/export$', 'containersExport')
routes.register('GET', r'/containers/([a-zA-Z0-9_-]+)/stats$', 'containersStats')
routes.register(
    'GET',
    r'/containers/([a-zA-Z0-9_-]+)/attach/ws$',
    'containersAttachWebsocket',
)
routes.register(
    'GET',
    r'/containers/([a-zA-Z0-9_-]+)/archive$',
    'containersGetFilesystemArchive',
)

routes.register('POST', r'/containers/create$', 'containersCreate')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/resize$', 'containersResizeTTY')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/start$', 'containersStart')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/stop$', 'containersStop')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/restart$', 'containersRestart')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/kill$', 'containersKill')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/update$', 'containersUpdate')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/rename$', 'containersRename')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/pause$', 'containersPause')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/unpause$', 'containersUnpause')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/attach$', 'containersAttach')
routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/wait$', 'containersWait')
routes.register('POST', r'/containers/prune$', 'containersPrune')

routes.register('DELETE', r'/containers/([a-zA-Z0-9_-]+)$', 'containersRemove')

routes.register(
    'HEAD',
    r'^/containers/([a-zA-Z0-9_-]+)/archive$',
    'containersGetInfoAboutFiles',
)

routes.register(
    'PUT',
    r'^/containers/([a-zA-Z0-9_-]+)/archive$',
    'containersExtractArchiveToDirectory',
)

# images
routes.register('GET', r'/images/json$', 'imagesList')
routes.register('GET', r'/images/([a-zA-Z0-9/:_.-]+)/json$', 'imagesInspect')
routes.register('GET', r'/images/([a-zA-Z0-9/:_.-]+)/history$', 'imagesHistory')
routes.register('GET', r'/images/search$', 'imagesSearch')
routes.register('GET', r'/images/([a-zA-Z0-9/:_.-]+)/get$', 'imagesExport')
routes.register('GET', r'/images/get$', 'imagesExportMultiple')

routes.register('POST', r'/build$', 'imagesBuild')
routes.register('POST', r'/build/prune$', 'imagesDeleteBuilderCache')
routes.register('POST', r'/images/create$', 'imagesCreate')
routes.register('POST', r'/images/([a-zA-Z0-9/:_.-]+)/push$', 'imagesPush')
routes.register('POST', r'/images/([a-zA-Z0-9/:_.-]+)/tag$', 'imagesTag')
routes.register('POST', r'/images/prune$', 'imagesPrune')
routes.register('POST', r'/commit$', 'imagesCommit')
routes.register('POST', r'/images/load$', 'imagesImport')

routes.register('DELETE', r'/images/([a-zA-Z0-9/:_.-]+)$', 'imagesRemove')

# networks
routes.register('GET', r'/networks$', 'networksList')
routes.register('GET', r'/networks/([a-zA-Z0-9_-]+)$', 'networksInspect')

routes.register('POST', r'/networks/create$', 'networksCreate')
routes.register('POST', r'/networks/([a-zA-Z0-9_-]+)/connect$', 'networksConnect')
routes.register('POST', r'/networks/([a-zA-Z0-9_-]+)/disconnect$', 'networksDisconnect')
routes.register('POST', r'/networks/prune$', 'networksPrune')

routes.register('DELETE', r'/networks/([a-zA-Z0-9_-]+)$', 'networksRemove')

# volumes
routes.register('GET', r'/volumes$', 'volumesList')
routes.register('GET', r'/volumes/([a-zA-Z0-9_-]+)$', 'volumesInspect')

routes.register('POST', r'/volumes/create$', 'volumesCreate')
routes.register('POST', r'/volumes/prune$', 'volumesPrune')

routes.register('DELETE', r'/volumes/([a-zA-Z0-9_-]+)$', 'volumesRemove')

# exec
routes.register('GET', r'/exec/([a-zA-Z0-9_-]+)/json$', 'execInspect')

routes.register('POST', r'/containers/([a-zA-Z0-9_-]+)/exec$', 'execCreate')
routes.register('POST', r'/exec/([a-zA-Z0-9_-]+)/start$', 'execStart')
routes.register('POST', r'/exec/([a-zA-Z0-9_-]+)/resize$', 'execResize')

# swarm
routes.register('GET', r'/swarm$', 'swarmInspect')
routes.register('GET', r'/swarm/unlockkey$', 'swarmUnlockKey')

routes.register('POST', r'/swarm/init$', 'swarmInitialize')
routes.register('POST', r'/swarm/join$', 'swarmJoin')
routes.register('POST', r'/swarm/leave$', 'swarmLeave')
routes.register('POST', r'/swarm/update$', 'swarmUpdate')
routes.register('POST', r'/swarm/unlock$', 'swarmUnlock')

# nodes
routes.register('GET', r'/nodes$', 'nodesList')
routes.register('GET', r'/nodes/([a-zA-Z0-9_-]+)$', 'nodesInspect')

routes.register('POST', r'/nodes/([a-zA-Z0-9_-]+)/update$', 'nodesUpdate')

routes.register('DELETE', r'/nodes/([a-zA-Z0-9_-]+)$', 'nodesRemove')

# services
routes.register('GET', r'/services$', 'servicesList')
routes.register('GET', r'/services/([a-zA-Z0-9_-]+)$', 'servicesInspect')
routes.register('GET', r'/services/([a-zA-Z0-9_-]+)/logs$', 'servicesLogs')

routes.register('POST', r'/services/create$', 'servicesCreate')
routes.register('POST', r'/services/([a-zA-Z0-9_-]+)/update$', 'servicesUpdate')

routes.register('DELETE', r'/services/([a-zA-Z0-9_-]+)$', 'servicesRemove')

# tasks
routes.register('GET', r'/tasks$', 'tasksList')
routes.register('GET', r'/tasks/([a-zA-Z0-9_-]+)$', 'tasksInspect')

# secrets
routes.register('GET', r'/secrets$', 'secretsList')
routes.register('GET', r'/secrets/([a-zA-Z0-9_-]+)$', 'secretsInspect')

routes.register('POST', r'/secrets/create$', 'secretsCreate')
routes.register('POST', r'/secrets/([a-zA-Z0-9_-]+)/update$', 'secretsUpdate')

routes.register('DELETE', r'/secrets/([a-zA-Z0-9_-]+)$', 'secretsRemove')

# configs
routes.register('GET', r'/configs$', 'configsList')
routes.register('GET', r'/configs/([a-zA-Z0-9_-]+)$', 'configsInspect')

routes.register('POST', r'/configs/create$', 'configsCreate')
routes.register('POST', r'/configs/([a-zA-Z0-9_-]+)/update$', 'configsUpdate')

routes.register('DELETE', r'/configs/([a-zA-Z0-9_-]+)$', 'configsRemove')

# plugins
routes.register('GET', r'/plugins$', 'pluginsList')
routes.register('GET', r'/plugins/privileges$', 'pluginsPrivileges')
routes.register('GET', r'/plugins/([a-zA-Z0-9_-]+)/json$', 'pluginsInspect')

routes.register('POST', r'/plugins/pull$', 'pluginsInstall')
routes.register('POST', r'/plugins/([a-zA-Z0-9_-]+)/enable$', 'pluginsEnable')
routes.register('POST', r'/plugins/([a-zA-Z0-9_-]+)/disable$', 'pluginsDisable')
routes.register('POST', r'/plugins/([a-zA-Z0-9_-]+)/upgrade$', 'pluginsUpgrade')
routes.register('POST', r'/plugins/create$', 'pluginsCreate')
routes.register('POST', r'/plugins/([a-zA-Z0-9_-]+)/push$', 'pluginsPush')
routes.register('POST', r'/plugins/([a-zA-Z0-9_-]+)/set$', 'pluginsConfigure')

routes.register('DELETE', r'/plugins/([a-zA-Z0-9_-]+)$', 'pluginsRemove')

# system
routes.register('GET', r'/_ping$', 'systemPing')
routes.register('GET', r'/auth$', 'systemRegistryAuth')
routes.register('GET', r'/info$', 'systemInfo')
routes.register('GET', r'/version$', 'systemVersion')
routes.register('GET', r'/events$', 'systemEvents')
routes.register('GET', r'/df$', 'systemDataUsage')

# distribution
routes.register('GET', r'/distribution/([a-zA-Z0-9_-]+)/json$', 'distributionImageInfo')

# session
routes.register('POST', r'/session$', 'sessionInteractive')
