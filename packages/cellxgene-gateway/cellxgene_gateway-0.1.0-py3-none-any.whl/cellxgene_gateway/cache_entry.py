# Copyright 2019 Novartis Institutes for BioMedical Research Inc. Licensed
# under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless
# required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
import psutil
import logging
import datetime

from flask import make_response, request, render_template
from requests import get, post, put

from cellxgene_gateway import env
from cellxgene_gateway.cellxgene_exception import CellxgeneException
from cellxgene_gateway.util import current_time_stamp
from cellxgene_gateway.flask_util import querystring

class CacheEntry:
    def __init__(
        self,
        pid,
        key,
        port,
        launchtime,
        timestamp,
        status,
        message,
        all_output,
        stderr,
        http_status,
    ):
        self.pid = pid
        self.key = key
        self.port = port
        self.launchtime = launchtime
        self.timestamp = timestamp
        self.status = status
        self.message = message
        self.all_output = all_output
        self.stderr = stderr
        self.http_status = http_status

    @classmethod
    def for_key(cls, key, port):

        return cls(
            None,
            key,
            port,
            current_time_stamp(),
            current_time_stamp(),
            "loading",
            None,
            None,
            None,
            None,
        )

    def set_loaded(self, pid):
        self.pid = pid
        self.status = "loaded"

    def set_error(self, message, stderr, http_status):
        self.message = message
        self.stderr = stderr
        self.http_status = http_status
        self.status = "error"

    def append_output(self, output):
        if self.all_output == None:
            self.all_output = output
        else:
            self.all_output += output

    def terminate(self):
        pid = self.pid
        if pid != None and self.status != "terminated":
            terminated = []
            def on_terminate(p):
                terminated.append(p.pid)
            p = psutil.Process(pid)
            children = p.children()
            for child in children:
                child.terminate()
            psutil.wait_procs(children, callback=on_terminate)
            terminated.append(p.pid)
            p.terminate()
            psutil.wait_procs([p], callback=on_terminate)
            logging.getLogger("cellxgene_gateway").info(f"terminated {terminated}")
        self.status = "terminated"

    def serve_content(self, path):
        gateway_basepath = (
            f"{env.external_protocol}://{env.external_host}/view/{self.key.pathpart}/"
        )
        subpath = path[len(self.key.pathpart) :]  # noqa: E203
            
        if len(subpath) == 0:
            r = make_response(f"Redirect to {gateway_basepath}\n", 301)
            r.headers["location"] = gateway_basepath+querystring()
            return r
        elif self.status == "loading":
            launch_time = datetime.datetime.fromtimestamp(self.launchtime)
            return render_template(
                "loading.html", launchtime=launch_time, all_output=self.all_output
            )

        port = self.port
        cellxgene_basepath = f"http://127.0.0.1:{port}"
        headers = {}
        copy_headers = [
            'accept',
            'accept-encoding',
            'accept-language',
            'cache-control',
            'connection',
            'content-length',
            'content-type',
            'cookie',
            'host',
            'origin',
            'pragma',
            'referer',
            'sec-fetch-mode',
            'sec-fetch-site',
            'user-agent'
        ]
        for h in copy_headers:
            if h in request.headers:
                headers[h] = request.headers[h]

        full_path = cellxgene_basepath + subpath + querystring()

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            cellxgene_response = get(
                full_path, headers=headers
            )
        elif request.method == "PUT":
            cellxgene_response = put(
                full_path,
                headers=headers,
                data=request.data,
            )
        elif request.method == "POST":
            cellxgene_response = post(
                full_path,
                headers=headers,
                data=request.data,
            )
        else:
            raise CellxgeneException(
                f"Unexpected method {request.method}", 400
            )
        content_type = cellxgene_response.headers["content-type"]
        if "text" in content_type:
            cellxgene_content = cellxgene_response.content.decode()
            gateway_content = cellxgene_content.replace(
                "http://fonts.gstatic.com", "https://fonts.gstatic.com"
            ).replace(cellxgene_basepath, gateway_basepath)
        else:
            gateway_content = cellxgene_response.content

        resp_headers = {}
        for h in copy_headers:
            if h in cellxgene_response.headers:
                resp_headers[h] = cellxgene_response.headers[h]

        gateway_response = make_response(
            gateway_content,
            cellxgene_response.status_code,
            resp_headers,
        )

        return gateway_response
