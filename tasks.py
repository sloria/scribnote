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
# Namespace client and server tasks to c and s, respectively
namespace.add_collection(client.tasks, 'c')
namespace.add_collection(server.tasks, 's')
namespace.add_task(serve)
