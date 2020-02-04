from functools import partial
from invoke import task
from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.refactor.move import create_move
from rope.refactor.occurrences import Finder
from . import lib

PROJECT = Project('.')
FINDER = partial(Finder, PROJECT)


def execute_changes(changes, do):
    print(changes.get_description())
    if do:
        PROJECT.do(changes)
        print("Change set has been applied.")
    else:
        print("Change set is shown above. Use --do to actually apply the changes.")


def find_definition_in_resource(name, resource):
    finder = FINDER(name)
    return next(occ for occ in finder.find_occurrences(resource=resource) if occ.is_defined())


@task
def rename_module(ctxt, module, to_name, do=False):
    """
    Rename module: --module <name> --to-name <> [--do False]
    """
    module_resource = PROJECT.get_resource(module)
    changes = Rename(PROJECT, module_resource).get_changes(to_name)
    execute_changes(changes, do)


@task
def rename_by_offset(ctxt, resource, offset, new, do=False):
    """
    Rename by offset: --resource <path> --offset <int> --new <name> [--do False]
    """
    resource = PROJECT.get_resource(resource)
    changes = Rename(PROJECT, resource, int(offset)).get_changes(new)
    execute_changes(changes, do)


@task
def rename_by_name(ctxt, resource, old, new, do=False):
    """
    Rename by name: --resource <path> --old <name> --new <name> [--do False]
    """
    resource = PROJECT.get_resource(resource)
    definition_occurrence = find_definition_in_resource(old, resource)
    changes = Rename(PROJECT, resource, definition_occurrence.offset).get_changes(new)
    execute_changes(changes, do)


@task
def move_module(ctxt, source, target, do=False):
    """
    Move module: --source <module> --target <module> [--do False]
    """
    source_resource = PROJECT.get_resource(source)
    target_resource = PROJECT.get_resource(target)
    mover = create_move(PROJECT, source_resource)
    changes = mover.get_changes(target_resource)
    execute_changes(changes, do)


@task
def move_by_name(ctxt, name, source, target, do=False):
    """
    Move definition: --name <> --source <module> --target <module> [--do False]
    
    https://github.com/python-rope/rope/issues/231
    """
    source_resource = PROJECT.get_resource(source)
    target_resource = PROJECT.get_resource(target)
    definition_occurrence = find_definition_in_resource(name, source_resource)
    mover = create_move(PROJECT, source_resource, definition_occurrence.offset)
    changes = mover.get_changes(target_resource)
    execute_changes(changes, do)


@task
def find(ctxt, name):
    """
    Find class, method or variable: --name <>
    """
    finder = FINDER(name)
    for source_folder in PROJECT.get_source_folders():
        print("In source folder: %s" % source_folder.name)
        for module_resource in lib.find_module_resources(source_folder):
            occurrences = finder.find_occurrences(resource=module_resource)
            lib.print_occurences(occurrences)
