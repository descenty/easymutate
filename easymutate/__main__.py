import ast
from dataclasses import dataclass
import tomllib
import os
import pkgutil
from .mutators import mutators


@dataclass
class Config:
    module_path: str
    test_command: str


@dataclass
class CommandLineArgs:
    config_path: str


def read_config(config_path: str) -> Config:
    with open(config_path, "rb") as f:
        toml_config = tomllib.load(f)["easymutate"]
        if "module_path" not in toml_config:
            raise ValueError(
                f"Module path is not specified in {config_path}, \
                    for example: 'src'"
            )
        if "test_command" not in toml_config:
            raise ValueError(
                f"Test command is not specified in {config_path}, \
                    for example: 'pytest'"
            )
        return Config(**toml_config)


def read_command_line_args() -> CommandLineArgs:
    import sys
    from os import path

    if (
        len(sys.argv) != 2
        or sys.argv[1] == "--help"
        or not path.isfile(sys.argv[1])
    ):
        print("Usage: easymutate <config_path>")
        raise SystemExit(1)

    return CommandLineArgs(sys.argv[1])


def get_modules(module_path: str):
    return [
        os.path.join(module_path + "/", x.name + ".py")
        for x in pkgutil.iter_modules([module_path])
    ]


def run_tests(test_command: str):
    os.system(test_command)


# TODO add duplicate check
def mutate_loop(modules: list, test_command: str):
    for module in modules:
        os.rename(module, module + ".bak")
        with open(module + ".bak", "r") as f:
            tree = ast.parse(f.read())
            for mutator in mutators:
                for mutated_module in mutator.generate(tree):
                    print(mutated_module.body, tree.body)
                    with open(module, "w") as f_mutated:
                        f_mutated.write(ast.unparse(mutated_module))
                    run_tests(test_command)
        os.remove(module)
        os.rename(module + ".bak", module)
        input()


def main():
    args = read_command_line_args()
    config = read_config(args.config_path)
    modules = get_modules(config.module_path)
    mutate_loop(modules, config.test_command)


if __name__ == "__main__":
    main()
