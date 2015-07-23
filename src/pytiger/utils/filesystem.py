"File System Utilities"

import os
import time

def get_file_age(self, filename):
        """
        Returns age of file in seconds
        """

        mtime = os.path.getmtime(filename)
        now = time.time()
        return int(now - mtime)

def touch(self, filename, create_dirs=False):
        """
        Opens and closes filename, similarly to shell touch(1). Optionally
        creates all parent directories if necessary.
        """

        if create_dirs:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        open(filename, 'w').close()

