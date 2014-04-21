# -*- coding: utf-8 -*-
"""The root invoke task namespace. Allows both client and server app
tasks to be run from the project root.
"""
from invoke import Collection

import client.tasks
import server.tasks

namespace = Collection()
namespace.add_collection(client.tasks, 'clt')
namespace.add_collection(server.tasks, 'srv')
