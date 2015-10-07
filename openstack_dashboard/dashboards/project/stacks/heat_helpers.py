# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf import settings
import glob
import os
import yaml


HEAT_ROOT = getattr(settings, "HEAT_ROOT", "/srv/heat")

TEMPLATE_PATH = "template"
ENV_PATH = "env"

HOT = ".yaml"
ENV = ".env"

HOT_MASK = "*%s" % HOT
ENV_MASK = "*%s" % ENV


def filename(path):
    """helper
    return filename without extension
    """
    return os.path.basename(path).split(".")[0]


def get_templates(choices=True):
    """if choices is False return array of full path
    """

    path = "/".join([HEAT_ROOT, TEMPLATE_PATH])

    templates = []

    for path in glob.glob("/".join([path, HOT_MASK])):
        name = filename(path)
        templates.append((name, name.replace("_", " ").capitalize()))

    return templates


def get_environments(template_name=None):
    """return environments choices
    """
    path = "/".join([HEAT_ROOT, ENV_PATH])

    environments = []

    if template_name:
        join = [path, template_name, ENV_MASK]
    else:
        join = [path, ENV_MASK]

    for path in glob.glob("/".join(join)):
        name = filename(path)
        environments.append((name, name.replace("_", " ").capitalize()))

    return environments


def get_template_data(name):
    """load and return template data
    """

    path = "/".join([HEAT_ROOT, TEMPLATE_PATH, "".join([name, HOT])])

    try:
        f = open(path, 'r')
        data = yaml.load(f)
    except Exception as e:
        raise e
    finally:
        f.close()

    if 'heat_template_version' in data:
        data['heat_template_version'] = str(data['heat_template_version'])
    return data


def get_environment_data(template_name, name):
    """load and return parameters data
    """

    path = "/".join([HEAT_ROOT, ENV_PATH, template_name,
                     "".join([name, ENV])])

    try:
        f = open(path, 'r')
        data = yaml.load(f)
    except Exception as e:
        raise e
    finally:
        f.close()

    return data
