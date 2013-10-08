"tools for lefigaro backend"
# -*- coding: utf-8 -*-

# Copyright(C) 2011  Julien Hebert
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

import re


def url2id(url):
    "return an id from an url"
    regexp = re.compile("(^.*),([0-9]+)\.html$")
    match = regexp.match(url)
    if match:
        return match.group(2)
    else:
        raise ValueError("Can't find an id for the url")


def rssid(entry):
    return url2id(entry.id)
