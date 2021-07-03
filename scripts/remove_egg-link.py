import os
import sys

for p in sys.path:
    if os.path.exists(p):
        for f in os.listdir(p):
            if f.endswith(f'{sys.argv[1]}.egg-link'):
                os.remove(os.path.join(p, f))