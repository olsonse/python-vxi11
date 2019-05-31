#!/usr/bin/env python3
"""
A sample program that stores traces from the scope to file in a loop.

Written by Spencer E. Olson <olsonse@umich.edu>
Copyright (C) 2008 Spencer E. Olson


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License. 

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

# make sure that you include the path to the rpc and vxi11 packages.
import sys, os
sys.path.append(os.path.pardir)
from six.moves import input

from vxi11.tools import TDS5000B

def haltif(cond, msg=None):
    if cond:
        if msg is None:
            msg = 'Press enter to continue'
        input(msg)
    return cond

def main():

    NUM_AVERAGES = 10
    NUM_DATA_POINTS = 51

    # a Windows XP path used on the scope (which runs Windows)
    FDIR = 'w:\\rubidium\\data\\2008\\Jul\\23\\test'
    channels = ['CH3'] # array of channels to save data from

    scope = TDS5000B(host='rbscope')
    scope.read_timeout = 10000 # in ms

    pre_cmds = dict()
    post_cmds = dict()
#   pre_cmds[0]  = 'CH3:SCALE .5'  # before 0th iteration, execute this
#   pre_cmds[8]  = 'CH3:SCALE .2'  # before 8th iteration, execute this
#   pre_cmds[16] = 'CH3:SCALE .1'  # before 16th iteration, execute this
#   post_cmds[16] = ('CH3:SCALE .1', 'CH4:SCALE .2')  # multiple commands tuple
#   post_cmds[16] = ['CH3:SCALE .1', 'CH4:SCALE .2']  # multiple commands list


    #* ********** BEGIN EXPERIMENT PROGRAM ********* */
    scope.getStatusByte()          # clear status byte.
    scope.send([
        'SAVE:WAVEFORM:FILEFORMAT SPREADSHEETTXT',  # set waveform save format
        'ACQUIRE:STATE STOP',                       # stop whatever
        'ACQUIRE:STOPAFTER SEQUENCE',               # set to single shot.
        'DATA:START 1',                             # start trace at beginning
        'DATA:STOP 10000000',                       # make sure that we get the entire trace.
        'FILESYSTEM:CWD \"' + FDIR + '\"'           # set working dir
    ])


    msg = ["Going to save:  "]
    for chi in channels:
        msg.append('%s  ' %chi)
    msg.append('\nto files in \'%s\'' %FDIR)
    print(''.join(msg))
    input('Press enter to continue!')

    print('Ready to accumulate', str(NUM_AVERAGES),
          'averages of', str(NUM_DATA_POINTS), 'data scans')


    if scope.printErrors('Setup Error -- CHECK AFS TOKENS'):
        return

    for n in range(0,NUM_AVERAGES):
        iter = -1
        while iter < NUM_DATA_POINTS:
            iter += 1
            # set pre acquire commands.
            if iter in pre_cmds:
                scope.send(pre_cmds[iter])

            if haltif(scope.printErrors('pre_cmd'),'Press enter to redo last!'):
                iter -= 1
                continue

            # Acquire
            scope.send('ACQUIRE:STATE RUN')
            scope.waitforACQStop()
            if haltif(scope.printErrors('ACQUIRE'),'Press enter to redo last!'):
                iter -= 1
                continue
            

            # set POST acquire commands.
            if iter in post_cmds:
                scope.send(post_cmds[iter])

            if haltif(scope.printErrors('post_cmd'),'Press enter to redo last!'):
                iter -= 1
                continue

            print('Average/Iteration # %(n)d/%(i)d' %{'n':n, 'i':iter})



            # now save all the needed waveforms
            OutDir = '%(d)s\\%(i).4d'   %{'d':FDIR, 'i':iter} 
            MkOutDir = 'FILESYSTEM:MKDIR \"%(od)s\"'    %{'od':OutDir} 
            save_cmds = []
            for chi in channels:
                save_cmds.append(
                    'SAVE:WAVEFORM %(c)s,\"%(d)s\\scope-%(c)s-%(n).4d.txt\"' \
                    %{'c':chi, 'd':OutDir, 'n':n}
                )

            if save_cmds != []:
                scope.send(MkOutDir)
                scope.clearStatusByte() # clear+ignore status byte
                scope.send(save_cmds); # save

            if haltif(scope.printErrors('SAVE:WAVEFORM -- CHECK AFS TOKENS'),
                      'Press enter to redo last!'):
                iter -= 1
                continue




if __name__ == "__main__":
    main()

