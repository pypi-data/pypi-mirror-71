"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from rse.main import Queue
import json
import os
import sys


def main(args, extra):

    # Create a queue object
    queue = Queue(config_dir=args.config_dir)
    task = queue.get(args.taskid)
    print(json.dumps(task.load(), indent=4))
