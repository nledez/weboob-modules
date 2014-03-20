# -*- coding: utf-8 -*-

# Copyright(C) 2014      Bezleputh
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from weboob.tools.browser2 import PagesBrowser, URL, Profile, Firefox

from .calendar import SensCritiquenCalendarEvent
from .pages import AjaxPage, EventPage, JsonResumePage

import re

__all__ = ['SenscritiqueBrowser']


class SensCritiqueAjaxProfile(Profile):
    def setup_session(self, session):
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows; U; Windows "
                                "NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
                                " GTB7.1 (.NET CLR 3.5.30729)",
                                "Accept": "text/html, */*; q=0.01",
                                "X-Requested-With": "XMLHttpRequest",
                                "Referer": "http://www.senscritique.com/sc/tv_guides",
                                "Origin": "http://www.senscritique.com",
                                "Accept-Language": "fr-fr;q=0.667",
                                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                })


class SensCritiqueJsonProfile(Profile):
    def setup_session(self, session):
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows; U; Windows "
                                "NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
                                " GTB7.1 (.NET CLR 3.5.30729)",
                                "Accept": "application/json, text/javascript, */*; q=0.01",
                                "X-Requested-With": "XMLHttpRequest",
                                })


class SenscritiqueBrowser(PagesBrowser):
    ENCODING = 'utf-8'

    BASEURL = 'http://www.senscritique.com'

    program_page = URL('/sc/tv_guides')
    ajax_page = URL('/sc/tv_guides/gridContent.ajax', AjaxPage)
    event_page = URL('/film/(?P<_id>.*)', EventPage)
    json_page = URL('/sc/products/storyline/(?P<_id>.*).json', JsonResumePage)

    LIMIT = 25  # number of results returned for each ajax call (defined in the website).

    LIMIT_NB_PAGES = 10  # arbitrary limit to avoid infinitive loop that can occurs if total number of films is a multiple of LIMIT (in website it causes an infinite scroll)

    """
    HEADER_RESUME = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows "
                     "NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
                     " GTB7.1 (.NET CLR 3.5.30729)",
                     "Accept": "application/json, text/javascript, */*; q=0.01",
                     "X-Requested-With": "XMLHttpRequest",
                     }
    """

    DATA = {'order': 'chrono',
            'without_product_done': '0',
            'period': 'cette-semaine',
            'limit': '%d' % LIMIT,
            }

    def set_package_settings(self, package, channels):
        url = 'http://www.senscritique.com/sc/tv_guides/saveSettings.json'
        params = {'network':    package}
        for channel in channels:
            params['channels[]'] = channel
        self.open(url, data=params)

    def list_events(self, date_from, date_to=None, package=None, channels=None):
        self.program_page.stay_or_go()
        page_nb = 1

        if package and channels:
            self.set_package_settings(package, channels)

        self._setup_session(SensCritiqueAjaxProfile())
        while True:
            self.DATA['page'] = '%d' % page_nb
            page = self.ajax_page.open(data=self.DATA)
            nb_events = page.count_events()
            events = page.list_events(date_from=date_from, date_to=date_to)

            for event in events:
                yield event

            if nb_events < self.LIMIT or page_nb >= self.LIMIT_NB_PAGES:
                break

            page_nb += 1

    def get_event(self, _id, event=None):
        if not event:
            self.program_page.stay_or_go()
            page_nb = 1

            self._setup_session(SensCritiqueAjaxProfile())
            while True:
                self.DATA['page'] = '%d' % page_nb
                page = self.ajax_page.open(data=self.DATA)
                event = page.list_events(_id=_id)
                nb_events = page.count_events()
                if event or nb_events < self.LIMIT or page >= self.LIMIT_NB_PAGES:
                    break

                page += 1

        if event:
            if not isinstance(event, SensCritiquenCalendarEvent):
                event = event.next()

            event.resume = self.get_resume(_id)

            self._setup_session(Firefox())
            event = self.event_page.go(_id=_id).get_event(obj=event)

            return event

    def get_resume(self, _id):
        self._setup_session(SensCritiqueJsonProfile())
        re_id = re.compile('^/?(.*)/.*', re.DOTALL)
        a_id = re_id.search(_id).group(1)

        return self.json_page.go(_id=a_id).get_resume()
        # return "get resume"
        """
        self.HEADER_RESUME['Referer'] = url
        req = urllib2.Request('http://www.senscritique.com/sc/products/storyline/%s.json' % _id,
                              headers=self.HEADER_RESUME)
        response = self.open(req)
        result = simplejson.loads(response.read(), self.ENCODING)
        if result['json']['success']:
            return result['json']['data']
        """
