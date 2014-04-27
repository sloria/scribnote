# -*- coding: utf-8 -*-

import os

from invoke import task, run


@task
def serve():
    run('grunt serve', pty=True)
