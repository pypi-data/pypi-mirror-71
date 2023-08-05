#  Copyright (c) 2020 Dmitry Bogun. Contacts: <nayka@nyaka.org>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import collections
import os.path
import pathlib
import urllib.parse


class URL(object):
    def __init__(self, base_url, query_args=None):
        if not isinstance(base_url, urllib.parse.ParseResult):
            base_url = urllib.parse.urlparse(base_url)

        if query_args is None:
            query_args = dict()

        query = self._merge_query_string(base_url.query, query_args)
        self.base = base_url._replace(query=query)

    def __call__(self, *path, **query_args):
        prefix = pathlib.PurePosixPath('/')
        prefix /= self.base.path

        path = list(path)
        while path and not path[0]:
            path = path.pop(0)

        if path:
            path[0] = path[0].lstrip('/')

        for chunk in path:
            prefix /= chunk

        replace = {
            'path': os.path.normpath(str(prefix))}
        if query_args:
            replace['query'] = self._merge_query_string(self.base.query, query_args)

        return type(self)(self.base._replace(**replace))

    def geturl(self):
        return self.base.geturl()

    @classmethod
    def _merge_query_string(cls, base, update):
        query = urllib.parse.parse_qsl(base)
        query = cls._merge_query_args(query, update)
        return urllib.parse.urlencode(query)

    @staticmethod
    def _merge_query_args(base, update):
        query = []
        wipe_out = set()
        for k, v in update.items():
            if v is None:
                wipe_out.add(k)
                continue

            if isinstance(v, collections.Sequence) and not isinstance(v, str):
                for entry in v:
                    query.append((k, entry))
            else:
                query.append((k, v))

        query[:0] = [x for x in base if x[0] not in wipe_out]
        return query
