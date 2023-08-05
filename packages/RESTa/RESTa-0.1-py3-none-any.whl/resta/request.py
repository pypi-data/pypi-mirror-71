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


class _Request(object):
    def __init__(self, method, url):
        self.method = method.upper()
        self.headers = dict()
        self.url = url

    def emit(self, session):
        args = {
            'headers': self.headers}
        args.update(self._inject_body())
        return session.request(self.method, self.url, **args)

    def _inject_body(self):
        raise NotImplementedError


class BodyLessRequest(_Request):
    def _inject_body(self):
        return {}


class JsonRequest(_Request):
    def __init__(self, method, url, payload=None):
        super().__init__(method, url)
        if payload is None:
            payload = dict()
        self.payload = payload

    def _inject_body(self):
        return {'json': self.payload}
