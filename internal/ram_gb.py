#! /usr/bin/env python3

import psutil
from internal import variables_data

# Assign variable to store total memory value.
mem = psutil.virtual_memory()
mem_total = float(mem.total / variables_data.gigabyte)


# Defining function ram_specs that uses modules/functions from psutil library and from variables_data.
def ram_specs():
    return round(float(mem_total), 2)
