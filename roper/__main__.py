from invoke import Collection, Program
import roper
namespace = Collection()
namespace.add_task(roper.tasks.find)
namespace.add_task(roper.tasks.move)
namespace.add_task(roper.tasks.rename_module)
program = Program(namespace=namespace, version=roper.__version__)
