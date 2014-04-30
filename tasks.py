# -*- coding: utf-8 -*-
"""The root invoke task namespace. Allows both client and server app
tasks to be run from the project root.
"""
from invoke import Collection, task

import client.tasks
import server.tasks
import app


@task
def serve():
    app.app.run(debug=True)


namespace = Collection()
namespace.add_collection(client.tasks, 'clt')
namespace.add_collection(server.tasks, 'srv')
namespace.add_task(serve)
