#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars - This software is public domain

from subprocess import call


def load_nppes_and_pecos():
    call(["loadnppes.py", "y", "y", "y"])
    call(["load_pecos.py", "y", "y", "y"])


if __name__ == "__main__":
    load_nppes_and_pecos()
