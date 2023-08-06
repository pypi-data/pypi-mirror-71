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

"""Module to provide u18n friendly help text strings for our CLI commands."""

from gettext import gettext as _

from dob_bright.config.fileboss import default_config_path, default_config_path_abbrev
from dob_bright.config.urable import ConfigUrable
from dob_bright.termio import attr, bg, coloring, fg, highlight_value

from ..copyright import assemble_copyright

from .. import __arg0name__, __package_name__

# Note that the help formatter reformats paragraphs when the help is
# displayed, to a width determined by the terminal and max_content_width.
# So the newlines you see in the text below will be removed and each
# paragraph will be reformatted with indents and new newlines inserted.
# - Your best bet to see how the text is formatted is to run the help.

# Note also that a lot of the help text is assembled at runtime, after
# dob has started and parsed command line arguments and configuration
# settings. This is because the global coloring() switch is off until
# after arguments are parsed and the config is read, and then it might
# be turned. But the way coloring works, ANSI is stripped when strings
# are assembled, as opposed to ANSI being stripped on output (the latter
# would make it easier to turn color on or off without having to rebuild
# strings, or to worry about when strings are generated; but our code is
# built the other way, so we have to wait for the coloring() question to
# be settled before building help text. Hence all the callbacks below.
#
# E.g./tl;dr, instead of seeing help text built like this:
#
#           SOME_HELP_TEXT = _("""Helps you.""")
#
#       you'll often see a builder method used instead, such as:
#
#           def SOME_HELP_TEXT(ctx):
#               return _("""Helps {color}you{reset}.""").format(...)

# ***
# *** [COMMON] Oft-used format() args.
# ***


def common_format():
    # (lb): Eh: This is a method because ENABLE_COLORS is False on startup,
    # and fg and attr will return empty strings if called when module is
    # sourced. So wait until help strings are built and it's known if color
    # or not.
    # FIXME: (lb): Replace hardcoded styles. Assign from styles.conf. #styling
    common_format = {
        'appname': highlight_value(__package_name__),
        'rawname': __package_name__,
        'codehi': fg('turquoise_2'),
        'reset': attr('reset'),
        'bold': attr('bold'),
        'italic': attr('italic'),
        'underlined': attr('underlined'),
        'wordhi': fg('chartreuse_3a'),
        'errcol': bg('red_1') + attr('bold'),
    }
    return common_format


# ***

def _command_create_force_help(what):
    return _(
        """
        If specified, overwrite {} if is exists.
        """
    ).format(what)


# ***
# *** [BARE] Command help.
# ***

def RUN_HELP_WHATIS():
    _help = _(
        """
        {appname} is a time tracker for the command line.
        """
        .strip()
    ).format(**common_format())
    return _help


def RUN_HELP_TRYME():
    _help = _(
        """
        - Try the demo to get acquainted with dob quickly,

          {codehi}{rawname} demo{reset}
        """
        .strip()
    ).format(**common_format())
    return _help


def RUN_HELP_QUICKIE():
    _help = _(
        """
        - To start dobbin immediately, init, then edit,

          {codehi}{rawname} init{reset}

          {codehi}{rawname} edit{reset}
        """
        .strip()
    ).format(**common_format())
    return _help


def RUN_HELP_HEADER():
    _help = _(
        """
        {what_is}

        {try_me}

        {quick_start}
        """
        .strip()
    ).format(
        what_is=RUN_HELP_WHATIS(),
        try_me=RUN_HELP_TRYME(),
        quick_start=RUN_HELP_QUICKIE(),
        **common_format()
    )
    return _help


def RUN_HELP_TLDR():
    _help = _(
        """
        {what_is}

        - To read lots more help, run the help command,

         \b
         {codehi}{rawname} help{reset}

        - To learn to dob quick and easy, try the demo,

         \b
         {codehi}{rawname} demo{reset}

        \b
        {copyright}
        """
        .strip()
    ).format(
        what_is=RUN_HELP_WHATIS(),
        try_me=RUN_HELP_TRYME(),
        copyright='\b\n        '.join(assemble_copyright()),
        **common_format()
    )
    return _help


def RUN_HELP_COMPLETE():
    _help = _(
        """
        {run_help_header}

        - Use {italic}help{reset} with any command to learn more, e.g.,

          {codehi}{rawname} init --help{reset}

          {codehi}{rawname} help init{reset}

          {codehi}{rawname} edit -h{reset}

        - Put global options {italic}before{reset} the command name, e.g.,

          {codehi}{rawname} --no-color details{reset}

        - Some commands have aliases, shown in (parentheses) below, e.g.,

          {codehi}{rawname} details{reset} {italic}is the same as{reset} {codehi}{rawname} info{reset}

        - For code rights and legal info, review the {copyrt_sym} and {scroll_sym},

          {codehi}{rawname} copyright{reset}

          {codehi}{rawname} license{reset}
        """  # noqa: E501 line too long
        .strip()
    ).format(
        run_help_header=RUN_HELP_HEADER(),
        copyrt_sym=coloring() and '©' or 'copyright',
        scroll_sym=coloring() and '📜' or 'license',
        **common_format()
    )
    return _help


def RUN_HELP_OVERVIEW(ctx):
    if (
        (ctx.command.name == 'run')
        and (
            ctx.invoked_subcommand
            or ctx.help_option_spotted
        )
    ):
        return RUN_HELP_COMPLETE()
    return RUN_HELP_TLDR()


# ***
# *** [HELP] Command help.
# ***

HELP_HELP = _(
    """
    Print help for the application, or for the specified command.
    """
)


# ***
# *** [VERSION] Command help.
# ***

VERSION_HELP = _(
    """
    Print the interface and library versions.
    """
)


# ***
# *** [LICENSE] Command help.
# ***

LICENSE_HELP = _(
    """
    Print the software license.
    """
)


# ***
# *** [LICENSE] Command help.
# ***

COPYRIGHT_HELP = _(
    """
    Print the software copyright.
    """
)


ABOUT_COMMAND_HELP = _(
    """
    Alias of 'copyright' command.
    """
)


# ***
# *** [DETAILS] Command help.
# ***

DETAILS_HELP = _(
    """
    Print details about the runtime environment.
    """
)


DETAILS_TMI_HELP = _(
    """
    Show AppDirs paths, too.
    """
)

# ***
# *** [ENVIRONS] Command help.
# ***

ENVIRONS_HELP = _(
    """
    Print shell-sourceable details about the runtime environment.

    Useful for setting up shell scripting, e.g.,

       \b
       eval "$({} environs)"
       echo $DOB_CONF
    """.format(__arg0name__)
)


# ***
# *** [DEBUG] Command help.
# ***

DEBUG_HELP = _(
    """
    Hidden command to break into a REPL prompt and poke around dob internals.

    This command is mostly an example to show developers how to easily debug.

    You'll probably want to just sprinkle your own breakpoints where you
    need them, e.g.,

      import sys, pdb; pdb.set_trace()

    or, if you're breaking into code after something stole the input,
    fix it first,

      import os, pdb; os.system("stty sane"); pdb.set_trace()
    """
)


# ***
# *** [DEMO] Command help.
# ***

def DEMO_HELP(ctx):
    _help = _(
        """
        Learn {rawname} -- {italic}Run this first!{reset}
        """
        .strip()
    ).format(**common_format())
    return _help


# ***
# *** [INIT] Command help.
# ***

def INIT_HELP_OVERVIEW(ctx):
    controller = ctx.obj

    _hint_sqlite = ''
    if controller.config['db.engine'] == 'sqlite':
        _hint_sqlite = _(
            """
        And if you know SQL, you can poke around the database file easily:

         \b
         {codehi}# Assuming sqlite3 is installed:{reset}
         {codehi}sqlite3 {cfg_db_path}{reset}

        But you'll probably just want to make sure you backup that file!
            """
            .strip()
        ).format(
            cfg_db_path=controller.config['db.path'],
            **common_format()
        )

    _help = _(
        """
        Create a default configuration file, and an empty database.

        - Unless it exists, init will create a default configuration at:

         \b
         {default_config_path}

        - Unless it exists, init will create an empty database file at:

         \b
         {hlg_db_path}

        After running init, you can see the contents of the config
        file by opening it in a text editor, or, better yet, you can
        dump it and get some more help with dob:

         \b
         {codehi}{rawname} config dump{reset}

        {_hint_sqlite}
        """
        .strip()
    ).format(
        default_config_path=highlight_value(default_config_path()),
        hlg_db_path=highlight_value(controller.config['db.path']),
        _hint_sqlite=_hint_sqlite,
        **common_format()
    )
    return _help


# ***
# *** [CONFIG] Commands help.
# ***

def CONFIG_GROUP_HELP(ctx):
    _help = _(
        """
        Manage user config settings (including editor key bindings).

        Some application behavior can be changed via config values.

        Config values can be persisted across invocation in a config
        file.

        You can also specify config values at runtime on the command line,
        or using environment variables.

        {underlined}Config File Location{reset}

        By default, {rawname} looks for a configuration file at:

            {default_config_path}

        - You can specify an alternative file location
        using the {codehi}{envkey}{reset} environment value.

          E.g., you could set the environment for just the command subshell like:

          \b
          {codehi}{envkey}=path/to/{rawname}.conf {rawname} COMMAND ...{reset}

          or you could export the environment variable first and then invoke {rawname}:

          \b
          {codehi}export {envkey}=path/to/{rawname}.conf{reset}
          {codehi}{rawname} COMMAND ...{reset}

        - You can alternatively specify the configuration file location
        using the {codehi}-F/--configfile{reset} global option, e.g.,
        using shorthand:

          \b
          {codehi}{rawname} -F path/to/{rawname}.conf COMMAND ...{reset}

          or using --option=value longhand:

          \b
          {codehi}{rawname} --configfile=path/to/{rawname}.conf COMMAND ...{reset}

        {underlined}Config Value Precedence{reset}

        - If no config value is specified for a setting, {rawname}
        uses a default value.

        - If a config value is found in the config value, that value
        takes precedence over the default value.

        - If a corresponding environment variable for the config value
        is found, that value is preferred over the value from the file.

          - The environment variable for each setting is formed from
        a prefix, {codehi}DOB_CONFIG_{reset}, followed by the uppercase
        section name and the uppercase setting name.

          E.g., here's how to specify the db.engine setting using its
        environment variable:

          \b
          {codehi}DOB_CONFIG_DB_ENGINE=sqlite {rawname} stats{reset}

        - If a config value is specified via the command line, that value is
        preferred over all other values.

          - You can specify config values using the {codehi}-C/--config{reset}
        option, e.g.,

          \b
          {codehi}{rawname} -C db.engine=sqlite stats{reset}

        {underlined}Config Command Overview{reset}

          - You can edit the config file directly, or (better yet) you can
        use the {codehi}dob set{reset} command to change its values.
        E.g., to enable coloring whenever you use {rawname}, run:

          \b
          {codehi}{rawname} config set client term_color True{reset}

          or omit the section name (because {rawname} is smart) and run instead:

          \b
          {codehi}{rawname} config set term_color True{reset}

          - If you remove the config file, or if you delete values from it,
        don't worry, {rawname} will use default values instead.

          - You can recreate the config file (and overwrite the existing file)
        with defaults by:

          \b
          {codehi}{rawname} config create --force{reset}

          - The best way to learn about all configurable settings is to
        print the config table, which includes a helpful message for each
        option:

          \b
          {codehi}{rawname} config show{reset}

          - If you think your config file is missing values, you can
        update it with missing settings by running the update command:

          \b
          {codehi}{rawname} config update{reset}

            - But you should not care about the contents of the config file
        if you stick to using {codehi}{rawname} config show{reset} and
        {codehi}{rawname} config set{reset} commands.

            - Although you might care about the config file contents if you'd
        like to add comments to it, which is supported.
        """
    ).format(
        default_config_path=highlight_value(default_config_path()),
        envkey=ConfigUrable.DOB_CONFIGFILE_ENVKEY,
        **common_format()
    )
    return _help


CONFIG_CREATE_HELP = _(
    """
    Write a new configuration file populated with default values.

    You can overwrite an existing configuration file using --force.
    """
)


CONFIG_CREATE_FORCE_HELP = _command_create_force_help(_('config file'))


CONFIG_EDIT_HELP = _(
    """
    Open the config file in your preferred $EDITOR.
    """
)


CONFIG_GET_HELP = _(
    """
    Print a configuration value from the config file.
    """
)


CONFIG_SET_HELP = _(
    """
    Write a configuration value to the config file.
    """
)


CONFIG_SHOW_HELP = _(
    """
    Print all config settings, including names, values, and help.
    """
)


CONFIG_UPDATE_HELP = _(
    """
    Write missing configuration values to the config file.
    """
)


# ***
# *** [STYLES] Commands help.
# ***

def STYLES_GROUP_HELP(ctx):
    _help = _(
        """
        Manage editor styles (centering, dimensions, coloring, and more).

        The easiest way to use styles is to choose one of the built-in
        styles and set it in your config.

        {underlined}Built-in Styles{reset}

        To view the list of styles, run:

          \b
          {codehi}{rawname} styles list{reset}

        {underlined}Activate a Style{reset}

        Assign the style you'd like to enable to `editor.styling`.

        For instance, to choose the 'night' style, which looks good on
        a dark background, run:

          \b
          {codehi}{rawname} config set editor styling night{reset}

        Or, to make the 'light' style active for a light background:

          \b
          {codehi}{rawname} config set editor styling light{reset}

        {underlined}Design your own Style{reset}

        dob styles are managed using a typical config file.

        Each section in the config file is one style.

        To enable a custom style, set editor.styling to its section
        name in the config file.

        To get started, create a styles file populated using a
        built-in style as a start.

        For example, to use the 'night' style as a base, run:

          \b
          {codehi}{rawname} styles create night{reset}

        Or, to start from scratch, use the 'default' style,
        or leave the style unspecified:

          \b
          {codehi}{rawname} styles create{reset}

        {underlined}Design your own Rules{reset}

        dob style rules are also managed using a config file.

        Each section in the rules file represents a single rule.

        Each rule defines one or more metadata values to match
        against your Facts, and if a rule matches, any styles
        it declares are applied to the interactive components.

        Each rule can also have a code block executed by eval.

        To generate a rules file with one example rule added,
        run:

          \b
          {codehi}{rawname} rules create{reset}

        {underlined}Edit Styles and Rules{reset}

        You can load the style file easily into your $EDITOR
        from dob:

          \b
          {codehi}{rawname} styles edit{reset}

        As well as the rules file:

          \b
          {codehi}{rawname} rules edit{reset}

        Or you could open them yourself. Their paths are listed
        in the config, e.g.:

          \b
          $ {codehi}{rawname} config get editor styles_fpath{reset}
          /home/user/.config/dob/styling/styles.conf

          \b
          $ {codehi}{rawname} config get editor rules_fpath{reset}
          /home/user/.config/dob/styling/rules.conf

        {underlined}Writing Styles and Rules{reset}

        Use the 'show' command to view the list of styles and rule
        settings and their descriptions:

          \b
          {codehi}{rawname} styles show{reset}

          \b
          {codehi}{rawname} rules show{reset}

        In addition to the styles and rules listed, you can also
        add additional settings.

        Each user-created style setting is named with a class name of
        your choosing, or it's named to match one of the special class
        names added automatically based on each Fact's metadata.

        The value for each user-created style setting is a space-separated
        list of class name of style strings, as recognized by Python Prompt
        Toolkit and Pygments.
        """
    ).format(
        **common_format()
    )
    return _help


STYLES_CREATE_HELP = _(
    """
    Write a new styles config file populated with basic styles options.

    You can overwrite an existing styles config file using --force.
    """
)


STYLES_CREATE_FORCE_HELP = _command_create_force_help(_('styles file'))


STYLES_CONF_HELP = _(
    """
    Print the styles file, a section from it, or an internal style.

    If no name is specified, prints the styles.conf file, in one exists.
    This includes any comments, too.

    If a name is specified, the matching section from the styles.conf
    file is printed, if one is found, including comments.

    Otherwise, dob looks for an internally-defined style with the
    matching name and prints that.

    On error, prints an error message.
    """
)


STYLES_EDIT_HELP = _(
    """
    Open the styles config file in your preferred $EDITOR.
    """
)


STYLES_LIST_HELP = _(
    """
    Display a list of built-in and user-declared style names.

    You can activate a style by assigning its value to `editor.styling`.

    For example, to use the 'night' style, run:

        $ dob config set editor styling night
    """
)


STYLES_SHOW_HELP = _(
    """
    View a table of basic style config settings and their descriptions.
    """
)


# ***
# *** [RULES] Commands help.
# ***

def RULES_GROUP_HELP(ctx):
    _help = _(
        """
        Manage styles (customize matching Facts, activities, tags, etc.).

        See the styles help for detailed information:

          \b
          {codehi}{rawname} styles --help{reset}
        """
    ).format(
        **common_format()
    )
    return _help


RULES_CREATE_HELP = _(
    """
    Write a new rules file populated with an example rule.

    You can overwrite an existing style rules file using --force.
    """
)


RULES_CREATE_FORCE_HELP = _command_create_force_help(_('style rules'))


RULES_CONF_HELP = _(
    """
    Print the rules file, or a single rule if a rule name is supplied.

    If no name is specified, prints the rules.conf file, in one exists.
    This includes any comments, too.

    If a name is specified, the matching section from the rules.conf
    file is printed, if one is found, including comments.

    On error, prints an error message.
    """
)


RULES_EDIT_HELP = _(
    """
    Open the rules file in your preferred $EDITOR.
    """
)


RULES_LIST_HELP = _(
    """
    Display a list of user-defined rule names.

    Each rule is enabled by default.

    To disable a rule, edit the rules file and
    set the rule's 'enabled' setting to False.

    Use the `rules conf` command to see the rules for each
    rule listed by this command, or use `styles conf <rule>`
    or `styles show <rule> to see the ruleset for a single
    rule.
    """
)


RULES_SHOW_HELP = _(
    """
    Show rule settings in a table, including name, default value,
    and description.

    If no name is supplied, an example ruleset is displayed.

    Otherwise, the named rule is fetched from the rules file
    and displayed.
    """
)


# ***
# *** [IGNORE] Commands help.
# ***

def IGNORE_GROUP_HELP(ctx):
    _help = _(
        """
        Manages ignore lists (to exclude matching names from prompts).
        """
    ).format(
        **common_format()
    )
    return _help


IGNORE_CREATE_HELP = _(
    """
    Write a new ignore file populated with example sections.

    You can overwrite an existing ignore file using --force.
    """
)


IGNORE_CREATE_FORCE_HELP = _command_create_force_help(_('ignore file'))


IGNORE_EDIT_HELP = _(
    """
    Open the ignore file in your preferred $EDITOR.
    """
)


IGNORE_LIST_HELP = _(
    """
    Display the list of ignore file section names.
    """
)


IGNORE_SHOW_HELP = _(
    """
    Show ignore rules in a table.
    """
)


# ***
# *** [STORE] Commands help.
# ***

STORE_GROUP_HELP = _(
    """
    Manage the database: create a new one; upgrade from Hamster; and more.
    """
)


STORE_CREATE_HELP = _(
    """
    Create an empty database file.

    You can overwrite an existing database file using --force.
    """
)


STORE_CREATE_FORCE_HELP = _command_create_force_help(_('data store'))


STORE_PATH_HELP = _(
    """
    Print the database path.
    """
)


STORE_URL_HELP = _(
    """
    Print the database URL.
    """
)


STORE_UPGRADE_LEGACY_HELP = _(
    """
    Migrate a legacy “Hamster” database to dob.
    """
)


STORE_UPGRADE_FORCE_HELP = _(
    """
    If specified, overwrite data store if is exists.
    """
)


# ***
# *** [STATS] Commands help.
# ***

# Print stats about your data (number of Facts, tags, etc.).
STATS_HELP = _(
    """
    Print stats about your data (Fact count, tag count, etc.).
    """
)


# ***
# *** [LIST] Commands help.
# ***

QUERY_GROUP_HELP = _(
    """
    Print activity, category, or tag {item_part}.
    """
)


QUERY_ITEM_HELP = _(
    """
    Print {item_type} {item_part}, optionally filtered and sorted.

    Finds all {item_types} by default, but results can be filtered by
    Fact start and end times and name matches.

    Results are sorted by name by default, but can be sorted
    by usage count, cumulative duration, or first Fact start
    time.

    Results are displayed in an ASCII table format by default,
    available in many different styles, or can be converted to
    comma-separated text (CSV), JSON, and other formats.

    SEARCH_TERM: Use to match specific {item_type} name(s), ORed together.
    """
)


LIST_GROUP_HELP = QUERY_GROUP_HELP.format(item_part=_('names'))


LIST_ACTIVITIES_HELP = QUERY_ITEM_HELP.format(
    item_type=_("activity"),
    item_types=_("activities"),
    item_part=_('names'),
)


LIST_CATEGORIES_HELP = QUERY_ITEM_HELP.format(
    item_type=_("category"),
    item_types=_("categories"),
    item_part=_('names'),
)


LIST_TAGS_HELP = QUERY_ITEM_HELP.format(
    item_type=_("tag"),
    item_types=_("tags"),
    item_part=_('names'),
)


# (lb): The `list facts` command is hidden, but supported for parity.
LIST_FACTS_HELP = QUERY_ITEM_HELP.format(
    item_type=_("fact"),
    item_types=_("facts"),
    item_part=_('names'),
)


# ***
# *** [FIND/SEARCH/JOURNAL/EXPORT] Commands help.
# ***

QUERY_HELP = _(
    """
Add a SEARCH_TERM to find any Facts with a description that contains
the specified search term. Or specify multiple terms to find any Fact
that contains one or more terms.

Use --broad to also loosely match the SEARCH_TERM against the activity,
category, and tag values.

Use --since and --until options to restrict the search to a specific
time range.

Use the --activity, --category, and --tags options to restrict the search
to exact activity, category, and/or tag names.

Use --order and --direction to specify how the results are sorted.

Use --limit and --offset to fetch a portion of the results.
    """
)


RESULTS_PROCESSING_HELP = _(
    """
Prints to stdout, or use --output to send to a file.

{query_help}

Combine --group-activity and --group-category to group by Activity@Category
names, or use them separately. You can also --group-tags. Or --group-days
to group by whole days. Use any combination of groupings to change the
results.

Use one or more --column options to choose which details are output,
and in what order.

To choose a different output format, use --format <format>, or one of
the format aliases (--journal, --json, etc.).

Some formats and output columns have their options, too, listed last
in the help.
    """
).format(query_help=QUERY_HELP)


SEARCH_HELP = _(
    """
Show all Facts, or those matching a search criteria.

{results_processing_help}
    """
).format(results_processing_help=RESULTS_PROCESSING_HELP)


def REPORT_HELP(ctx):
    _help = _(
        """
Generate a report on recent time usage.

This command is essentially an alias to:

  \b
  {codehi}{rawname} find --journal --since 'last week' \\{reset}
  {codehi}   --group-activity --group-category --group-days \\{reset}
  {codehi}   --sort usage --dir desc \\{reset}
  {codehi}   -l start_date -l duration -l sparkline -l actegory -l tags_freq{reset}

{results_processing_help}
        """
    ).format(results_processing_help=RESULTS_PROCESSING_HELP, **common_format())
    return _help


# ***
# *** [USAGE] Commands help.
# ***

USAGE_GROUP_HELP = QUERY_GROUP_HELP.format(item_part=_('usage'))


USAGE_ACTIVITIES_HELP = QUERY_ITEM_HELP.format(
    item_type=_("activity"),
    item_types=_("activities"),
    item_part=_('usage'),
)


USAGE_CATEGORIES_HELP = QUERY_ITEM_HELP.format(
    item_type=_("category"),
    item_types=_("categories"),
    item_part=_('usage'),
)


USAGE_TAGS_HELP = QUERY_ITEM_HELP.format(
    item_type=_("tag"),
    item_types=_("tags"),
    item_part=_('usage'),
)


# (lb): The `usage facts` command is hidden, but supported for parity.
USAGE_FACTS_HELP = QUERY_ITEM_HELP.format(
    item_type=_("fact"),
    item_types=_("facts"),
    item_part=_('usage'),
)


# ***
# *** [CURRENT-FACT] Commands help.
# ***

STOP_HELP = _(
    # Not DRY: Copied from first line of ADD_FACT_THEN.
    """
    Stop active Fact, ending it now or at the time specified.
    """
)


CANCEL_HELP = _(
    """
    Discard the active Fact.
    """
)


CURRENT_HELP = _(
    """
    Print the active Fact, if there is one.
    """
)


def NO_ACTIVE_FACT_HELP(ctx):
    _help = _(
        """
        No active Fact. Try {italic}starting{reset} a new Fact first.
        """
        .strip()
    ).format(**common_format())
    return _help


LATEST_HELP = _(
    """
    Print the latest completed Fact (with the most recent end time).
    """
)


HELP_CMD_SHOW = _(
    """
    Print the active Fact, if any, otherwise the latest Fact.
    """
)


# ***
# *** [ADD-FACT] Commands help.
# ***

def ADD_FACT_REFERRAL():
    _help = _(
        """
        For more help on this and the other add Fact commands, try

          {codehi}{rawname} --pager help add{reset}
        """
        .strip()
    ).format(**common_format())
    return _help


# verify_none
ADD_FACT_ON = _(
    """
    Alias for 'now' command, e.g., `dob on act@gory #tag: Blah...`.
    """
)


# verify_none
ADD_FACT_NOW = _(
    # FIXME/2019-11-22: (lb): I think "if nothing active" might be wrong.
    """
    Start a new Fact only if no Fact is active, using time now.
    """
)


# verify_none
ADD_FACT_START = _(
    # Not DRY: Copied from first line of ADD_FACT_AT.
    """
    Start a new Fact, beginning now or at the time specified.
    """
)


# verify_start
def ADD_FACT_AT(ctx):
    _help = _(
        """
        \b
        Start a new Fact, beginning now or at the time specified.

        \b
        This might stop the active Fact, if one exists, and the time
        specified comes after the active Fact start time.

        \b
        Or this might change the start and/or stop time of other Facts
        if the Fact being added overlaps other Facts' time windows.

        {}
        """
    ).format(ADD_FACT_REFERRAL())
    return _help


# verify_then
def ADD_FACT_THEN(ctx):
    # FIXME/2019-11-22: Verify the 'just use a colon' text, I think that works.
    _help = _(
        """
        Stop the active Fact, and start a new one, at given time or now.

        This is basically a shortcut for the at command, which requires a time
        offset, e.g.,

          {rawname} then Grinding beans for coffee.

        is the same as:

          {rawname} at +0: Grinding beans...

        If you want to specify an offset, you can, just use a colon,
        which could work well to throw down a gap Fact, e.g.,

          {rawname} then -5m: Woke up.
          {rawname} now Grinding beans...
        """
        .strip()
    ).format(**common_format())
    return _help


# verify_still
ADD_FACT_STILL = _(
    """
    Stop the active Fact, and start a new one, copying metadata.

    The new Fact is started with the same activity, category, and tags
    as the Fact that is ended.
    """
)


# Note that dob.transcode mentions a `since:` that's like `after:/next:` (verify_after).
# verify_after
def ADD_FACT_AFTER(ctx):
    _help = _(
        """
        Start a new Fact, beginning when the last Fact ended.

        {}
        """
        .strip()
    ).format(ADD_FACT_REFERRAL())
    return _help


# verify_after
ADD_FACT_NEXT = _(
    """
    Alias for the 'after' command, e.g., `dob next: Foo bar...`.
    """
)


# verify_end
ADD_FACT_TO = _(
    """
    Stop the active Fact, ending it now, or at the time specified.
    """
)


# verify_end
def ADD_FACT_UNTIL(ctx):
    _help = _(
        """
        Alias for the 'to' command, e.g., `{rawname} until -10m: Yada...`.
        """
        .strip()
    ).format(**common_format())
    return _help


# verify_both
def ADD_FACT_FROM(ctx):
    _help = _(
        """
        Insert a new Fact using the start and end time indicated.

        E.g., {rawname} from 2019-01-01 00:00 to 2019-01-01 01:00: Happy New Year!
        """
        .strip()
    ).format(**common_format())
    return _help


# ***
# *** [EDIT] Command help.
# ***

# (lb): 2019-11-22: I had been using the term "Carousel" in docs, but I
# think I should call it an "editor", and sometimes an "interactive" one.
EDIT_FACT_HELP = _(
    """
    Run the interactive editor in your terminal, to add and edit Facts.
    """
)


# ***
# *** [EXPORT] Command help.
# ***

def EXPORT_HELP(ctx):
    _help = _(
        """
Export Facts to a file, for backing up to text, or grepping.

{query_help}

See also {codehi}{rawname} report{reset} for more robust searching
and reporting options. The export command saves Facts to a file and
is useful for backing up your data as a text file, or for making a
searchable text file that you can wire into your existing notes
management system.
        """
    ).format(query_help=QUERY_HELP, **common_format())
    return _help


# ***
# *** [IMPORT] Command help.
# ***

# FIXME/2018-05-12: (lb): Document hamster-import more fully.
# - This command is quite powerful, and it might be a good way
# to demonstrate how all the dob-on/dob-after/etc. commands work.
IMPORT_HELP = _(
    """
Import Facts from a file, or from stdin, using a natural syntax.

Useful if you cannot use dob for a while, but you can maintain a
text file. Or if you need to massage data from another source into
dob.

HINT: To read from stdin, you can pipe to dob:

        echo "2020-01-09 00:00: Hi!" | dob import

      You can use shell redirection:

        dob import < path/to/my.facts

      Or you can use a single dash as the filename:

        dob import -

      For the last option, dob processes input as you type it,
      until you press ^D.
    """
)


# ***
# *** [COMPLETE] Command help.
# ***

COMPLETE_HELP = _(
    """
    Bash tab-completion helper.
    """
)


# ***
# *** [MIGRATE] Commands help.
# ***

MIGRATE_GROUP_HELP = _(
    """
    Upgrade the database, if necessary.
    """
)


MIGRATE_CONTROL_HELP = _(
    """
    Mark a database as under version control.
    """
)


MIGRATE_DOWN_HELP = _(
    """
    Downgrade the database version by 1 script.
    """
)


MIGRATE_UP_HELP = _(
    """
    Upgrade the database version by 1 script.
    """
)


MIGRATE_VERSION_HELP = _(
    """
    Show the database migration version.
    """
)


# ***
# *** [--GLOBAL-OPTIONS] Global Options help. [run_cli.py]
# ***

GLOBAL_OPT_VERBOSE = _(
    """
    Be chatty (use -VV for more).
    """
)


GLOBAL_OPT_VERBOSER = _(
    """
    Be chattier.
    """
)


GLOBAL_OPT_COLOR_NO_COLOR = _(
    """
    Color, or plain (Default: Auto).
    """
)


GLOBAL_OPT_PAGER_NO_PAGER = _(
    """
    Send output to pager, or not (Default: No).
    """
)


GLOBAL_OPT_CONFIG = _(
    """
    Override config setting(s) (multiple allowed).
    """
)


# MAYBE: (lb): Profiling: I tested this as a function, to avoid re.sub()
# always being called (on every invocation, in default_config_path_abbrev),
# but the option help is always built, so cannot escape. I wouldn't expect
# this to really have a performance impact, though.
GLOBAL_OPT_CONFIGFILE = _(
    """
    Specify config path (Default: {default_config_path_abbrev}).
    """
    .strip()
).format(
    default_config_path_abbrev=highlight_value(default_config_path_abbrev()),
)

