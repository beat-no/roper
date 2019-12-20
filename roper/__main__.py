from invoke import Collection, Program
import roper
namespace = Collection()
namespace.add_task(roper.tasks.find_class)
namespace.add_task(roper.tasks.move_class)
namespace.add_task(roper.tasks.rename_module)
program = Program(namespace=namespace, version=roper.__version__)
