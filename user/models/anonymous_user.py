# -*- coding: utf-8 -*-


from .mixin import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False
