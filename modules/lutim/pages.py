# -*- coding: utf-8 -*-

# Copyright(C) 2014      Vincent A
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


from weboob.tools.browser import BasePage
import re

__all__ = ['PageAll']


class PageAll(BasePage):
    def post(self, name, content, max_days):
        pass

    def get_info(self):
        for link in self.browser.links():
            linkurl = link.absolute_url
            m = re.match(re.escape(self.url) + '([a-zA-Z0-9]+)$', linkurl)
            if m:
                return {'id': m.group(1)}
