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


@task
def rename_module(ctxt, module, to_name, do=False):
    """
    Rename module: --module <nam> --to-name <> [--do False]
    """
    module_resource = PROJECT.get_resource(module)
    changes = Rename(PROJECT, module_resource).get_changes(to_name)
    execute_changes(changes, do)


@task
def move(ctxt, name, source, target, do=False):
    """
    Move definition: --name <> --source <module> --target <module> [--do False]
    
    https://github.com/python-rope/rope/issues/231
    """
    finder = FINDER(name)
    source_resource = PROJECT.get_resource(source)
    target_resource = PROJECT.get_resource(target)
    definition_occurrence = next(
        occ for occ in finder.find_occurrences(resource=source_resource) if occ.is_defined())
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
