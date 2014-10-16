# -*- coding: utf-8 -*-

# Copyright(C) 2013 Julien Veyssier
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

from weboob.capabilities.recipe import CapRecipe, Recipe
from weboob.tools.backend import Module

from .browser import CuisineazBrowser

import unicodedata

__all__ = ['CuisineazModule']


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


class CuisineazModule(Module, CapRecipe):
    NAME = 'cuisineaz'
    MAINTAINER = u'Julien Veyssier'
    EMAIL = 'julien.veyssier@aiur.fr'
    VERSION = '1.0'
    DESCRIPTION = u'Cuisine AZ French recipe website'
    LICENSE = 'AGPLv3+'
    BROWSER = CuisineazBrowser

    def get_recipe(self, id):
        return self.browser.get_recipe(id)

    def iter_recipes(self, pattern):
        # the search form does that so the url is clean of special chars
        # we go directly on search results by the url so we strip it too
        return self.browser.iter_recipes(strip_accents(unicode(pattern)).encode('utf-8'))

    def fill_recipe(self, recipe, fields):
        if 'nb_person' in fields or 'instructions' in fields:
            rec = self.get_recipe(recipe.id)
            recipe.picture_url = rec.picture_url
            recipe.instructions = rec.instructions
            recipe.ingredients = rec.ingredients
            recipe.comments = rec.comments
            recipe.author = rec.author
            recipe.nb_person = rec.nb_person
            recipe.cooking_time = rec.cooking_time
            recipe.preparation_time = rec.preparation_time

        return recipe

    OBJECTS = {
        Recipe: fill_recipe,
    }
