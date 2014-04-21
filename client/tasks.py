# -*- coding: utf-8 -*-
from invoke import task


@task
def build():
    print("building client app")
