#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''CLI module.'''

import datetime
import os
import sys
import time
import click
import re
import binascii
from .at import ATException
from .utils import *

__version__ = '1.8.0'


class CliException(Exception):
    '''Generic cli error exception.'''
    pass


def is_node_in_list(ctx, serial):
    node_list = command(ctx, "$LIST")

    for row in node_list:
        s = row.split(',', 1)[0]
        if s == serial:
            return True
    return False


@click.group()
@click.option('--device', '-d', type=str, help='Device path.', metavar="DEVICE")
@click.option('--zmq', type=str, help='ZMQ', metavar="HOST:PORT")
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, device=None, zmq=None):
    '''Cooper Control Tool.'''
    ctx.obj['device'] = device
    ctx.obj['zmq'] = zmq


@cli.command()
def devices():
    '''Print available devices.'''
    for port in get_ports():
        click.echo(port[0], err=True)


@cli.group()
@click.pass_context
def node(ctx):
    '''Manage the nodes'''


@node.command("list")
@click.pass_context
def node_list(ctx):
    '''List attached nodes'''
    node_list = command(ctx, "$LIST")

    if node_list:
        for serial in node_list:
            click.echo(serial)
    else:
        click.echo("Empty list")


@node.command("attach")
@click.argument('serial')
@click.argument('key')
@click.option('--alias', 'alias', type=str, help='Set alias')
@click.pass_context
def node_attach(ctx, serial, key, alias=""):
    '''Attach node'''
    if not re.match("^[0-9]{16}$", serial):
        ctx.fail("serial is in bad format.")

    if not re.match("^[0-9abcdef]{32}$", key):
        ctx.fail("key is in bad format.")

    if is_node_in_list(ctx, serial):
        ctx.fail("Already attach.")

    if alias:
        command(ctx, '$ATTACH=%s,%s,"%s"' % (serial, key, alias))
    else:
        command(ctx, '$ATTACH=%s,%s' % (serial, key))

    command(ctx, "&W")

    click.echo('OK')


@node.command("detach")
@click.argument('serial')
@click.pass_context
def node_detach(ctx, serial):
    '''Detach node'''
    if not re.match("^[0-9]{16}$", serial):
        ctx.fail("serial is in bad format")

    if not is_node_in_list(ctx, serial):
        ctx.fail("Node is not attached.")

    command(ctx, "$DETACH=" + serial)
    command(ctx, "&W")
    click.echo('OK')


@node.command("purge")
@click.pass_context
def node_purge(ctx):
    '''Detach all nodes'''
    command(ctx, "$PURGE")
    command(ctx, "&W")
    click.echo('OK')


@cli.group()
@click.pass_context
def config(ctx):
    '''Config'''


@config.command('channel')
@click.option('--set', 'set_channel', type=int, help='New cahnnel (from 0 to 20)')
@click.pass_context
def config_channel(ctx, set_channel=None):
    '''Channel'''
    if set_channel is not None:
        if set_channel < 0 or set_channel > 20:
            ctx.fail("Bad channel, must by from range from 0 to 20.")

        command(ctx, "$CHANNEL=%d" % set_channel)
        command(ctx, "&W")

    click.echo(command(ctx, "$CHANNEL?")[0][1:])


@config.command('key')
@click.option('--set', 'key', type=str, help='Set 128-bit AES key')
@click.option('--generate', is_flag=True, help='Generate')
@click.option('--add-node-to-dongle', 'attach_device', type=str, metavar="DEVICE")
@click.option('--add-node-to-dongle-zmq', 'attach_zmq', type=str, metavar="HOST:PORT")
@click.pass_context
def config_key(ctx, key=None, generate=False, attach_device=None, attach_zmq=None):
    '''128-bit AES key'''
    if generate:
        key = binascii.hexlify(os.urandom(16)).decode('ascii')

    if not key:
        ctx.fail('Missing option "--set" or "--generate".')

    if len(key) != 32:
        ctx.fail("The key length is expected 32 characters.")

    key = key.lower()

    command(ctx, "$KEY=%s" % key)
    command(ctx, "&W")

    serial = command(ctx, "+CGSN")[0][7:]

    if attach_device or attach_zmq:
        gwctx = {'device': attach_device, 'zmq': attach_zmq}
        if is_node_in_list(gwctx, serial):
            command(gwctx, "$DETACH=" + serial)
        command(gwctx, '$ATTACH=%s,%s' % (serial, key))
        command(gwctx, "&W")

    click.echo("%s %s" % (serial, key))


@config.command('lock')
@click.option('--password', type=str, help='Max 16 char.')
@click.pass_context
def config_lock(ctx, password=None):
    '''Lock'''
    if password:
        if len(password) > 16:
            ctx.fail("Bad password, max 16 char.")
        command(ctx, '$LOCK="%s"' % password)
        command(ctx, "&W")

    click.echo('Device is locked.' if command(ctx, "$LOCK?")[0] == '1' else 'Device is unlocked.')


@config.command('unlock')
@click.option('--password', type=str, help='Max 16 char.', required=True)
@click.pass_context
def config_unlock(ctx, password=None):
    '''Lock'''
    if password:
        if len(password) > 16:
            ctx.fail("Bad password, max 16 char.")
        command(ctx, '$UNLOCK="%s"' % password)
        command(ctx, "&W")

    click.echo('Device is locked.' if command(ctx, "$LOCK?")[0] == '1' else 'Device is unlocked.')


@cli.command('info')
@click.pass_context
def info(ctx):
    '''Info'''
    click.echo('Model: ' + command(ctx, "+CGMM")[0][7:])
    click.echo('ID:    ' + command(ctx, "+CGSN")[0][7:])


@cli.command('status')
@click.pass_context
def status(ctx):
    '''Print status'''
    for line in command(ctx, "$STATUS"):
        click.echo(line[1:])


@cli.command('reset')
@click.pass_context
def reset(ctx):
    '''Reset'''
    if ctx.obj['zmq']:
        raise CliException("Zmq doesn't support reset")

    at = create_at(ctx)
    if at:
        at.ftdi_reset_sequence()
        click.echo("OK")


def main():
    '''Application entry point.'''
    try:
        cli(obj={}),
    except ATException as e:
        click.echo(str(e), err=True)
        sys.exit(1)
    except CliException as e:
        click.echo(str(e), err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
