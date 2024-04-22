from .util import post_request, get_request, Video, print_error
from .constants import *

def get_vrtmax_token():
    json = post_request('https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v2/tokens', {})
    token = json['vrtPlayerToken']
    return token

def get_metadata(pageId):
    headers = {'Content-Type': 'application/json'}
    data = {"query": "query VideoPage($pageId: ID!, $lazyItemCount: Int = 100, $after: ID, $before: ID) {\n  page(id: $pageId) {\n    ... on EpisodePage {\n      objectId\n      title\n      permalink\n      seo {\n        ...seoFragment\n        __typename\n      }\n      socialSharing {\n        ...socialSharingFragment\n        __typename\n      }\n      trackingData {\n        ...trackingDataFragment\n        __typename\n      }\n      ldjson\n      episode {\n        objectId\n        title\n        available\n        whatsonId\n        brand\n        brandLogos {\n          ...brandLogosFragment\n          __typename\n        }\n        logo\n        primaryMeta {\n          ...metaFragment\n          __typename\n        }\n        secondaryMeta {\n          ...metaFragment\n          __typename\n        }\n        image {\n          ...imageFragment\n          __typename\n        }\n        durationRaw\n        durationValue\n        durationSeconds\n        playlist {\n          ...playlistFragment\n          __typename\n        }\n        onTimeRaw\n        offTimeRaw\n        ageRaw\n        regionRaw\n        announcementValue\n        name\n        episodeNumberRaw\n        episodeNumberValue\n        subtitle\n        richDescription {\n          __typename\n          html\n        }\n        program {\n          objectId\n          link\n          title\n          __typename\n        }\n        watchAction {\n          streamId\n          videoId\n          avodUrl\n          avodPlatform\n          resumePoint\n          completed\n          __typename\n        }\n        shareAction {\n          title\n          description\n          image {\n            templateUrl\n            __typename\n          }\n          url\n          __typename\n        }\n        favoriteAction {\n          id\n          title\n          favorite\n          programWhatsonId\n          programUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\nfragment metaFragment on MetaDataItem {\n  __typename\n  type\n  value\n  shortValue\n  longValue\n}\nfragment imageFragment on Image {\n  __typename\n  objectId\n  alt\n  title\n  focalPoint\n  templateUrl\n}\nfragment seoFragment on SeoProperties {\n  __typename\n  title\n  description\n}\nfragment socialSharingFragment on SocialSharingProperties {\n  __typename\n  title\n  description\n  image {\n    __typename\n    objectId\n    templateUrl\n  }\n}\nfragment brandLogosFragment on Logo {\n  colorOnColor\n  height\n  mono\n  primary\n  type\n  width\n}\nfragment playlistFragment on Playlist {\n  __typename\n  objectId\n  activeListId\n  lists {\n    ... on PaginatedTileList {\n      ...basicPaginatedTileListFragment\n      __typename\n    }\n    ... on StaticTileList {\n      ...basicStaticTileListFragment\n      __typename\n    }\n    ... on NoContent {\n      __typename\n      objectId\n      title\n      text\n      noContentType\n    }\n    __typename\n  }\n}\nfragment basicStaticTileListFragment on StaticTileList {\n  __typename\n  objectId\n  listId\n  displayType\n  expires\n  tileVariant\n  tileContentType\n  tileOrientation\n  title\n  items {\n    ...tileFragment\n    __typename\n  }\n  ... on IComponent {\n    ...componentTrackingDataFragment\n    __typename\n  }\n}\nfragment tileFragment on Tile {\n  ... on IIdentifiable {\n    __typename\n    objectId\n  }\n  ... on IComponent {\n    ...componentTrackingDataFragment\n    __typename\n  }\n  ... on ITile {\n    description\n    title\n    active\n    action {\n      ...actionFragment\n      __typename\n    }\n    actionItems {\n      ...actionItemFragment\n      __typename\n    }\n    image {\n      ...imageFragment\n      __typename\n    }\n    primaryMeta {\n      ...metaFragment\n      __typename\n    }\n    secondaryMeta {\n      ...metaFragment\n      __typename\n    }\n    tertiaryMeta {\n      ...metaFragment\n      __typename\n    }\n    indexMeta {\n      __typename\n      type\n      value\n    }\n    statusMeta {\n      __typename\n      type\n      value\n    }\n    labelMeta {\n      __typename\n      type\n      value\n    }\n    __typename\n  }\n  ... on ContentTile {\n    brand\n    brandLogos {\n      ...brandLogosFragment\n      __typename\n    }\n    __typename\n  }\n  ... on BannerTile {\n    compactLayout\n    backgroundColor\n    textTheme\n    brand\n    brandLogos {\n      ...brandLogosFragment\n      __typename\n    }\n    ctaText\n    passUserIdentity\n    titleArt {\n      objectId\n      templateUrl\n      __typename\n    }\n    __typename\n  }\n  ... on EpisodeTile {\n    description\n    formattedDuration\n    available\n    chapterStart\n    action {\n      ...actionFragment\n      __typename\n    }\n    playAction: watchAction {\n      pageUrl: videoUrl\n      resumePointProgress\n      resumePointTotal\n      completed\n      __typename\n    }\n    episode {\n      __typename\n      objectId\n      program {\n        __typename\n        objectId\n        link\n      }\n    }\n    epgDuration\n    __typename\n  }\n  ... on PodcastEpisodeTile {\n    formattedDuration\n    available\n    programLink: podcastEpisode {\n      objectId\n      podcastProgram {\n        objectId\n        link\n        __typename\n      }\n      __typename\n    }\n    playAction: listenAction {\n      pageUrl: podcastEpisodeLink\n      resumePointProgress\n      resumePointTotal\n      completed\n      __typename\n    }\n    __typename\n  }\n  ... on PodcastProgramTile {\n    link\n    __typename\n  }\n  ... on ProgramTile {\n    link\n    __typename\n  }\n  ... on AudioLivestreamTile {\n    brand\n    brandsLogos {\n      brand\n      brandTitle\n      logos {\n        ...brandLogosFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on LivestreamTile {\n    description\n    __typename\n  }\n  ... on ButtonTile {\n    icon\n    iconPosition\n    mode\n    __typename\n  }\n  ... on RadioEpisodeTile {\n    action {\n      ...actionFragment\n      __typename\n    }\n    available\n    epgDuration\n    formattedDuration\n    thumbnailMeta {\n      ...metaFragment\n      __typename\n    }\n    ...componentTrackingDataFragment\n    __typename\n  }\n  ... on SongTile {\n    startDate\n    formattedStartDate\n    endDate\n    __typename\n  }\n  ... on RadioProgramTile {\n    objectId\n    __typename\n  }\n}\nfragment actionFragment on Action {\n  __typename\n  ... on FavoriteAction {\n    favorite\n    id\n    programUrl\n    programWhatsonId\n    title\n    __typename\n  }\n  ... on ListDeleteAction {\n    listName\n    id\n    listId\n    title\n    __typename\n  }\n  ... on ListTileDeletedAction {\n    listName\n    id\n    listId\n    __typename\n  }\n  ... on PodcastEpisodeListenAction {\n    id: audioId\n    podcastEpisodeLink\n    resumePointProgress\n    resumePointTotal\n    completed\n    __typename\n  }\n  ... on EpisodeWatchAction {\n    id: videoId\n    videoUrl\n    resumePointProgress\n    resumePointTotal\n    completed\n    __typename\n  }\n  ... on LinkAction {\n    id: linkId\n    linkId\n    link\n    linkType\n    openExternally\n    passUserIdentity\n    linkTokens {\n      __typename\n      placeholder\n      value\n    }\n    __typename\n  }\n  ... on ShareAction {\n    title\n    url\n    __typename\n  }\n  ... on SwitchTabAction {\n    referencedTabId\n    mediaType\n    link\n    __typename\n  }\n  ... on RadioEpisodeListenAction {\n    streamId\n    pageLink\n    startDate\n    __typename\n  }\n  ... on LiveListenAction {\n    streamId\n    livestreamPageLink\n    startDate\n    endDate\n    __typename\n  }\n  ... on LiveWatchAction {\n    streamId\n    livestreamPageLink\n    startDate\n    endDate\n    __typename\n  }\n}\nfragment actionItemFragment on ActionItem {\n  __typename\n  objectId\n  accessibilityLabel\n  action {\n    ...actionFragment\n    __typename\n  }\n  active\n  icon\n  iconPosition\n  mode\n  objectId\n  title\n}\nfragment componentTrackingDataFragment on IComponent {\n  trackingData {\n    data\n    perTrigger {\n      trigger\n      data\n      template {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\nfragment basicPaginatedTileListFragment on PaginatedTileList {\n  __typename\n  objectId\n  listId\n  displayType\n  expires\n  tileVariant\n  tileContentType\n  tileOrientation\n  title\n  paginatedItems(first: $lazyItemCount, after: $after, before: $before) {\n    __typename\n    edges {\n      __typename\n      cursor\n      node {\n        __typename\n        ...tileFragment\n      }\n    }\n    pageInfo {\n      __typename\n      endCursor\n      hasNextPage\n      hasPreviousPage\n      startCursor\n    }\n  }\n  ... on IComponent {\n    ...componentTrackingDataFragment\n    __typename\n  }\n}\nfragment trackingDataFragment on PageTrackingData {\n  data\n  perTrigger {\n    trigger\n    data\n    template {\n      id\n      __typename\n    }\n    __typename\n  }\n}","operationName": "VideoPage","variables": {"pageId": pageId}}
    json = post_request('https://www.vrt.be/vrtnu-api/graphql/public/v1', data=data, headers=headers)
    streamId = json['data']['page']['episode']['watchAction']['streamId']
    title = json['data']['page']['title']
    description = json['data']['page']['seo']['description']
    thumbnailUrl = json['data']['page']['socialSharing']['image']['templateUrl']
    date = json['data']['page']['episode']['primaryMeta'][2]['shortValue'].split(' ')[1].replace('/','-')
    hour = json['data']['page']['episode']['primaryMeta'][2]['longValue'].split(' ')
    hour = hour[len(hour)-1] + ':00'
    year = json['data']['page']['objectId'].split('/')[4]
    date = date + '-' + year + ' ' + hour
    return streamId, title, description, thumbnailUrl, date    

def get_pageId_and_fileName(url):
    url = url.split('/a-z/')[1]
    if url.endswith('/'):
        url = url[:-1]
    pageId = '/vrtnu/a-z/' + url + '.model.json'
    fileName = url.split('/')
    fileName = fileName[len(fileName)-1] + '.mp4'
    return pageId, fileName
    
def get_streamUrl(streamId, vrtmaxToken):
    url = 'https://media-services-public.vrt.be/media-aggregator/v2/media-items/' + streamId + '?vrtPlayerToken=' + vrtmaxToken + '&client=vrtnu-web%40PROD'
    a = get_request(url,{})
    if 'code' in a:
        if 'CONTENT_REQUIRES_AUTHENTICATION' == a['code']:
            print_error(STR_7)
    mpegUrl = a['targetUrls'][1]['url']
    streamUrl = mpegUrl.split('?')[0]
    if not 'nodrm' in streamUrl:
        print_error(STR_6)
    return streamUrl
    
def get_video_from_vrtmax(url):
    videos = []
    pageIdAndFileName = get_pageId_and_fileName(url)
    pageId = pageIdAndFileName[0]
    fileName = pageIdAndFileName[1]
    metadata = get_metadata(pageId)
    streamId = metadata[0]
    title = metadata[1]
    description = metadata[2]
    thumbnailUrl = metadata[3]
    date = metadata[4]
    vrtmaxToken = get_vrtmax_token()
    streamUrl = get_streamUrl(streamId,vrtmaxToken)
    video = Video(streamUrl, url, title, description, thumbnailUrl, fileName, date)
    videos.append(video)
    return videos