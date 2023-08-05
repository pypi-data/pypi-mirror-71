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


class Endpoint(object):
    def __init__(self, session_provider, context=None):
        self.session_provider = session_provider
        self.context = context

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def _handle(self, request):
        self._inject_headers(request)
        return request.emit(self.session_provider())

    def _inject_headers(self, request):
        pass
