# This file exists within 'dob':
#
#   https://github.com/hotoffthehamster/dob
#
# Copyright © 2018-2020 Landon Bouma,  2015-2016 Eric Goller.  All rights reserved.
#
# 'dob' is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License  as  published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any   later    version.
#
# 'dob' is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY  or  FITNESS FOR A PARTICULAR
# PURPOSE.  See  the  GNU General Public License  for  more details.
#
# You can find the GNU General Public License reprinted in the file titled 'LICENSE',
# or visit <http://www.gnu.org/licenses/>.

"""A time tracker for the command line. Utilizing the power of hamster! [nark]."""

# BREADCRUMB: PROFILING
from nark.helpers.dev.profiling import profile_elapsed
# BREADCRUMB: PROFILING
# E402 module level import not at top of file
profile_elapsed('To dob:   _top')  # noqa: E402

from gettext import gettext as _

import os
import re
import sys
from functools import update_wrapper

import click_hotoffthehamster as click

from dob_bright.crud.fact_dressed import FactDressed
from dob_bright.styling.ignore_cmds import (
    create_ignore_conf,
    echo_ignore_sections,
    echo_ignore_table,
    edit_ignore_file
)
from dob_bright.styling.rules_cmds import (
    create_rules_conf,
    echo_rules_conf,
    echo_rule_names,
    echo_rules_table,
    edit_rules_conf
)
from dob_bright.styling.styles_cmds import (
    create_styles_conf,
    echo_styles_conf,
    echo_styles_list,
    echo_styles_table,
    edit_styles_conf
)
from dob_bright.termio.echoes import click_echo
from dob_bright.termio.errors import dob_in_user_exit
from dob_bright.termio.paging import flush_pager

from .clickux import help_strings
from .clickux import help_string_add_fact
from .clickux.add_fact_help_group import ClickAddFactHelpGroup
from .clickux.aliasable_bunchy_plugin import ClickAliasableBunchyPluginGroup
from .clickux.bunchy_help import (
    cmd_bunch_group_introducing,
    cmd_bunch_group_edit,
    cmd_bunch_group_get_meta,
    cmd_bunch_group_generate_report,
    cmd_bunch_group_dbms,
    cmd_bunch_group_add_fact,
    cmd_bunch_group_ongoing_fact,
    cmd_bunch_group_personalize
)
from .clickux.cmd_options import (
    cmd_options_edit_item,
    cmd_options_fact_add,
    cmd_options_fact_dryable,
    cmd_options_fact_edit,
    cmd_options_fact_import,
    cmd_options_factoid,
    cmd_options_factoid_verify_none,
    cmd_options_factoid_verify_start,
    cmd_options_factoid_verify_end,
    cmd_options_factoid_verify_both,
    cmd_options_rule_name,
    cmd_options_styles_internal,
    cmd_options_styles_named
)
from .clickux.cmd_options_search import (
    cmd_options_any_search_query,
    cmd_options_output_format_any_input,
    postprocess_options_normalize_search_args,
    postprocess_options_output_format_any_input
)
from .clickux.help_command import help_command_help
from .clickux.help_detect import show_help_finally, show_help_if_no_command
from .clickux.induct_newbies import induct_newbies, insist_germinated
from .clickux.plugin_group import ensure_plugged_in
from .clickux.post_processor import post_processor
from .cmds_list import activity as list_activity
from .cmds_list import category as list_category
from .cmds_list import fact as list_fact
from .cmds_list import tag as list_tag
from .cmds_usage import activity as usage_activity
from .cmds_usage import category as usage_category
from .cmds_usage import tag as usage_tag
from .complete import tab_complete
from .config import (
    echo_config_table,
    echo_config_value,
    edit_config_file,
    write_config_value
)
from .copyright import echo_copyright, echo_license
from .demo import demo_config, demo_dob
from .details import echo_app_details, echo_app_environs, echo_data_stats
from .facts.add_fact import add_fact
from .facts.cancel_fact import cancel_fact
from .facts.echo_fact import echo_latest_ended, echo_ongoing_fact, echo_ongoing_or_ended
from .facts.edit_fact import edit_fact_by_pk
from .facts.import_facts import import_facts
from .migrate import control as migrate_control
from .migrate import downgrade as migrate_downgrade
from .migrate import upgrade as migrate_upgrade
from .migrate import upgrade_legacy_database_file
from .migrate import version as migrate_version
from .run_cli import dob_versions, pass_controller, pass_controller_context, run

# __all__ = ( ... )  # So many. Too tedious to list.


# ***
# *** [HELP]
# ***

@cmd_bunch_group_get_meta
@run.command(help=help_strings.HELP_HELP)
# (lb): Should not need the help-finally decorator, but doesn't seem to hurt, either:
#   @show_help_finally
@flush_pager
@click.pass_context
@click.argument('command', nargs=-1)
def help(ctx, command=None):
    """Show help."""
    help_command_help(ctx, command)


# ***
# *** [VERSION] Ye rote version command.
# ***

@cmd_bunch_group_get_meta
@run.command(help=help_strings.VERSION_HELP)
@show_help_finally
@flush_pager
@pass_controller
def version(controller):
    """Show version information."""
    include_all = controller.config['dev.catch_errors']
    click_echo(dob_versions(include_all=include_all))


# ***
# *** [LICENSE] Command.
# ***

@run.command(hidden=True, help=help_strings.LICENSE_HELP)
@show_help_finally
@flush_pager
def license():
    """Show license information."""
    _license()


def _license():
    """Show license information."""
    echo_license()


# ***
# *** [COPYRIGHT] Command.
# ***

@cmd_bunch_group_get_meta
@run.command(help=help_strings.COPYRIGHT_HELP)
@show_help_finally
@flush_pager
@pass_controller
def copyright(controller):
    """Display copyright information.."""
    echo_copyright()


@cmd_bunch_group_get_meta
@run.command(hidden=True, help=help_strings.ABOUT_COMMAND_HELP)
@show_help_finally
@flush_pager
@pass_controller
def about(controller):
    """Display copyright information.."""
    echo_copyright()


# ***
# *** [DETAILS] Command [about paths, config, etc.].
# ***

# MAYBE: (lb): Call this dob-show? dob-status? dob-info?
#   (2018-06-09: Trying aliases for now)
#   Some ideas: aliases=['show', 'status', 'info', 'config', 'details', 'appinfo'])
#   Though maybe 'show' should be alias for dob-current?
# MAYBE: Calling this 'appinfo' would make this command first in the --help....
#   @run.command(aliases=['show', 'status', 'info'], help=help_strings.DETAILS_HELP)
# See also similarly named commands that have generic meanings:
#   dob details | dob info | dob show
# i.e., details about what? info about what? showing what?
@cmd_bunch_group_get_meta
@run.command(aliases=['info'], help=help_strings.DETAILS_HELP)
@show_help_finally
@flush_pager
@click.option('--tmi', '--full', is_flag=True, help=help_strings.DETAILS_TMI_HELP)
@pass_controller
def details(controller, tmi):
    """List details about the runtime environment."""
    echo_app_details(controller, full=tmi)


# ***
# *** [ENVIRONS] Command [like details command, but shell-sourceable].
# ***

@cmd_bunch_group_get_meta
@run.command(aliases=['env'], help=help_strings.ENVIRONS_HELP)
@show_help_finally
@flush_pager
@pass_controller
def environs(controller):
    """List shell-sourceable details about the runtime environment."""
    echo_app_environs(controller)


# ***
# *** [DEBUG] Dump ya on a prompt.
# ***

@cmd_bunch_group_get_meta
@run.command(help=help_strings.DEBUG_HELP, hidden=True)
@show_help_finally
@flush_pager
@pass_controller
def debug(controller):
    """Break!"""
    import pdb
    pdb.set_trace()
    pass


# ***
# *** [DEMO] Command.
# ***

@cmd_bunch_group_introducing
@run.command('demo', help=help_strings.DEMO_HELP)
@show_help_finally
@flush_pager
@pass_controller
@demo_config
def demo_dob_and_nark(controller):
    """"""
    demo_dob(controller)


# ***
# *** [INIT] Command.
# ***

@cmd_bunch_group_introducing
@run.command('init', help=help_strings.INIT_HELP_OVERVIEW)
@show_help_finally
@flush_pager
@pass_controller
def init_config_and_store(controller):
    """"""
    controller.create_config_and_store(fact_cls=FactDressed)


# ***
# *** Shared Command Group settings.
# ***

run_group_kwargs = {
    # Groups should also use our class override so that usage is proper,
    # and other fancy features we add are part of group commands, too.
    'cls': ClickAliasableBunchyPluginGroup,
    # Ensure Click does not die on the -h/--help option, e.g.,
    # `dob config -h` should show help, not show "Error: Missing command."
    'invoke_without_command': True,
}


# ***
# *** [CONFIG] Commands.
# ***

@cmd_bunch_group_get_meta
@run.group('config', help=help_strings.CONFIG_GROUP_HELP, **run_group_kwargs)
@show_help_finally
@show_help_if_no_command
@flush_pager
@click.pass_context
def config_group(ctx):
    """Base `config` group command run prior to any of the dob-config commands."""
    pass  # The command group decorator prints help if no subcommand called.


# *** [CONFIG] CREATE

@config_group.command('create', aliases=['new'], help=help_strings.CONFIG_CREATE_HELP)
@show_help_finally
@flush_pager
@click.option('-f', '--force', is_flag=True,
              help=help_strings.CONFIG_CREATE_FORCE_HELP)
@pass_controller_context
@ensure_plugged_in
def config_create(ctx, controller, force):
    """"""
    controller.create_config(force)


# *** [CONFIG] SHOW

@config_group.command('show', aliases=['dump'], help=help_strings.CONFIG_SHOW_HELP)
@show_help_finally
@flush_pager
@cmd_options_output_format_any_input
@click.argument('section', nargs=1, default='')
@click.argument('keyname', nargs=1, default='')
@pass_controller_context
@ensure_plugged_in
def config_show(ctx, controller, section='', keyname='', **kwargs):
    """"""
    postprocess_options_output_format_any_input(kwargs)
    echo_config_table(controller, section, keyname, **kwargs)


# *** [CONFIG] EDIT

@config_group.command('edit', help=help_strings.CONFIG_EDIT_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def config_edit(ctx, controller):
    """"""
    edit_config_file(controller)


# *** [CONFIG] GET

@config_group.command('get', aliases=['read'], help=help_strings.CONFIG_GET_HELP)
@show_help_finally
@flush_pager
@click.argument('parts', nargs=-1, metavar='[SECTION] KEYNAME VALUE')
@pass_controller_context
@ensure_plugged_in
def config_value_get(ctx, controller, parts):
    """"""
    echo_config_value(ctx, controller, parts)


# *** [CONFIG] SET

@config_group.command('set', aliases=['write'], help=help_strings.CONFIG_SET_HELP)
@show_help_finally
@flush_pager
@click.argument('parts', nargs=-1, metavar='[SECTION] KEYNAME VALUE')
@pass_controller_context
@ensure_plugged_in
def config_value_set(ctx, controller, parts):
    """"""
    write_config_value(ctx, controller, parts)


# *** [CONFIG] UPDATE

@config_group.command('update', help=help_strings.CONFIG_UPDATE_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def config_update(ctx, controller):
    """Write "missing" key values to the user configuration file."""
    controller.round_out_config()


# ***
# *** [STYLES] Commands.
# ***

@cmd_bunch_group_personalize
@run.group('styles',
           help=help_strings.STYLES_GROUP_HELP,
           help_weight=10,
           **run_group_kwargs)
@show_help_finally
@show_help_if_no_command
@flush_pager
@click.pass_context
def styles_group(ctx):
    """Base `styles` group command run prior to any of the dob-styles commands."""
    pass  # The command group decorator prints help if no subcommand called.


# *** [STYLES] CREATE

@styles_group.command('create', aliases=['new'], help=help_strings.STYLES_CREATE_HELP)
@show_help_finally
@flush_pager
@cmd_options_styles_named
@click.option('-f', '--force', is_flag=True, help=help_strings.STYLES_CREATE_FORCE_HELP)
@pass_controller_context
@ensure_plugged_in
def styles_create(ctx, controller, name, force):
    """"""
    create_styles_conf(controller, name, force)


# *** [STYLES] CONF

@styles_group.command('conf', help=help_strings.STYLES_CONF_HELP)
@show_help_finally
@flush_pager
@cmd_options_styles_named
@cmd_options_styles_internal
# (lb): Cannot specify click.option name, and if just -a and --all, click uses
# all as the function parameter, which shadows the built-in. So add --complete.
@click.option('-a', '--complete', '--all', is_flag=True,
              help=_('Include all possible settings, even those not set by the style.'))
@pass_controller_context
@ensure_plugged_in
def styles_conf(ctx, controller, name, internal, complete):
    """"""
    echo_styles_conf(controller, name, internal, complete)


# *** [STYLES] EDIT

@styles_group.command('edit', help=help_strings.STYLES_EDIT_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def styles_edit(ctx, controller):
    """"""
    edit_styles_conf(controller)


# *** [STYLES] LIST

@styles_group.command('list', help=help_strings.STYLES_LIST_HELP)
@show_help_finally
@flush_pager
@cmd_options_styles_internal
@pass_controller_context
@ensure_plugged_in
def styles_list(ctx, controller, internal):
    """"""
    echo_styles_list(controller, internal)


# *** [STYLES] SHOW

@styles_group.command('show', aliases=['dump'], help=help_strings.STYLES_SHOW_HELP)
@show_help_finally
@flush_pager
@cmd_options_styles_named
@cmd_options_output_format_any_input
@pass_controller_context
@ensure_plugged_in
def styles_show(ctx, controller, name, **kwargs):
    """"""
    postprocess_options_output_format_any_input(kwargs)
    echo_styles_table(controller, name, **kwargs)


# ***
# *** [RULES] Commands.
# ***

@cmd_bunch_group_personalize
@run.group('rules',
           help=help_strings.RULES_GROUP_HELP,
           help_weight=20,
           **run_group_kwargs)
@show_help_finally
@show_help_if_no_command
@flush_pager
@click.pass_context
def rules_group(ctx):
    """Base `rules` group command run prior to any of the dob-rules commands."""
    pass  # The command group decorator prints help if no subcommand called.


# *** [RULES] CREATE

@rules_group.command('create', aliases=['new'], help=help_strings.RULES_CREATE_HELP)
@show_help_finally
@flush_pager
@click.option('-f', '--force', is_flag=True, help=help_strings.RULES_CREATE_FORCE_HELP)
@pass_controller_context
@ensure_plugged_in
def rules_create(ctx, controller, force):
    """"""
    create_rules_conf(controller, force)


# *** [RULES] CONF

@rules_group.command('conf', help=help_strings.RULES_CONF_HELP)
@show_help_finally
@flush_pager
@cmd_options_rule_name
# (lb): Cannot specify click.option name, and if just -a and --all, click uses
# all as the function parameter, which shadows the built-in. So add --complete.
@click.option('-a', '--complete', '--all', is_flag=True,
              help=_('Include all possible settings, even those not set by the style.'))
@pass_controller_context
@ensure_plugged_in
def rules_conf(ctx, controller, name, complete):
    """"""
    echo_rules_conf(controller, name, complete)


# *** [RULES] EDIT

@rules_group.command('edit', help=help_strings.RULES_EDIT_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def rules_edit(ctx, controller):
    """"""
    edit_rules_conf(controller)


# *** [RULES] LIST

@rules_group.command('list', help=help_strings.RULES_LIST_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def rules_list(ctx, controller):
    """"""
    echo_rule_names(controller)


# *** [RULES] SHOW

@rules_group.command('show', aliases=['dump'], help=help_strings.RULES_SHOW_HELP)
@show_help_finally
@flush_pager
@cmd_options_rule_name
@cmd_options_output_format_any_input
@pass_controller_context
@ensure_plugged_in
def rules_show(ctx, controller, name, **kwargs):
    """"""
    postprocess_options_output_format_any_input(kwargs)
    echo_rules_table(controller, name, **kwargs)


# ***
# *** [IGNORE] Commands.
# ***

@cmd_bunch_group_personalize
@run.group('ignore',
           help=help_strings.IGNORE_GROUP_HELP,
           help_weight=30,
           **run_group_kwargs)
@show_help_finally
@show_help_if_no_command
@flush_pager
@click.pass_context
def ignore_group(ctx):
    """Base `ignore` group command run prior to any of the dob-ignore commands."""
    pass  # The command group decorator prints help if no subcommand called.


# *** [IGNORE] CREATE

@ignore_group.command('create', aliases=['new'], help=help_strings.IGNORE_CREATE_HELP)
@show_help_finally
@flush_pager
@click.option('-f', '--force', is_flag=True, help=help_strings.IGNORE_CREATE_FORCE_HELP)
@pass_controller_context
@ensure_plugged_in
def ignore_create(ctx, controller, force):
    """"""
    create_ignore_conf(controller, force)


# *** [IGNORE] EDIT

@ignore_group.command('edit', help=help_strings.IGNORE_EDIT_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def ignore_edit(ctx, controller):
    """"""
    edit_ignore_file(controller)


# *** [IGNORE] LIST

@ignore_group.command('list', help=help_strings.IGNORE_LIST_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@ensure_plugged_in
def ignore_list(ctx, controller):
    """"""
    echo_ignore_sections(controller)


# *** [IGNORE] SHOW

@ignore_group.command('show', aliases=['dump'], help=help_strings.IGNORE_SHOW_HELP)
@show_help_finally
@flush_pager
@cmd_options_rule_name
@cmd_options_output_format_any_input
@pass_controller_context
@ensure_plugged_in
def ignore_show(ctx, controller, name, **kwargs):
    """"""
    postprocess_options_output_format_any_input(kwargs)
    echo_ignore_table(controller, name, **kwargs)


# ***
# *** [STORE] Commands.
# ***

# See also: 'migrate' commands. The store commands are mostly for initial setup.

@cmd_bunch_group_dbms
@run.group('store', help=help_strings.STORE_GROUP_HELP, **run_group_kwargs)
@show_help_finally
@show_help_if_no_command
@flush_pager
@click.pass_context
def store_group(ctx):
    """Base `store` group command run prior to dob-store commands."""
    pass


@store_group.command('create', aliases=['new'], help=help_strings.STORE_CREATE_HELP)
@show_help_finally
@flush_pager
@click.option('-f', '--force', is_flag=True,
              help=help_strings.STORE_CREATE_FORCE_HELP)
@pass_controller
def store_create(controller, force):
    """"""
    controller.create_data_store(force, fact_cls=FactDressed)


@store_group.command('path', help=help_strings.STORE_PATH_HELP)
@show_help_finally
@flush_pager
@pass_controller
def store_path(controller):
    """"""
    click_echo(controller.sqlite_db_path)


@store_group.command('url', help=help_strings.STORE_URL_HELP)
@show_help_finally
@flush_pager
@pass_controller
def store_url(controller):
    """"""
    click_echo(controller.data_store_url)


@store_group.command('upgrade-legacy', help=help_strings.STORE_UPGRADE_LEGACY_HELP)
@show_help_finally
@flush_pager
@click.argument('filename', nargs=1, type=click.File('r'), required=False)
@click.option('-f', '--force', is_flag=True,
              help=help_strings.STORE_UPGRADE_FORCE_HELP)
@pass_controller_context
@post_processor
def upgrade_legacy(ctx, controller, force, filename=None):
    """Migrate a legacy "Hamster" database."""
    # If filename is false, this method will raise.
    return upgrade_legacy_database_file(ctx, controller, file_in=filename, force=force)


# ***
# *** [STATS] Command.
# ***

@cmd_bunch_group_dbms
@run.command('stats', help=help_strings.STATS_HELP, help_weight=20)
@show_help_finally
@flush_pager
@pass_controller_context
@induct_newbies
def nark_stats(ctx, controller):
    """List stats about the user's data."""
    echo_data_stats(controller)


# ***
# *** [LIST] Commands.
# ***

@cmd_bunch_group_generate_report
# Use a command alias to avoid conflict with builtin of same name
# (i.e., we cannot declare this function, `def list()`).
@run.group(
    'list', help=help_strings.LIST_GROUP_HELP, help_weight=20, **run_group_kwargs,
)
@show_help_finally
@show_help_if_no_command
@flush_pager
@pass_controller_context
def list_group(ctx, controller):
    """Base `list` group command run prior to any of the dob-list commands."""
    # No-op; have already shown a help message.
    pass


# *** ACTIVITIES.

@list_group.command('activities', aliases=['activity', 'act'],
                    help=help_strings.LIST_ACTIVITIES_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='list', item='activity', match=True, group=False)
@pass_controller_context
@induct_newbies
def list_activities(ctx, controller, *args, **kwargs):
    """List matching activities, filtered and sorted."""
    query_activities(ctx, controller, *args, **kwargs)


def query_activities(ctx, controller, *args, **kwargs):
    postprocess_options_normalize_search_args(kwargs)
    if kwargs['show_usage'] or kwargs['show_duration']:
        handler = usage_activity.usage_activities
    else:
        handler = list_activity.list_activities
    handler(controller, *args, **kwargs)


# *** CATEGORIES.

@list_group.command('categories', aliases=['category', 'cat'],
                    help=help_strings.LIST_CATEGORIES_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='list', item='category', match=True, group=False)
@pass_controller_context
@induct_newbies
def list_categories(ctx, controller, *args, **kwargs):
    """List matching categories, filtered and sorted."""
    query_categories(ctx, controller, *args, **kwargs)


def query_categories(ctx, controller, *args, **kwargs):
    postprocess_options_normalize_search_args(kwargs)
    if kwargs['show_usage'] or kwargs['show_duration']:
        handler = usage_category.usage_categories
    else:
        handler = list_category.list_categories
    handler(controller, *args, **kwargs)


# *** TAGS.

@list_group.command('tags', aliases=['tag'], help=help_strings.LIST_TAGS_HELP)
@show_help_finally
@flush_pager
# TESTME/2020-05-16: group_target seems peculiar: it's not enabled on
# list-act or list-cat; but it could be interesting (to see what tags
# you use on which act@gories).
@cmd_options_any_search_query(command='list', item='tags', match=True, group=False)
@pass_controller_context
@induct_newbies
def list_tags(ctx, controller, *args, **kwargs):
    """List all tags, with filtering and sorting options."""
    query_tags(ctx, controller, *args, **kwargs)


def query_tags(ctx, controller, *args, **kwargs):
    postprocess_options_normalize_search_args(kwargs)
    if kwargs['show_usage'] or kwargs['show_duration']:
        handler = usage_tag.usage_tags
    else:
        handler = list_tag.list_tags
    handler(controller, *args, **kwargs)


# *** FACTS.

def _list_facts(controller, *args, cmd_journal=False, **kwargs):
    """Find matching facts, filtered and sorted."""
    postprocess_options_normalize_search_args(kwargs, cmd_journal=cmd_journal)
    list_fact.list_facts(controller, *args, **kwargs)


@list_group.command('facts', aliases=['fact'], help=help_strings.LIST_FACTS_HELP)
@show_help_finally
@flush_pager
# The `dob find` and `dob list fact` commands are the same.
@cmd_options_any_search_query(command='list', item='fact', match=True, group=True)
@pass_controller_context
@induct_newbies
def dob_list_facts(ctx, controller, *args, **kwargs):
    _list_facts(controller, *args, **kwargs)


# ***
# *** [SEARCH] Facts Command.
# ***

@cmd_bunch_group_generate_report
@run.command('find', aliases=['search'], help=help_strings.SEARCH_HELP, help_weight=5)
@show_help_finally
@flush_pager
# The `dob find` and `dob list fact` commands are the same.
@cmd_options_any_search_query(command='list', item='fact', match=True, group=True)
@pass_controller_context
@induct_newbies
def search_facts(ctx, controller, *args, **kwargs):
    _list_facts(controller, *args, **kwargs)


# ***
# *** [REPORT] Facts Command.
# ***

@cmd_bunch_group_generate_report
@run.command('report', help=help_strings.REPORT_HELP, help_weight=10)
@show_help_finally
@flush_pager
# The `dob report` command is `dob find` with specific defaults.
@cmd_options_any_search_query(command='journal', item='fact', match=True, group=True)
@pass_controller_context
@induct_newbies
def journal_report(ctx, controller, *args, **kwargs):
    # The journal command groups by Activity, Category, and Day by default,
    # unless the user specified a different grouping. Note that to apply no
    # grouping, the user would have to use the `dob find` command instead.
    _list_facts(controller, *args, cmd_journal=True, **kwargs)


# ***
# *** [USAGE] Commands.
# ***

@cmd_bunch_group_generate_report
@run.group(
    'usage', help=help_strings.USAGE_GROUP_HELP, help_weight=15, **run_group_kwargs,
)
@show_help_finally
@show_help_if_no_command
@flush_pager
@pass_controller_context
def usage_group(ctx, controller):
    """Base `usage` group command run prior to any of the dob-usage commands."""
    pass


# *** ACTIVITIES.

@usage_group.command('activities', aliases=['activity', 'act'],
                     help=help_strings.USAGE_ACTIVITIES_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='usage', item='activity', match=True, group=False)
@pass_controller_context
@induct_newbies
def usage_activities(ctx, controller, *args, **kwargs):
    """List all activities. Provide optional filtering by name."""
    query_activities(ctx, controller, *args, **kwargs)


# *** CATEGORIES.

@usage_group.command('categories', aliases=['category', 'cat'],
                     help=help_strings.USAGE_CATEGORIES_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='usage', item='category', match=True, group=False)
@pass_controller_context
@induct_newbies
def usage_categories(ctx, controller, *args, **kwargs):
    """List all categories. Provide optional filtering by name."""
    query_categories(ctx, controller, *args, **kwargs)


# *** TAGS.

@usage_group.command('tags', aliases=['tag'], help=help_strings.USAGE_TAGS_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='usage', item='tags', match=True, group=False)
@pass_controller_context
@induct_newbies
def usage_tags(ctx, controller, *args, **kwargs):
    """List all tags' usage counts, with filtering and sorting options."""
    query_tags(ctx, controller, *args, **kwargs)


# *** FACTS.

@usage_group.command('facts', aliases=['fact'], help=help_strings.USAGE_FACTS_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='usage', item='fact', match=True, group=True)
@pass_controller_context
@induct_newbies
def usage_facts(ctx, controller, *args, **kwargs):
    """List all tags' usage counts, with filtering and sorting options."""
    postprocess_options_normalize_search_args(kwargs)
    list_fact.list_facts(
        controller,
        *args,
        **kwargs,
    )


# ***
# *** [CURRENT-FACT] Commands: stop/cancel/current/latest/show.
# ***

@cmd_bunch_group_ongoing_fact
@run.command('cancel', help=help_strings.CANCEL_HELP)
@show_help_finally
@flush_pager
@click.option(
    '-f', '--force', '--purge', is_flag=True,
    help=_('Completely delete Fact, rather than just marking deleted.'),
)
@pass_controller_context
@induct_newbies
@post_processor
def cancel(ctx, controller, force):
    """Cancel the active Fact. Do not store the Fact in the backend."""
    return cancel_fact(controller, purge=force)


@cmd_bunch_group_ongoing_fact
@run.command('current', help=help_strings.CURRENT_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@induct_newbies
def current(ctx, controller):
    """Display the active Fact."""
    echo_ongoing_fact(controller)


@cmd_bunch_group_ongoing_fact
@run.command('latest', aliases=['last'], help=help_strings.LATEST_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@induct_newbies
def latest(ctx, controller):
    """Display the last saved Fact."""
    echo_latest_ended(controller)


@cmd_bunch_group_ongoing_fact
@run.command('show', help=help_strings.HELP_CMD_SHOW)
@show_help_finally
@flush_pager
@pass_controller_context
@induct_newbies
def show(ctx, controller):
    """Display the latest saved, or the active Fact."""
    echo_ongoing_or_ended(controller)


# ***
# *** [CREATE-FACT] Commands.
# ***

def generate_add_fact_command(time_hint):
    def _generate_add_fact_command(func):
        @cmd_options_fact_add
        @cmd_options_fact_dryable
        @pass_controller_context
        @induct_newbies
        @post_processor
        def _add_fact(ctx, controller, *args, editor, **kwargs):
            return add_fact(
                controller, *args, time_hint=time_hint, use_carousel=editor, **kwargs
            )
        return update_wrapper(_add_fact, func)
    return _generate_add_fact_command


@cmd_bunch_group_add_fact
@run.command("now", aliases=["now:"], help=help_strings.ADD_FACT_NOW)
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_none
@generate_add_fact_command("verify_none")
def add_fact_now(controller, *args, **kwargs):
    """Start or add a fact using the `now` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("on", aliases=["on:"], help=help_strings.ADD_FACT_ON,
             hidden=True)  # FIXME/2019-11-21: Remove aliases, but keep unique help.
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_none
@generate_add_fact_command("verify_none")
def add_fact_on(controller, *args, **kwargs):
    """Start or add a fact using the `on` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("at", aliases=["at:"], help=help_strings.ADD_FACT_AT)
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_start
@generate_add_fact_command("verify_start")
def add_fact_at(controller, *args, **kwargs):
    """Start or add a fact using the `at` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("from", help=help_strings.ADD_FACT_FROM)
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_both
@generate_add_fact_command("verify_both")
def add_fact_from(controller, *args, **kwargs):
    """Add a fact using the `from ... to/until` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("to", aliases=["to:"], help=help_strings.ADD_FACT_TO)
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_end
@generate_add_fact_command("verify_end")
def add_fact_to(controller, *args, **kwargs):
    """Start or add a fact using the `to` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("until", aliases=["until:"], help=help_strings.ADD_FACT_UNTIL,
             hidden=True)  # FIXME/2019-11-21: Remove aliases... but I like "until"!
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_end
@generate_add_fact_command("verify_end")
def add_fact_until(controller, *args, **kwargs):
    """Start or add a fact using the `until` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("then", aliases=["then:"], help=help_strings.ADD_FACT_THEN)
@show_help_finally
@flush_pager
# FIXME/2019-11-22: (lb): This right? (Because command is verify_then):
@cmd_options_factoid_verify_start
@generate_add_fact_command("verify_then")
def add_fact_then(controller, *args, **kwargs):
    """Start or add a fact using the `then` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("still", aliases=["still:"], help=help_strings.ADD_FACT_STILL)
@show_help_finally
@flush_pager
# FIXME/2019-11-22: (lb): This right? (Because command is verify_still):
@cmd_options_factoid_verify_start
@generate_add_fact_command("verify_still")
def add_fact_still(controller, *args, **kwargs):
    """Start or add a fact using the `still` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("after", aliases=["after:"], help=help_strings.ADD_FACT_AFTER)
@show_help_finally
@flush_pager
# FIXME/2019-11-22: (lb): This right? (Because command is verify_after):
@cmd_options_factoid_verify_start
@generate_add_fact_command("verify_after")
def add_fact_after(controller, *args, **kwargs):
    """Start or add a fact using the `after` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


@cmd_bunch_group_add_fact
@run.command("next", aliases=["next:"], help=help_strings.ADD_FACT_NEXT,
             hidden=True)  # FIXME/2019-11-21: Remove aliases, but keep unique help.
@show_help_finally
@flush_pager
# FIXME/2019-11-22: (lb): This right? (Because command is verify_after):
@cmd_options_factoid_verify_start
# Note that 'next' is really just an alias of 'after'.
@generate_add_fact_command("verify_after")
def add_fact_next(controller, *args, **kwargs):
    """Start or add a fact using the `next` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


# ***
# *** [START-STOP] Command(s).
# ***


# NOPE: @cmd_bunch_group_add_fact
@cmd_bunch_group_ongoing_fact
@run.command('start', help=help_strings.ADD_FACT_START, help_weight=5)
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_none
@generate_add_fact_command('verify_none')
def add_fact_start(controller, *args, **kwargs):
    """Start or add a fact using the `now` directive."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


# NOPE: @cmd_bunch_group_add_fact
@cmd_bunch_group_ongoing_fact
@run.command('stop', help=help_strings.STOP_HELP, help_weight=5)
@show_help_finally
@flush_pager
@cmd_options_factoid_verify_end
# (lb) verify_end is imprecise, because stop should always set end time
# to now. At least if you're being pedantic. I just want to have a group
# of latest-fact commands that's hopefully simpler to grok than the more
# expansive group of add-fact commands.
@generate_add_fact_command('verify_end')
def stop(controller, *args, **kwargs):
    """Complete the active fact (by setting its 'end')."""
    # Not reachable, because generate_add_fact_command.
    assert False  # pragma: no cover


# ***
# *** [ADD-FACT-HELP] Command(s).
# ***


add_group_kwargs = {
    # Use a special business class that munges the usage to show all add commands.
    'cls': ClickAddFactHelpGroup,
    'invoke_without_command': True,
}


@cmd_bunch_group_add_fact
# - Hide this command; we'll show the misdirecting 'add --show' command instead,
#   but this command is necessary to catch `dob add --help` (i.e., catch the
#   command `add` with the option `--help`, as opposed to the next command,
#   which is the command `add --show` with no option, e.g., `dob "add --show"`.
# - ADD_FACT_GROUP_NAME is 'add', and a class member to automate usage building.
@run.group(
    ClickAddFactHelpGroup.ADD_FACT_GROUP_NAME,  # 'add'
    help=help_string_add_fact.ADD_FACT_COMMON,
    hidden=True,
    **add_group_kwargs
)
@show_help_finally
@show_help_if_no_command
@flush_pager
@cmd_options_factoid
@cmd_options_fact_add
@cmd_options_fact_dryable
@pass_controller_context
@induct_newbies
@post_processor
def add_group(ctx, controller, *args, **kwargs):
    """Base `add` group command run prior to any of the dob-add commands."""
    pass


@cmd_bunch_group_add_fact
# - (lb): Just a little "hack" (more like "misdirection") to make the first entry
#   in the add-fact bunchy group a hint to the user how to get help on adding Facts.
# - ADD_FACT_GROUP_HELP is 'add --help', and a class member to automate usage building.
@run.group(
    ClickAddFactHelpGroup.ADD_FACT_GROUP_HELP,  # 'add --help'
    help=help_string_add_fact.ADD_FACT_COMMON,
    **add_group_kwargs
)
@show_help_finally
@show_help_if_no_command
@flush_pager
@cmd_options_factoid
@cmd_options_fact_add
@cmd_options_fact_dryable
@pass_controller_context
@induct_newbies
@post_processor
def add_help(*args, **kwargs):
    """Misdirecting "add --help" command to improve general help."""
    pass


# ***
# *** [EDIT] Command(s).
# ***

@cmd_bunch_group_edit
@run.command('edit', help=help_strings.EDIT_FACT_HELP)
@show_help_finally
@flush_pager
@cmd_options_edit_item
@cmd_options_fact_edit
@pass_controller_context
@induct_newbies
@post_processor
def edit_group(ctx, controller, *args, **kwargs):
    """Base `edit` group command run prior to any of the dob-edit commands."""
    # NOTE: The return value is a list of edited Facts that's sent to the
    #       @post_processor decorator callbacks.
    return edit_fact_by_key(ctx, controller, *args, **kwargs)


def edit_fact_by_key(
    ctx,
    controller,
    *args,
    key,
    no_editor,
    edit_text,
    edit_meta,
    # Leave 'latest_1' in kwargs.
    **kwargs
):
    def _edit_fact_by_key():
        keys = assemble_keys()
        return process_edit_command(keys)

    def assemble_keys():
        keys = []
        if key is not None:
            keys.append(key)
        # See also if user specified '-1', '-2', etc.
        for kwg_key in kwargs.keys():
            match = re.match(r'^(latest_(\d+))$', kwg_key)
            if match is not None:
                # Check whether enabled (True) or not.
                if kwargs[match.groups()[0]]:
                    to_last_index = -1 * int(match.groups()[1])
                    keys.append(to_last_index)
        # (lb): If user runs plain `dob edit` be nice and assume latest Fact.
        #  - So `dob edit` same as `dob edit -1`.
        if not keys:
            keys = [-1]
        elif len(keys) > 1:
            dob_in_user_exit(_(
                "Argument error: Please specify “-1”, or Fact ID, not both!"
            ))
        return keys

    def process_edit_command(keys):
        edited_facts = edit_fact_by_pk(
            controller,
            key=keys[0],
            use_carousel=(not no_editor),
            edit_text=edit_text,
            edit_meta=edit_meta,
        )
        return edited_facts

    return _edit_fact_by_key()


# ***
# *** [EXPORT] Command.
# ***

@cmd_bunch_group_dbms
@run.command('export', help=help_strings.EXPORT_HELP)
@show_help_finally
@flush_pager
@cmd_options_any_search_query(command='export', item='fact', match=True, group=False)
@pass_controller_context
@induct_newbies
def transcode_export(ctx, controller, *args, **kwargs):
    """Export all facts of within a given time window to a file of specified format."""
    postprocess_options_normalize_search_args(kwargs)
    kwargs['output_format'] = 'factoid'
    list_fact.list_facts(controller, *args, **kwargs)


# ***
# *** [IMPORT] Command.
# ***

@cmd_bunch_group_dbms
@run.command('import', help=help_strings.IMPORT_HELP)
@show_help_finally
@flush_pager
@click.argument('filename', nargs=1, type=click.File('r'), required=False)
@click.option('-o', '--output', type=click.File('w', lazy=True),
              help=_('If specified, write to output file rather than saving'))
@click.option('-f', '--force', is_flag=True,
              help=_('Overwrite --output file if is exists'))
@click.option('-r', '--rule', '--sep', nargs=1, default='',
              help=_('With --output, split facts with a horizontal rule'))
@click.option('--backup/--no-backup', '-B', default=True, show_default=True,
              help=_('Keep plaintext backup of edited facts until committed'))
@click.option('-b', '--leave-backup', is_flag=True,
              help=_('Leave working backup file after commit'))
@cmd_options_fact_dryable
@cmd_options_fact_import
@pass_controller_context
@induct_newbies
@post_processor
def transcode_import(
    ctx,
    controller,
    output,
    force,
    no_editor,
    filename=None,
    *args,
    **kwargs
):
    """Import from file or STDIN (pipe).

    .. NOTE: You can get tricky and enter Facts on stdin using ``-``::

               dob import -

             Click will set filename to STDIN, and Dob process each line
             as the user types it (and presses ENTER), and stops on ^D.
    """

    # If neither file nor stdin specified, dump the help.
    if filename is None and sys.stdin.isatty():
        # There are two functionally equivalent ends to showing help.
        # - We could use the help helper with a string:
        #     help_command_help(ctx, ['import'])
        # - Or we can use the context to spill its help:
        click_echo(ctx.command.get_help(ctx))
        # We could `return` or `return []` here for post_processor, or exit 0
        # because we showed help and now we're done; but you can pipe stdin to
        # `dob import` and that is a real operation, so let's return 1, indicating
        # that maybe the command *is* wrong, because no input specified.
        sys.exit(1)

    # If opposite condition, complain -- user cannot send stdin and a filename.
    if filename is not None and not sys.stdin.isatty():
        # Use case:
        #   echo "2020-01-28 15:38: hello" | dob import facts.txt
        # Or:
        #   dob import - < facts.txt
        msg = 'Hey, why are you redirecting STDIN *and* specifying a file?'
        click_echo(msg)
        sys.exit(1)

    # If output file specified, verify file absent, or --force.
    if output and not force and os.path.exists(output.name):
        msg = _('Outfile already exists at: {}'.format(output.name))
        click_echo(msg)
        sys.exit(1)

    # If filename smells False, import_facts will use sys.stdin.
    # - FIXME/2019-11-19: Test not specifying file and see how it works on
    # its own vs. piped, e.g., test `dob import` vs. `cat file | dob import`.
    # NOTE: It use_carousel is True, user is forced to save through interface,
    #       and then quit, and then saved_facts is empty; but if the carousel
    #       was not used and the facts were immediately saved, saved_facts
    #       will be those facts, which are returned from this functions for
    #       @post_processor to use to call the plugins.
    pre_post_processed_saved_facts = import_facts(
        controller,
        *args,
        file_in=filename,
        file_out=output,
        use_carousel=(not no_editor),
        **kwargs
    )
    return pre_post_processed_saved_facts


# ***
# *** [COMPLETE] Command [Bash tab completion].
# ***

# FIXME: YAS! `hidden` is from a branch at:
#          sstaszkiewicz-copperleaf:6.x-maintenance
#        Watch the PR, lest you want to remove this before publishing:
#          https://github.com/pallets/click/pull/985
#          https://github.com/pallets/click/pull/500
@run.command('complete', hidden=True, help=help_strings.COMPLETE_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@induct_newbies
def complete(ctx, controller):
    """Bash tab-completion helper."""
    controller.disable_logging()
    tab_complete(controller)


# ***
# *** [MIGRATE] Commands [database transformations].
# ***

@cmd_bunch_group_dbms
@run.group(
    'migrate',
    help=help_strings.MIGRATE_GROUP_HELP,
    # (lb): Hidden until needed. Does db really need to evolve?
    # Then again, I don't want to be rigid like JSON or Md specs.
    # I'm open to fresh ideas.
    hidden=True,
    **run_group_kwargs,
)
@show_help_finally
@show_help_if_no_command
@flush_pager
@pass_controller_context
def migrate_group(ctx, controller):
    """Base `migrate` group command run prior to any of the dob-migrate commands."""
    pass


@migrate_group.command('control', help=help_strings.MIGRATE_CONTROL_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@insist_germinated
def _migrate_control(ctx, controller):
    """Mark a database as under version control."""
    migrate_control(controller)


@migrate_group.command('down', help=help_strings.MIGRATE_DOWN_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@insist_germinated
def _migrate_downgrade(ctx, controller):
    """Downgrade the database according to its migration version."""
    migrate_downgrade(controller)


@migrate_group.command('up', help=help_strings.MIGRATE_UP_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@insist_germinated
def _migrate_upgrade(ctx, controller):
    """Upgrade the database according to its migration version."""
    migrate_upgrade(controller)


@migrate_group.command('version', help=help_strings.MIGRATE_VERSION_HELP)
@show_help_finally
@flush_pager
@pass_controller_context
@insist_germinated
def _migrate_version(ctx, controller):
    """Show migration information about the database."""
    migrate_version(controller)


# 2018-07-15 14:00ish: To loaded: 0.440 secs.
# After adding lazy-loading:
# 2018-07-15 18:06:    To loaded: 0.060 secs.
# 2018-07-15 18:06:    To run:    0.329 secs.
# About ~ 0.150 is sqlalchemy, which is unavoidable?
# About ~ 0.005 is loading config.
# The other half of the time, ~ 0.145, is plugins.
profile_elapsed('To dob: loaded')

