import argparse
import errno
import os
from datetime import date
from random import seed
from random import randint

def QSLer(qpicklist,spicklist,lpicklist):
    seed()
    qlist = []
    slist = []
    llist = []
    with open ("Source Files/Q.txt", "r") as qfile: # reads off the Q file
        for line in qfile:
            if line.startswith('###'):
                pass
            else:
                qlist.append(line.strip('\n\r'))
    with open ("Source Files/S.txt", "r") as sfile: # reads off the Q file
        for line in sfile:
            if line.startswith('###'):
                pass
            else:
                slist.append(line.strip('\n\r'))
    with open ("Source Files/L.txt", "r") as lfile: # reads off the Q file
        for line in lfile:
            if line.startswith('###'):
                pass
            else:
                llist.append(line.strip('\n\r'))
    qpicker = randint(0, len(qlist)-1)
    if qpicker == qpicklist[-1]: # this if avoids repeated Qs
        qpicker += 1
        if qpicker > len(qlist)-1:
            qpicker = 1
    spicker = randint(0, len(slist)-1)
    if spicker == spicklist[-1]: # this if avoids repeated Ss
        spicker += 1
        if spicker > len(slist)-1:
            spicker = 1
    lpicker = randint(0, len(llist)-1)
    if lpicker == lpicklist[-1]: # this if avoids repeated Ls
        lpicker += 1
        if lpicker > len(llist)-1:
            lpicker = 1
    qsloutput = (f"{qlist[qpicker]} {slist[spicker]} {llist[lpicker]}")
    outputlist = [qsloutput,qpicker,spicker,lpicker]
    return outputlist

parser = argparse.ArgumentParser(prog="QSL") # the subsequent lines contain the command line arguments
parser.add_argument("outputs", nargs = '?', help = "Number of QSLs to be output")
parser.add_argument("-v","--version", action='version',version='%(prog)s 0.1.0')
args = parser.parse_args()
filename = 'QSL'
currentdir = os.getcwd() # retrieves the current directory in which the QSL.py script is running
qpicklist = [-1]
spicklist = [-1]
lpicklist = [-1]
if str(args.outputs).isnumeric() == True:
    try:
        os.makedirs((currentdir) + '/Output/')
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    today = str(date.today())
    path = currentdir + "/Output/" + (filename)  # Creates the root of the output directory path
    increment = 0
    while os.path.exists(f"{path} {today} {str(increment)}.txt"):
        increment += 1
    path = (f"{path} {today} {str(increment)}")  # Adds today's date and an increment number to the output directory path
    f = open((path) + '.txt', "w")
    f.write(f"QSL output of {args.outputs} QSLs on {today}") # writes header
    f.write('\n\n--------\n\n')
    for x in range(int(args.outputs)): # creates entries
        outputlist = QSLer(qpicklist,spicklist,lpicklist)
        qsloutput = outputlist[0]
        qpicklist.append(outputlist[1])
        spicklist.append(outputlist[2])
        lpicklist.append(outputlist[3])
        f.write(qsloutput + '\n')
    del qpicklist[0] # these lines clean up the picklists
    del spicklist[0]
    del lpicklist[0]
    f.write('\n\n--------\n\n')
    f.write('LOG\n\n')
    for x in range (len(qpicklist)):
        if len(str(qpicklist[x])) == 1:
            f.write('0')
        f.write(str(qpicklist[x]))
        f.write(' ')
    f.write('\n')
    for x in range (len(spicklist)):
        if len(str(spicklist[x])) == 1:
            f.write('0')
        f.write(str(spicklist[x]))
        f.write(' ')
    f.write('\n')
    for x in range (len(lpicklist)):
        if len(str(lpicklist[x])) == 1:
            f.write('0')
        f.write(str(lpicklist[x]))
        f.write(' ')
    f.write('\n')
    f.close()
else:
    print ('ERROR: Must specify a number of QSLs to output. e.g. "QSL.py 32"\n')