# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""REANA client debugging commands."""

import logging
import traceback

import click
from reana_client.api.client import current_rs_api_client
from reana_client.api.client import ping as rs_ping
from reana_client.cli.utils import check_connection
from reana_client.version import __version__


@click.group(help='Configuration commands')
def configuration_group():
    """Configuration commands."""
    pass


@configuration_group.command('ping')
@click.pass_context
@check_connection
def ping(ctx):  # noqa: D301
    """Check connection to REANA server.

    The `ping` command allows to test connection to REANA server.

    Examples: \n
    \t $ reana-client ping
    """
    try:
        logging.info('Connecting to {0}'.format(
            current_rs_api_client.swagger_spec.api_url))
        response = rs_ping()
        click.echo(click.style('Connected to {0} - Server is running.'.format(
            current_rs_api_client.swagger_spec.api_url), fg='green'))
        logging.debug('Server response:\n{}'.format(response))

    except Exception as e:
        logging.debug(traceback.format_exc())
        logging.debug(str(e))
        click.echo(click.style(
            'Could not connect to the selected '
            'REANA cluster server at {0}.'.format(
                current_rs_api_client.swagger_spec.api_url),
            fg='red'), err=True)


@configuration_group.command('version')
@click.pass_context
def version(ctx):  # noqa: D301
    """Show version.

    The `version` command shows REANA client version.

    Examples: \n
    \t $ reana-client version
    """
    click.echo(__version__)
