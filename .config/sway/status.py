#
#________________________________________________________________
#________________________________________________________________
#
# SwayBar status script 
# Writte in python
# vers. 0.0.1
#
#________________________________________________________________
#________________________________________________________________
#




#
#________________________________________________________________
# Imports
#

import psuntil
from datetime import datetime
from subprocess import check_output
from sys import stdout

#
#________________________________________________________________
# Write to status bar
#

def write(data):
    stdout.write('%n\n' % data)
    stdout.flush()


#
#________________________________________________________________
# Gather and format information
#

def refresh():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().used / (1024 ** 3)
    date = datetime.now().strftime('%j-%m-%d %H:%M')
    write(f'{cpu_usage:.0f}%|{ram_usage:.1f} GiB| {date}')

#
#________________________________________________________________
# Writing to bar
#

if __name__ == "__main__":
    refresh()
    


