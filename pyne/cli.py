#!/usr/bin/env python
import os
import pkgutil
import sys

import click_completion
from click import (
    argument,
    group,
    pass_context,
    Path)

# Enable shell completion.
click_completion.init()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@argument('path', required=False, type=Path(resolve_path=True), default=".")
@pass_context
def main(context, path):
    def load_all_modules_from_dir(dirname):
        sys.path.append(dirname)
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            if "_test" == package_name[-5:] and package_name not in sys.modules:
                module = importer.find_module(package_name
                                              ).load_module(package_name)
                print(module)

    load_all_modules_from_dir(path)
    for content in os.listdir(path):
        if content[-3:] != ".py" and content[-2:] != "__" and content[0] != ".":
            load_all_modules_from_dir(path + "/" + content)


if __name__ == "__main__":
    main()
