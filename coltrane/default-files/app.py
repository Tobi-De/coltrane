#!/usr/bin/env python

# Generated by coltrane==__coltrane_version__

from django.core.management import execute_from_command_line

from coltrane import initialize

wsgi = initialize()

if __name__ == "__main__":
    execute_from_command_line()
