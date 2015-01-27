# -*- coding: utf-8 -*-
###############################################################################
###############################################################################
# Anime-On
###############################################################################
###############################################################################
### Imports ###
import re
from common import (_addon, addpr, nURL, eod, ContextMenu_Movies, ContextMenu_Series, ContextMenu_Episodes, set_view, addst, addonPath, GetDataBeetwenMarkers)
from metahandler import metahandlers
#from metahandler import metacontainers
### ##########################################################################
### ##########################################################################
site = addpr('site', '')
section = addpr('section', '')
url = addpr('url', '')
mainSite = 'http://animeon.pl/'
metaget = metahandlers.MetaData(preparezip=False)
fanartAol = addonPath + '/art/japan/fanart.jpg'
nexticon = addonPath + '/art/next.png'


def Pageanimeon(url, page='', metamethod=''):
    html = nURL(url).replace('\n','')
    Browse_ItemAon(html, metamethod)
    eod()


def Browse_ItemAon(html, metamethod='', content='tvshows', view='515'):
    if (len(html) == 0):
        return
    data = re.findall("<img src='http://animeon.pl/images/anime_min/mins/(.+?)'(.+?)<a href='(.+?)'>(.+?)</a></strong>(.+?)<div>(.+?)</div>", html)
    ItemCount = len(data)
    for item in data:
            _url = item[2]
            name = item[3]
            img = 'http://animeon.pl/images/anime_min/' + item [0]
            fanart = fanartAol
            plot = item[5]
            labs = {}
            try:
                labs['plot'] = plot
            except:
                labs['plot'] = ''
###
            pars = {'mode': 'EpisodesAnimeon', 'site': site, 'section': section, 'title': name, 'url': _url, 'img': img, 'fanart': fanart}
            contextLabs = {'title': name, 'url': _url, 'img': img, 'fanart': fanart, 'todoparams': _addon.build_plugin_url(pars), 'site': site, 'section': section, 'plot': labs['plot']}
            if   section == 'movie':
                contextMenuItems = ContextMenu_Movies(contextLabs)
            elif section == 'animeon':
                contextMenuItems = ContextMenu_Series(contextLabs)
            else:
                contextMenuItems = []
            labs['title'] = name
            _addon.add_directory(pars, labs, is_folder=True, fanart=fanart, img=img, contextmenu_items=contextMenuItems, total_items=ItemCount)
# szukanie następnej strony
    npage = url[:-2] + str(int(url[-2:]) + 20)
    if -1 != html.find("div class='pagenav"):
            _addon.add_directory({'mode': 'Pageanimeon', 'site': site, 'section': section, 'url': npage, 'page': npage}, {'title': "Next page"}, is_folder=True, fanart=fanartAol, img=nexticon)
    set_view(content, view_mode=addst('tvshows-view'))


def Browse_EpisodesAnimeon(url, page='', content='episodes', view='515'):
#    print url
    if url == '':
        return
    html = nURL(url)
    html = GetDataBeetwenMarkers(html, "<div class='anime-desc-title'><h2>Odcinki</h2></div>", '<div class="float-left"><h2 class="commentsFormH">Komentarze</h2></div>', False)[1]
    data = re.findall("<a href='(.+?)'><b>(.+?)</b> - (.+?)</a>", html)
    ItemCount = len(data)
    for item in data:
        url = item[0]
        name = item[2].replace('o', 'O')
        img = ""
        fanart = fanartAol
        plot = ""
        labs = {}
        try:
            labs['plot'] = plot
        except:
            labs['plot'] = ''
###
        contextLabs = {'title': name, 'year': '0000', 'url': url, 'img': img, 'fanart': fanart, 'DateAdded': '', 'plot': labs['plot']}
        contextMenuItems = ContextMenu_Episodes(labs=contextLabs)
        pars = {'mode': 'Version', 'site': site, 'section': section, 'title': name, 'url': url, 'img': img, 'fanart': fanart}
        labs['title'] = name
        _addon.add_directory(pars, labs, is_folder=True, fanart=fanart, img=img, contextmenu_items=contextMenuItems, total_items=ItemCount)
    set_view(content, int(addst('links-view')))
    eod()


def Browse_Version(url, page='', content='episodes', view='515'):
    if url == '':
        return
    html = nURL(url)
    html = GetDataBeetwenMarkers(html, "<div class='version-list'><ul>", "<a>Oznacz jako obejrzany</a>", False)[1]
    data = re.findall("<li><a href='(.+?)'>Wersja (.+?)</a><li>", html)
    ItemCount = len(data)
    for item in data:
        url = mainSite + item[0].replace('http://animeon.com.pl/', '')
        name = item[1]
        fanart = fanartAol
        plot = ""
        labs = {}
        try:
            labs['plot'] = plot
        except:
            labs['plot'] = ''
        html = nURL(url)
        html = GetDataBeetwenMarkers(html, "<div class='float-left player-container' style='display: none'><center>", "<br><br>", False)[1]
        data = re.findall("src='(.+?)'", html)
        for item in data:
            url2 = item
            print url2
            if ('video.sibnet.ru' in url2):
                    url2 = url2.replace('swf', 'php')
            elif ('archive.org' in url2):
                    url2 = url2.replace('http:', '')
                    url2 = 'http:' + url2
            elif ('animeon.com.pl/episodes/players/vk.php' in url2):
                    html = nURL(url2)
                    data = re.findall("src='(.+?)'", html)
                    for item in data:
                        url2 = item
###
            contextLabs = {'title': name, 'year': '0000', 'url': url, 'fanart': fanart, 'DateAdded': ''}
            contextMenuItems = ContextMenu_Episodes(labs=contextLabs)
            pars = {'mode': 'PlayFromHost', 'site': site, 'section': section, 'title': name, 'url': url2, 'fanart': fanart}
            labs['title'] = name
            _addon.add_directory(pars, labs, is_folder=False, fanart=fanart, contextmenu_items=contextMenuItems, total_items=ItemCount)
    set_view(content, int(addst('tvshows-view')))
    eod()




