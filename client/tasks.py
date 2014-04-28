# -*- coding: utf-8 -*-

import os

from invoke import task, run

HERE = os.path.abspath(os.path.dirname(__file__))

@task
def serve():
    os.chdir(HERE)
    run('grunt serve', pty=True)
