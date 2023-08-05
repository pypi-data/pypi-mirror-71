# Copyright 2019 Novartis Institutes for BioMedical Research Inc. Licensed
# under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless
# required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.

import logging
import subprocess

from flask_api import status
from cellxgene_gateway.env import enable_annotations
from cellxgene_gateway.process_exception import ProcessException
from cellxgene_gateway.dir_util import make_annotations
from cellxgene_gateway.path_util import get_file_path, get_annotation_file_path

class SubprocessBackend:
    def __init__(self):
        pass

    def create_cmd(self, cellxgene_loc, file_path, port, scripts, annotation_file_path):
        if enable_annotations and not annotation_file_path is None:
            annotation_args_prefix = " --experimental-annotations"
            if annotation_file_path == "":
                annotation_args = f"{annotation_args_prefix} --experimental-annotations-output-dir {make_annotations(file_path)}"
            else:
                annotation_args = f"{annotation_args_prefix} --experimental-annotations-file {annotation_file_path}"
        else:
            annotation_args = ""
        cmd = (
            f"yes | {cellxgene_loc} launch {file_path}"
            + " --port "
            + str(port)
            + " --host 127.0.0.1"
            + annotation_args
        )

        for s in scripts:
            cmd += f" --scripts {s}"

        return cmd

    def launch(self, cellxgene_loc, scripts, cache_entry):

        cmd = self.create_cmd(
            cellxgene_loc, get_file_path(cache_entry.key), cache_entry.port, scripts, get_annotation_file_path(cache_entry.key)
        )
        logging.getLogger("cellxgene_gateway").info(f"launching {cmd}")
        process = subprocess.Popen(
            [cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        while True:
            output = process.stdout.readline().decode()
            if output == "[cellxgene] Type CTRL-C at any time to exit.\n":
                break
            elif output == "":
                stderr = process.stderr.read().decode()
                if (
                    "Error while loading file" in stderr
                    or "Could not open file" in stderr
                ):
                    message = "File was invalid."
                    http_status = status.HTTP_400_BAD_REQUEST
                else:
                    message = "Cellxgene failed to launch dataset."
                    http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

                cache_entry.status = "error"
                cache_entry.set_error(message, stderr, http_status)

                raise ProcessException.from_cache_entry(cache_entry)
            else:
                cache_entry.append_output(output)

        cache_entry.set_loaded(process.pid)

        return
