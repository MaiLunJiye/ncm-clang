from cm import getLogger
from os.path import dirname, join, isfile
from pathlib import Path
import shlex
import json

logger = getLogger(__name__)

def args_from_cmake(filepath, cwd):
    filedir = dirname(filepath)

    compile_commands = find_config([filedir, cwd], 'compile_commands.json')
    if not compile_commands:
        compile_commands = find_config([filedir, cwd], 'build/compile_commands.json')

    if not compile_commands:
        return None, None

    try:
        with open (compile_commands, "r") as f:
            txt = f.read()
            commands = json.loads(txt)
            for cmd in commands:
                if cmd['file'] == filepath:
                    logger.info("compile_commands: %s", cmd)
                    return shlex.split(cmd['command'])[1:-1], cmd['directory']
            logger.error("Failed finding args from %s for %s", compile_commands, filepath)
    except Exception as ex:
        logger.exception("read %s failed.", compile_commands)

    return None, None


def args_from_clang_complete(filepath, cwd):
    filedir = dirname(filepath)

    clang_complete = find_config([filedir, cwd], '.clang_complete')

    if not clang_complete:
        return None, None

    try:
        with open (clang_complete, "r") as f:
            clang_complete_args = shlex.split(" ".join(f.readlines()))
            logger.info('.clang_complete args: %s', clang_complete_args)
            return clang_complete_args, dirname(clang_complete)
    except Exception as ex:
        logger.exception("read config file %s failed.", clang_complete)

    return None, None


def find_config(bases, name):

    if type(bases) == type(""):
        bases = [bases]

    for base in bases:
        r = Path(base).resolve()
        dirs = [r] + list(r.parents)
        for d in dirs:
            d = str(d)
            p = join(d, name)
            if isfile(p):
                return p

    return None

