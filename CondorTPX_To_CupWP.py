# This Python file uses the following encoding: utf-8
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

# Purpose:  Convert Condor task 'New TP' turnpoints (copy/pasted from Condor task description
# to a text file) to CUP-formatted strings and write them to a user-selected file to be used
# in XCSoar

# CUP file format:
# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc
#"Cruseilles",Cruseill,,4601.100N,00606.400E,716.0m,1,,,,
#"Marignane",,,4325.998N,00512.846E,4m,5,317,2500,0,

#Condor Task 'New Waypoint' format:
# TP 2 (7,362 ft)
# Heading: 144° for 46.8 NM,
# Coords: 45.23.99N / 6.45.300E
# Classic turnpoint,
# min. height: 0 ft, max.: 32,808 ft
# angle: 360°, radius: 3,281 ft

#Plan:
#   Step1: Get text file containing Condor 'newTP' blocks copy/pasted from task description
#   Step2: Get 'outfile' filename to write .CUP lines to. Create if necessary. 
#           If aleady existing, ask user if we can overwrite. 'No' causes program to exit
#   Step3: Read lines until finding a line starting with 'TP' or 'Start'
#   Step4: Parse 'Coords' line to get coordinate Lat/Lon strings
#   Step5: Construct .CUP formatted line & write to outfile

#   Step1: Get text file containing Condor 'newTP' blocks copy/pasted from task description
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
root = tk.Tk() ; root.withdraw()


# PURPOSE: constructs a .CUP-formatted string from the (six?) lines waypoint
# block in the typical Condor-club task briefing.
# For example:
# ----------------------------------------------------------------------
# Start (2,434 ft)
# Heading: 115° for 3.9 NM,
# Coords: 46.31.377N / 6.42.372E
# Classic turnpoint,
# min. height: 0 ft, max.: 6,234 ft
# angle: 180°, radius: 13,123 ft
# ----------------------------------------------------------------------
# The CUP waypoint format is:
# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc
# but we are only going to fill the name, code, lat, lon and style fields
#Inputs:
#   TPName = string containing the name to be used in the .CUP string
#   x = integer denoting index into the turnpoint block string list acquired from the input file
#Outputs
#   returns a string and the INDEX TO THE NEXT LINE in the list of strings from the input file
#Plan:
#   Step1: assign 'TPname' to 'name' and 'code'
#   Step2: skip the 'Heading' line
#   Step3: extract the lat/lon strings from the 'Coords' line and convert them to .CUP format
#   Step4: extract the style string from the next line
#   Step5: concatenate the above, with appropriate ',' entries for blank entries

def ConstructCUPString(tpname, inlist, inlist_idx):
    if args.verbose:
        print(f"In ConstructCUPString(tpname = {tpname}, inlist_idx = {inlist_idx})")
        
#Step1: assign 'TPname' to 'name' and 'code'
    namestr = tpname
    codestr = tpname
    
#Step2: skip the 'Heading' line
    inlist_idx += 2
#Step3: extract the lat/lon strings from the 'Coords' line and convert them to .CUP format
    
#  From SeeYou site: Latitude is a field of length 9, where char0-1 are degrees, Char2-3 are minutes, Char4 decimal point,
# char5-7 are decimal minutes and char8 is either N or S. The ellipsoid used is WGS-1984
# Example: SeeYou 5107.830N is equal to 51° 07.830' N    print(f"inlist[{inlist_idx}] = {inlist[inlist_idx]}")
    coordstrlist = inlist[inlist_idx].split()
    
    if args.verbose:
        print(coordstrlist)
        print("Constructing Latitude...\n")
    
    #latitude deg
    latstr = coordstrlist[1]
    
    if args.verbose:
        print(f"latitude string = {latstr}")
        
    lat_deg_dot_idx = latstr.find('.')
    lat_deg_val_str = latstr[0:lat_deg_dot_idx]
    lat_deg_val = int(lat_deg_val_str)
    if args.verbose:
        print(f"latitude lat_deg str = {lat_deg_val_str}")
        print(f"latitude lat_deg = {lat_deg_val}")
    
    #if necessary, add leading zero(s) to lat_deg value
    if len(lat_deg_val_str) < 2:
        if len(lat_deg_val_str) < 1:
            lat_deg_val_str = '0'+ lat_deg_val_str
        lat_deg_val_str = '0'+ lat_deg_val_str
    if args.verbose:
        print(f"after adjustment, latitude deg str = {lat_deg_val_str}")
    
    #latitude min
    min_dot_idx = latstr.find('.',lat_deg_dot_idx +1 )
    if args.verbose:
        print(f"lat_deg_dot_idx = {lat_deg_dot_idx}, min_dot_idx = {min_dot_idx}")
        
    minplusdec_str = latstr[lat_deg_dot_idx +1:] #still has 'N/S' appended
    lat_NorS_str = minplusdec_str[len(minplusdec_str)-1]
    minplusdec_str = minplusdec_str[0:len(minplusdec_str)]
    if args.verbose:
        print(f"latitude minplusdec str = {minplusdec_str}")
        print(f"latitude NorS str = {lat_NorS_str}")
        
    lat_min_dot_idx = minplusdec_str.find('.')
    if args.verbose:
        print(f"latitude min dot idx = {lat_min_dot_idx}")
        
    lat_min_val_str = minplusdec_str[0:lat_min_dot_idx]
    if args.verbose:
        print(f"latitude min val str = {lat_min_val_str}")
        
    lat_min_dec_val_str = minplusdec_str[lat_min_dot_idx + 1: len(minplusdec_str)-1]
    if args.verbose:
        print(f"latitude min dec val str = {lat_min_dec_val_str}")
    lat_min_dec_val = int(lat_min_dec_val_str)
    lat_min_val = int(lat_min_val_str)
    
    #if necessary, add leading zero(s) to minutes value
    if len(lat_min_val_str) < 2:
        if len(lat_min_val_str):
            lat_min_val_str = '0'+ lat_min_val_str
    if args.verbose:
        print(f"after 'len < 2' adjustment, latitude min str = {lat_min_val_str}")
        
    
    #if necessary, add trailing zero(s) to minutes decimal value
    if len(lat_min_dec_val_str) < 3:
        if len(lat_min_dec_val_str) < 2:
            lat_min_dec_val_str = lat_min_dec_val_str + '0'
        lat_min_dec_val_str = lat_min_dec_val_str + '0'
    if args.verbose:
        print(f"after 'len < 2' adjustment, latitude min dec str = {lat_min_dec_val_str}")
        print(f"latitude min = {lat_min_val}")
        print(f"latitude min str = {lat_min_val_str}")
        
    #now construct SeeYou equivalent
    
    cuplatstr = lat_deg_val_str + lat_min_val_str + '.' + lat_min_dec_val_str + lat_NorS_str
    if args.verbose:
        print(f"latitude .CUP str = {cuplatstr}")
        print("\nConstructing Longitude...\n")
    
    lonstr = coordstrlist[3]
    if args.verbose:
        print(f"longitude string = {lonstr}")
 
    lon_deg_dot_idx = lonstr.find('.')
    lon_deg_val_str = lonstr[0:lon_deg_dot_idx]
    lon_deg_val = int(lon_deg_val_str)
    if args.verbose:
        print(f"longitude lon_deg str = {lon_deg_val_str}")
        print(f"longitude lon_deg = {lon_deg_val}")
    
    #if necessary, add leading zero(s) to lon_deg value
    if len(lon_deg_val_str) < 3:
        if len(lon_deg_val_str) < 2:
            lon_deg_val_str = '0'+ lon_deg_val_str
        lon_deg_val_str = '0'+ lon_deg_val_str
    if args.verbose:
        print(f"after 'len < 3' adjustment, longitude deg str = {lon_deg_val_str}")
    
    #longitude min
    min_dot_idx = lonstr.find('.',lon_deg_dot_idx +1 )
    if args.verbose:
        print(f"lon_deg_dot_idx = {lon_deg_dot_idx}, min_dot_idx = {min_dot_idx}")
    
    minplusdec_str = lonstr[lon_deg_dot_idx +1:] #still has 'E/W' appended
    lon_EorW_str = minplusdec_str[len(minplusdec_str)-1]
    minplusdec_str = minplusdec_str[0:len(minplusdec_str)]
    if args.verbose:
        print(f"longitude minplusdec str = {minplusdec_str}")
        print(f"longitude EorW str = {lon_EorW_str}")
        
    lon_min_dot_idx = minplusdec_str.find('.')
    lon_min_val_str = minplusdec_str[0:lon_min_dot_idx]
    lon_min_dec_val_str = minplusdec_str[lon_min_dot_idx + 1: len(minplusdec_str)-1]
    if args.verbose:
        print(f"longitude min dot idx = {lon_min_dot_idx}")
        print(f"longitude min val str = {lon_min_val_str}")
        print(f"longitude min dec val str = {lon_min_dec_val_str}")
    
    
    #if necessary, add leading zero(s) to minutes value
    if len(lon_min_val_str) < 2:
        if len(lon_min_val_str):
            lon_min_val_str = '0'+ lon_min_val_str
    if args.verbose:
        print(f"after 'len < 2' adjustment, longitude min str = {lon_min_val_str}")
        
    
    #if necessary, add trailing zero(s) to minutes decimal value
    if len(lon_min_dec_val_str) < 3:
        if len(lon_min_dec_val_str) < 2:
            lon_min_dec_val_str = lon_min_dec_val_str + '0'
        lon_min_dec_val_str = lon_min_dec_val_str + '0'
    if args.verbose:
       print(f"after 'len < 3' adjustment, longitude min dec str = {lon_min_dec_val_str}")
        
    #now construct SeeYou equivalent
    cuplonstr = lon_deg_val_str + lon_min_val_str + '.' + lon_min_dec_val_str + lon_EorW_str
    if args.verbose:
        print(f"longitude .CUP str = {cuplonstr}")

#Step4: extract the style string from the next line
    if args.verbose:
        print(f"\nExtracting Turnpoint Style: ")    
        
    inlist_idx += 1
    stylestrlist = inlist[inlist_idx].split()
    stylestr = stylestrlist[0]    
    if args.verbose:
        print(f"stylestr = {stylestr}\n")
    
#Step5: concatenate the above, with appropriate ',' entries for blank entries
# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc
    cupStr = namestr + ", " + codestr + ", ," + cuplatstr + ", " + cuplonstr + ", ," + stylestr + ", , , ,"
    inlist_idx += 1

    return cupStr, inlist_idx
#------------------------------------------------------------------------------------------------------    
#----------------------------------------Main Program------------------------------------------------    
#------------------------------------------------------------------------------------------------------    
infile = askopenfilename(parent=root)
    
print(f"File containing custom Condor task turnpoints = {infile}")

#   Step2: Get 'outfile' filename to write .CUP lines to. Create if necessary. 
#           If aleady existing, ask user if we can overwrite. 'No' causes program to exit
outfilename = asksaveasfilename(parent = root)

print(f"File to which XCSoar-compatible turnpoint lines will be written = {outfilename}")
ofile = open(outfilename,'w')
ofile.write(f"name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc\n")

#   Step3: Read 'infile' lines until finding a line starting with 'TP' or 'Start'
f=open(infile, encoding="utf-8")#"utf-8" encoding param needed so deg symbol displays OK
inlist = f.readlines()
f.close()


TPname = ''

#Print out entire list
if args.verbose:
    print("list contains " + str(len(inlist)) + " items")
    for x in range(len(inlist)):
        instr = inlist[x]
        print(str(x) + ": " + instr)
    
    if args.verbose:
        print("\nStart Processing Lines\n")

# for x in range(len(inlist)):
x = 0        
while x < len(inlist):
    instr = inlist[x]
    
    if args.verbose:
        print(str(x) + ": " + instr)
    
    outstr = '' #03/23/2024 needed to avoid error in verbose print block
    numstr = '' #03/23/2024 needed to avoid error in verbose print block
    if 'Start' in instr:
        TPname = 'NewStart'+ str(x)
        outstr, x = ConstructCUPString(TPname, inlist, x)
        ofile.write(outstr + "\n") #Write .CUP formatted line & write to outfile
    # if args.verbose:
        # print(f"back in main pgm: cupstr = {outstr},  x = {x}")
        
    elif 'TP' in instr:
        #TP number separated by a space
        numstr = instr[2:4]
        TPname = 'NewTP'+ numstr
        outstr, x = ConstructCUPString(TPname, inlist, x)
        ofile.write(outstr + "\n") #Write .CUP formatted line & write to outfile
        
    if args.verbose:
        print(f"numstr = {numstr}")
        print(f"back in main pgm: cupstr = {outstr},  x = {x}")
        
    x = x + 1
        
print(f"all {x} infile lines processed")
        
ofile.close()

#now print out ofile contents
# if args.verbose:
print(f"\nContents of output file {outfilename}")
outfile = open(outfilename, 'r')

for line in outfile:
    print(line)
 
