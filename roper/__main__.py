from invoke import Collection, Program
import roper
namespace = Collection()
namespace.add_task(roper.tasks.find)
namespace.add_task(roper.tasks.move)
namespace.add_task(roper.tasks.rename_module)
namespace.add_task(roper.tasks.rename_by_name)
namespace.add_task(roper.tasks.rename_by_offset)
program = Program(namespace=namespace, version=roper.__version__)
