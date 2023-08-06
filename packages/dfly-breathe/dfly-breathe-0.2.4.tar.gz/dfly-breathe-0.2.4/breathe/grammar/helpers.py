from dragonfly import ElementBase, Function, Repetition
from ..elements import BoundCompound, CommandContext, CommandsRef
from six import string_types, PY2
import sys
import importlib
import logging
import traceback

logger = logging.getLogger("breathe_master")

def construct_extras(extras=None, defaults=None, global_extras=None, top_level=False):
    """
        Takes a list of extras provided by the user, and merges it with all global
        extras to produce the {name: extra} dictionary that dragonfly expects.

        In naming conflicts global extras will always be overridden, otherwise
        the later extra will win.
    """
    full_extras = global_extras.copy() if global_extras else {}
    defaults = defaults or {}
    if not extras:
        return full_extras
    assert isinstance(extras, (list, tuple))
    assert isinstance(defaults, dict)

    for e in extras:
        assert isinstance(e, ElementBase)
        if not top_level and isinstance(e, CommandsRef):
            # Trying to add top level commands amongst normal CCR commands
            # seems like a likely mistake so it needs to fail gracefully.
            msg = "Attempting to use '%s' in commands which are not" \
                "marked as top level. Separate these commands from normal commands" \
                "and add them using 'Breathe.add_commands(..., top_level=True)'."
            logger.error(msg, e)
            continue
        if not e.has_default() and e.name in defaults:
            e._default = defaults[e.name]
        full_extras[e.name] = e
    return full_extras


def construct_commands(mapping, extras=None):
    """
        Constructs a list of BoundCompound objects from a mapping and an
        extras dict.

        Also automatically converts all callables to dragonfly Function objects,
        allowing e.g.

            mapping = {"foo [<n>]": lambda n: foo(n),}
    """
    children = []
    assert isinstance(mapping, dict)
    for spec, value in mapping.items():
        if callable(value):
            value = Function(value)
        try:
            assert isinstance(spec, string_types)
            c = BoundCompound(spec, extras=extras, value=value)
            children.append(c)
        except Exception as e:
            logger.error("Exception raised while processing '%s', command will be skipped.", spec)
            logger.exception(e)
    return children


def process_top_level_commands(command_lists, alts):
    """
        Once we have begun creating a new subgrammar, we have access to
        all of the ccr commands which will be active in this context (alts).

        We now use these to replace the CommandsRef placeholders with
        Repetition(alts) in a new extras dict, and recreate the top level
        commands using this dict.
    """
    commands = []
    for command_list in command_lists:
        new_extras = {}
        for n, e in command_list[0]._extras.items():
            if isinstance(e, CommandsRef):
                new_extras[n] = Repetition(alts, e.min, e.max, e.name, e.default)
            else:
                new_extras[n] = e
        new_command_list = [
            BoundCompound(c._spec, new_extras, value=c._value)
            for c in command_list
        ]
        commands.extend(new_command_list)
    return commands


def check_for_manuals(context, command_dictlist):
    """
        Slightly horrible recursive function which handles the adding of command contexts.

        If we haven't seen it before, we need to add the name of the context to our DictList
        so it can be accessed by the "enable" command.

        If we have seen it before, we need to ensure that there is only the one command
        context object being referenced from multiple rules, rather than one for each.

        This has to be done not only for CommandContext objects but also for ones
        embedded in the children of an e.g. LogicOrContext.
    """
    if isinstance(context, CommandContext):
        if context.name in command_dictlist:
            context = command_dictlist[context.name]
        else:
            command_dictlist[context.name] = context
    elif hasattr(context, "_children"):
        new_children = [
            check_for_manuals(c, command_dictlist) for c in context._children
        ]
        context._children = tuple(new_children)
    elif hasattr(context, "_child"):
        context._child = check_for_manuals(context._child, command_dictlist)
    return context


def load_or_reload(module_name):
    try:
        if module_name not in sys.modules:
            importlib.import_module(module_name)
        else:
            module = sys.modules[module_name]
            if PY2:
                reload(module)
            else:
                importlib.reload(module)
    except Exception as e:
        logger.error("Import of '%s' failed with", module_name)
        logger.exception(e)
