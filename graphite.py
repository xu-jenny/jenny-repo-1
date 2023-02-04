# get arguments from space after gt
# checkoutBranch
# getStackLines
# logShortClassic

# importing required modules
import argparse

parser = argparse.ArgumentParser(description = "An addition program")
parser.add_argument("ls", nargs = '*', metavar = "type", type = str,
                     help = "type of list method")
 
args = parser.parse_args()
print(args)
# match args:
#     case 'list'
if len(args.ls) != 0:
    print(args.ls)