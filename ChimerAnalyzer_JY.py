'''
4 sections:  VARIABLES, GUI FUNCTIONS, BME LOGIC FUNCTIONS, MAIN (Interface 1,
Logic 1, Interface 2, Logic 2)

@author: Jonathan Young
'''


import Tkinter as tk
import tkFileDialog as tkfd
import tkFont
import tkMessageBox as tkmb
import csv
import math
import datetime
import os


# VARIABLES

# GUI Dictionary. Dictionary of file paths. Input from user.
path_dict = {}

# BME Logic Variables
# Comp results dictionaries
'''EXAMPLE.  {'red2': [230.22, 238.25, 'Not unique', 'Overlap'], 'red1':
[151.18, 159.47, 'Stutter', 'Informative', '(p159.47 * 2) / ((p159.47 * 2) +
d155.34)', "(p['red1'][159.47] * 2) / ((p['red1'][159.47] * 2) +
d['red1'][155.34])"], 'red0': '''
pre_dict = {}
don_dict = {}
# key, sizes and heights
'''Example. {'red2': {229.86: 1111, 245.97: 921}, 'red1': '''
pre_ht = {}
don_ht = {} 

# Dictionaries of only 'Informative' alleles from comp results dictionaries.
# format:  {'marker': informative allele, 'marker2': informative allele2}.
''' EXAMPLE.  {'green4': 347.27, 'blue1': 207.99}.'''
pre_info = {}
don_info = {}

# Follow-up big dictionaries w/ all data from filepath. (dictionary dictionary).
'''{1: {'Dye': '"B,1"', 'Height': '114', 'Area': '2697', 'Size': '73.64}, 2:'''
uns_dict = {}
cd3_dict = {}
bm_dict = {}
oth_dict = {}

# Lists of heights at 'Informative' alleles in followup.
''' ex. [2026.0, 2994.0, etc.]'''
uns_fuh_pre = []
uns_fuh_don = []
cd3_fuh_pre = []
cd3_fuh_don = []
bm_fuh_pre = []
bm_fuh_don = []
oth_fuh_pre = []
oth_fuh_don = []

# Values to determine if pre or donor is 'low'
low_uns = ''
low_cd3 = ''
low_bm = ''
low_oth = ''

# Dictionaries to associate pre or donor sizes with follow-up sizes.
# These will equal p and d in calculate equation.
'''EXAMPLE.  {'red2': {238.25: 0, 'SizeF0': 230.37, 230.22: 2091.0}, 'red1':
{'SizeF1': 159.54, 'SizeF0': 151.19, 151.18: 449.0, 159.47: 174.0}, 'red0':
{111.83: 121.0, 106.18: 4678.0, 'SizeF0': 106.39, 'SizeF1': 112.04}, 'green1':
{174.82: 133.0, 'SizeF0': 174.95}, 'green0': '''
uns_val_p = {}
uns_val_d = {}
cd3_val_p = {}
cd3_val_d = {}
bm_val_p = {}
bm_val_d = {}
oth_val_p = {}
oth_val_d = {}

# FINAL results dictionaries with key corresponding to decimal value of
# equation.  will also have final percent and standard deviation.
'''EXAMPLE.  {'green4': 2.023121387283237, 'red1': 4.512448132780083, 'red0':
5.042717232756824, 'green3': 2.439391657882849, 'green2': 2.2011065672359877,
'yellow3': 4.226878612716764, 'yellow1': 0.0, 'stdev': 1.6452737067123513,
'blue1': 2.550251256281407, 'mean': 2.874489355867144}'''
fin_uns = {}
fin_cd3 = {}
fin_bm = {}
fin_oth = {}

#Dominant component heights dictionaries.
'''Example.  {key: copy, dominant height} or
{key: [copy, dominant height1, dominant height2]}. copy = het or hom.'''
dominant_uns = {}
dominant_cd3 = {}
dominant_bm = {}
dominant_oth = {}

# Control list for orange 246
pre_control = []
don_control = []

# Allele ranges.  Input from user.
blue_range = {0 : [108.00, 178.50], 1 : [178.50, 250.50],
              2 : [250.50, 300.50], 3 : [300.50, 362.00]}
green_range = {0 : [94.00, 155.50], 1 : [155.50, 203.50],
               2 : [203.50, 254.50], 3: [254.50, 297.50],
               4 : [297.50, 375.00]}
yellow_range = {0 : [93.00, 144.50], 1 : [144.50, 211.50],
                2 : [211.50, 261.50], 3 : [261.50, 361.00]}
red_range = {0 : [103.50, 114.50], 1 : [114.50, 195.50],
             2 : [195.50, 287.00]}

# Loci
blue_loci = ['D8S1179', 'D21S11', 'D7S820', 'CSF1PO(5q)']
green_loci = ['D3S1358', 'THO1(11p)', 'D13S317', 'D16S539', 'D2S1338']
yellow_loci = ['D19S433', 'VWA(12p)', 'TPOX(2p)', 'D18S51']
red_loci = ['Amelogenin', 'D5S818', 'FGA(4q)']
all_loci = blue_loci + green_loci + yellow_loci + red_loci

simple_loci = ['blue0', 'blue1', 'blue2', 'blue3', 'green0', 'green1',
               'green2', 'green3', 'green4', 'yellow0', 'yellow1', 'yellow2',
               'yellow3', 'red0', 'red1', 'red2']

conv = dict(zip(simple_loci, all_loci))




#GUI FUNCTIONS
def get_path(win, name, label):
    '''Creates window to get a file path from user via 'Browse' button.  If
    user does not click 'Cancel', add file path to dictionary to allow opening
    of files outside of function.'''
    #global path_dict?
    #Answer: No, if the global value is mutable, you can modify it without
    #declaring it global (Downey, ch 11)
    path = tkfd.askopenfilename(parent=win, title="Select file for '"+name+"'",
                                filetypes=[('txt file', '.txt')],
                                initialdir='C:')
    #if user uses 'Cancel' button, tkfd.askopenfilename returns an empty string
    if path:
        path_dict[name] = path
        label.configure(fg='#%02x%02x%02x' % (0, 165, 20),
                        font=customFontSelected)
    
def enter_darker_green(event):
    '''Change the background of the calling widget when mouse pointer enters
    widget.'''
    #Event objects have a bunch of event attributes (ex. 'widget' used below).
    #For more see (Lundh, ch 7)
    #event.widget.configure(bg='#%02x%02x%02x' % (49, 223, 49))
    #event.widget.configure(bg='#%02x%02x%02x' % (0, 217, 28))
    event.widget.configure(bg='#%02x%02x%02x' % (0, 249, 60))

def leave_green(event):
    '''Change the background of the calling widget when mouse pointer leaves
    widget.'''
    event.widget.configure(bg='#%02x%02x%02x' % (102, 232, 102))

def enter_darker_gray(event):
    '''Change the background of the calling widget when mouse pointer enters
    widget.'''
    event.widget.configure(bg='gray85')

def leave_gray(event):
    '''Change the background of the calling widget when mouse pointer leaves
    widget.'''
    event.widget.configure(bg='gray93')
    
def evaluate_button(win):
    ''' When user clicks 'EVALUATE' this checks to make sure files have been
    uploaded for 'pre' and 'don'.  If not, displays an error.  If so,
    destroys window to continue with application'''
    #Error checking
    if 'pre' not in path_dict or 'don' not in path_dict:
        e19 = ('At a minimum, both a Patient ("Pre") and Donor file must be '
               'uploaded.')
        error_cont(e19)
    else:
        win.destroy()

def shutdown():
    if tkmb.askokcancel(message='Do you really want to quit?'):
        os._exit(99)

def analysis_complete():
    ''' creates a pop-up to allow root.destroy.  returns 'ok' if you click ok
    or if you x-out of the pop-up.'''
    #new 1.3 changed message :)
    if tkmb.showinfo(message='Reconstruction complete.'):
        root.destroy()

def error_shutdown(m):
    ''' pops up error message and quits app completely when 'ok' clicked'''
    if tkmb.showerror(message=m):
        os._exit(99)

def warning(m):
    tkmb.showwarning(title='Warning', message=m)

def warning2(t, m): #new 1.1
    tkmb.showwarning(title=t, message=m)

def error_cont(m):
    tkmb.showerror(title='Error', message=m)

def error_warning(m):
    # Don't use yet.  Need to quit at this point
    if tkmb.askyesno(message=m+'\n\nDo you want to proceed with zero equations '
                     'selected for one sample?'):
        return
    else:
        os._exit(99)
        
# testing, remove
def print_files(name):
    f = open(path_dict[name])
    for i in f:
        print i




# BME LOGIC FUNCTIONS
def get_alleles(temp_dict, marker_list, range_dict):
    '''From a row of dictionary values, determines which marker a significant
    peak size belongs to according to the list of markers (marker_list) and
    corresponding marker's acceptable size range (range_dict).'''
    if int(temp_dict['Height']) >= 500:  #change from 500 to 750 to 1000?
        for i, value in enumerate(marker_list):
            if temp_dict['Size']:  #new 1.1 - if leave this line out and height
                #is >500 and size is empty string '' will get error unable to
                #convert string to float.
                if ((float(range_dict[i][0])) <= (float(temp_dict['Size'])) <
                    (float(range_dict[i][1]))):
                    value.append(float(temp_dict['Size']))
                    value.append(int(temp_dict['Height']))
                    break
                    # Break out of for loop
    
def evaluate_file(file_path, output_dict, control, ht_dict):
    '''Iterates through file_path. Creates a temporary dictionary from each row
    of the tab-delimited file.  Depending on which 'Dye' is present in each
    row, get_alleles is called with the appropriate arguments. Dictionary of
    alleles is created.  A temporary dictionary (ht_dict) is created to allow
    removal of false peaks due to stutter down and pull-up.'''
    # Define markers.  Input from user.
    blue0 = []; blue1 = []; blue2 = []; blue3 = []
    blue_list = [blue0, blue1, blue2, blue3]
        
    green0 = []; green1 = []; green2 = []; green3 = []; green4 = []
    green_list = [green0, green1, green2, green3, green4]

    yellow0 = []; yellow1 = []; yellow2 = []; yellow3 = []
    yellow_list = [yellow0, yellow1, yellow2, yellow3]

    red0 = []; red1 = []; red2 = []
    red_list = [red0, red1, red2]
    
    f = open(file_path, 'r')
    for i, row in enumerate(f):
        row_list = row.strip().split('\t')
        #Error checking
        if len(row_list) < 4:
            e1 = ('ERROR:  The uploaded file does not contain enough columns. '
                  'All text files should contain the following columns:  '
                  'Dye, Size, Height, and Area.  Quitting app...')
            error_shutdown(e1)
        if len(row_list) > 5: #changed from 4 to 5?
            e2 = ('ERROR:  The uploaded file is not in the correct format.  '
                  'Quitting app...')
            error_shutdown(e2)

        # Set row from string to list, split on '\t'
        t_dict = {'Dye':row_list[0], 'Size':row_list[1], 'Height':row_list[2],
                  'Area':row_list[3]}
        # Temporary dictionary
        if i:
            # Starting with the second row
            if 'B' in t_dict['Dye']:
                get_alleles(t_dict, blue_list, blue_range)
            elif 'G' in t_dict['Dye']:
                get_alleles(t_dict, green_list, green_range)
            elif 'Y' in t_dict['Dye']:
                get_alleles(t_dict, yellow_list, yellow_range)
            elif 'R' in t_dict['Dye']:
                get_alleles(t_dict, red_list, red_range)
            elif 'O' in t_dict['Dye']:
                # Get control orange peak at 246 +/- 1.0
                if int(t_dict['Height']) >= 500 and t_dict['Size']:
                    #if size is 0.0 sometimes represented as empty string ''.
                    #maybe should add if t_dict['Size'] control for other colors
                        if (245.00 <= float(t_dict['Size']) <= 247.00):
                            control.extend(['Present', float(t_dict['Size'])])
                #TODO:  write control to file?
    f.close()
    # Zip together a dictionary
    all_values = blue_list + green_list + yellow_list + red_list
    for locus in all_values:
        #Error checking
        if not locus:
            e3 = ('ERROR:  Zero peaks identified at a locus.  The analysis '
                  'must be completed by hand.  Consider increasing injection '
                  'time.  Quitting app...')
            error_shutdown(e3)
        
            
    temp = dict(zip((simple_loci), (all_values)))
    output_dict.update(temp)

    #create dict of key : {size : height}
    for key, val in output_dict.items():
        for i, num in enumerate(val):
            if num < 500:  #will need to update this if change cutoff above
                if key not in ht_dict:
                    ht_dict[key] = {val[i] : val[(i+1)]}
                elif key in ht_dict:
                    ht_dict[key].update({val[i] : val[(i+1)]})

    # remove every other height from output_dict[key] starting with index 1. 
    for key, value in output_dict.items():
        del value[1::2]

    # CHECK FOR FALSE PEAKS IN PRE AND DONOR 
    for key, val in ht_dict.items():
        # if only 1 peak, I assume it is real...
        if len(ht_dict[key]) > 1:
            for size, height in val.items():
                for k, v in ht_dict.items():
                    if k == key:
                        for si, he in v.items():
                            #checks for stutter down peak (false peak)
                            #size +/- 0.75
                            #original was height < 1000 and he > 3500
                            if ((si-0.75) <= (size+4) <= (si+0.75)
                                and height < 1100 and he > 2900): #new 1.1

                                if size in output_dict[key]:
                                    output_dict[key].remove(size)
                                    #print si, key, size, 'stutter1'
                                
                            elif ((si-0.75) <= (size+4) <= (si+0.75)
                                  and height < 1500 and he > 6000):
                               
                                if size in output_dict[key]:
                                    output_dict[key].remove(size)
                                    #print si, key, size, 'stutter2'
                                
                    elif k != key:
                        for s, h in v.items():
                            #checks for pull-up (false peak) from a peak >6000
                            #size +/- 0.2
                            #changed to +/- 0.3 on 5/30/12. 1.1
                            #new 1.3 changed to h > 6400. 6473 is lowest peak
                            #causing p/u i've seen given pullupPeakHeights file.
                            if (s-0.3) <= size <= (s+0.3) and h > 6400:
                                peak = False
                                #print size, height, s, h
                                
                                #The code below accounts for a true peak that is
                                #close in size to any peak >6000 (the
                                #algorithm above would determine that the true
                                #peak is actully a false peak).
                                #The code below will prevent the true peak from
                                #being removed.
                                #The code looks for any peak at that locus
                                #(other than the possible false peak) that is
                                #< +/- 250 in height from the possible false
                                #peak. If there is a peak that meets this
                                #criteria, then the possible false peak is a
                                #true peak. 
                                #The code below will also accurately identify a
                                #peak as false if there are two false peaks
                                #within a marker that are > +/- 250 from each
                                #other.  But, if there are two false peaks that
                                #are not removed from output_dict, program will
                                #end with an error, greater than two values in
                                #dict.  Also,
                                #if homozygous at 8000, false pull-up and false
                                #stutter down (~1500) all at same locus, could
                                #theoretically have a false pull-up at (~1500)
                                #reported as the second allele with the homo
                                #peak (8000) as the stutter down would be
                                #removed by the above algorithm. This is why
                                #I added height >2000 below.

                                #because of this code could have a pull-up peak
                                #called true because it is within 250 height to
                                #another peak at this key. need to account for
                                #this

                                #consider changing to +/- 500 for all sizes
                                #1.3 8/29/12

                                #new 1.1: added warning messages below
                                for x, y in val.items():
                                    #add and 'red' not in key:?
                                    if x != size and height >= 2000:
                                        if size < 250:
                                            if (y-250) <= height <= (y+250):
                                                peak = True
                                                #new 1.3 for case #089
                                                for a, b in val.items():
                                                    if a != size:
                                                        if b >= 7000:
                                                            peak = False
                                                            #print a, b, size
                                                #print s, key, size, '< 250', y
                                                #new 1.3 if statement below
                                                if peak == True:
                                                    w5=("Please make sure that "
                                                        "the following comp "
                                                        "peak is based on a "
                                                        "true peak and not "
                                                        "actually a false peak "
                                                        "due to pull-up:  "
                                                        +conv[key]+"  "
                                                        +str(size)+
                                                        "\n\nContinuing app...")
                                                    warning(w5)
                                            #new 1.2: case 088, true peak +/- 
                                            #0.3 from offscale peak and +/-
                                            #449 from other allele at locus
                                            elif ((y-500) <= height <= (y+500)
                                                  and h >= 8500):
                                                #maybe add 1.3 for loop here too
                                                peak = True
                                                w8=("Please make sure that the "
                                                    "following comp peak is "
                                                    "based on a true peak and "
                                                    "not actually a false peak "
                                                    "due to pull-up:  "
                                                    +conv[key]+"  "+str(size)+
                                                    "\n\nContinuing app...")
                                                warning(w8)
                                        elif size >= 250: #height > 1500?
                                            #change to +/- 600?
                                            if (y-500) <= height <= (y+500):
                                                peak = True
                                                #print s, key, size, '< 500'
                                                w6=("Please make sure that the "
                                                    "following comp peak is "
                                                    "based on a true peak and "
                                                    "not actually a false peak "
                                                    "due to pull-up:  "
                                                    +conv[key]+"  "+str(size)+
                                                    "\n\nContinuing app...")
                                                warning(w6)
        
                                if peak == False:
                                    if size in output_dict[key]:
                                        output_dict[key].remove(size)
                                        #print s, key, size, 'pull-up'
                                               
    #Error checking
    for key, series in output_dict.items(): #new 1.1
        if len(series) > 2:
            #print series

            w7 = ("Please double check the comp alleles at the following locus "
                  "to make sure they are accurate and not based on false peaks "
                  +conv[key]+"\n\nContinuing app...")
            warning(w7)

            #remove lowest? then add warning
            temp_heights_d = {}
            for j in series:
                temp_heights_d.update({ht_dict[key][j] : j})
                #print j, key, series, ht_dict[key][j]

            #print temp_heights_d
            lowest = min(temp_heights_d.keys())
            #print lowest
            #print output_dict[key]
            output_dict[key].remove(temp_heights_d[lowest]) #new 1.1
            
            
            #print 'removed', lowest, temp_heights_d[lowest]
            #print len(series)
            #print_dict(output_dict)
            #print_dict(ht_dict)

    for series in output_dict.values():
        if len(series) > 2:
            e4 = ('ERROR (e4):  More than two peaks have been identified at a '
                  'locus.  The analysis must be completed by hand.  Consider '
                  'decreasing injection time.  Quitting app...')
            error_shutdown(e4)

    # copy homozygous alleles to list of alleles at that locus
    for value in output_dict.values():
        if len(value) == 1:
            value.append(value[0])   

def get_informative(d, od):
    '''Find all 'Informative' alleles in dictionary of alleles.  Rule out
    alleles that are not unique, numerator in a position of stutter, or
    overlapping with another peak in a different color in either dictionary'''
    #TODO:  Update for 'Offscale'
    for key, value in d.items():
        #Error checking
        if not value or not od[key]:
            e5 = ('ERROR:  Zero peaks identified at a locus.  The analysis '
                  'must be completed by hand.  Consider increasing injection '
                  'time.  Quitting app...')
            error_shutdown(e5)
        for allele in value:
            if type(allele) == type(''):
                break
            #changed from 1 to 1.15 below, new 1.1 5/30/12
            #maybe can go up to +/- 1.49
            elif (allele < (od[key][0]-1.15)) or (allele > (od[key][0]+1.15)):
                if ((allele < (od[key][1]-1.15)) or (allele > (od[key][1]+1.15))):
                    # if gets here, is a unique allele
                    if (((allele+4) < (od[key][0]-1.5)) or
                        ((allele+4) > (od[key][0]+1.5))):
                        if (((allele+4) < (od[key][1]-1.5)) or
                            ((allele+4) > (od[key][1]+1.5))):
                            #if gets here, not in stutter down position
                            #new 1.2: changed to +/- 1.5 for stutter down above
                                #8/7/12
                            for k, v in d.items():
                                #Error checking
                                if not v:
                                    e6 = ('ERROR:  Zero peaks identified at '
                                          'a locus.  The analysis must be '
                                          'completed by hand.  Consider '
                                          'increasing injection time.  '
                                          'Quitting app...')
                                    error_shutdown(e6)
                                informative_d = True
                                #maybe change overlap to +/- 0.5 (4_10_12)
                                if k != key:
                                    if ((v[0]-1) <= allele <= (v[0]+1) or
                                        (v[1]-1) <= allele <= (v[1]+1)):
                                        informative_d = False
                                        value.append('Overlap')
                                        break
                            if informative_d == True:
                                for k, v in od.items():
                                    #Error checking
                                    if not v:
                                        e7 = ('ERROR:  Zero peaks identified '
                                              'at a locus.  The analysis must '
                                              'be completed by hand.  Consider '
                                              'increasing injection time.  '
                                              'Quitting app...')
                                        error_shutdown(e7)
                                    informative_od = True
                                    #maybe change overlap to +/- 0.5 (4_10_12)
                                    if k != key:
                                        if ((v[0]-1) <= allele <= (v[0]+1) or
                                            (v[1]-1) <= allele <= (v[1]+1)):
                                            informative_od = False
                                            value.append('Overlap')
                                            break
                            if informative_d == True and informative_od == True:
                                # if gets here, no overlapping peaks = overall
                                # 'Informative' allele.
                                value.append('Informative')
                        else:
                            value.append('Stutter')     
                    else:
                        value.append('Stutter')               
                else:
                    value.append('Not unique')
            else:
                value.append('Not unique')

def get_equations(low, high, a, b):
    '''For all 'Informative' markers, appends two equations to the marker list.
    A string equation for display to the user and the same equation in
    future dictionary notation, enabling later calculations of low patient or
    low donor'''
    #TODO:  will need to update this with 'Offscale' peaks.
    #TODO:  if using 'Not Unique' values that are shared between 'low' and
    #'high', in which dictionary should you look up the corresponding height?
    #the sizes in pre vs donor will be slightly different. Current code looks up the
    #'Not Unique' allele heights using the 'high' sizes. it is possible that
    #that the two allele sizes will be different by just < 1.0, which may mean
    #you might miss one of the peaks by only searching for a size corresponding
    #to one and not both.  this may need to be accounted for later
    eq = ''
    for key, value in low.items():
        #Error checking
        if len(value) < 4 or len(high[key]) < 4:
            e8 = ("ERROR:  'Informative' alleles have not been correctly "
                  "identified.  The analysis must be completed by hand.  "
                  "Quitting app...")
            error_shutdown(e8)
        if 'Informative' in value: # and 'Offscale' not in value and 'Offscale'
            # not in high[key]:
            if value[2] == 'Informative':
                if value[0] == value[1]:
                    # homozygous and informative
                    if high[key][0] != high[key][1]:
                        # donor is heterozygous at this marker
                        x = (a, value[0], a, value[1], b, high[key][0],
                             b, high[key][1])
                        eq = '%s%0.2f / (%s%0.2f + %s%0.2f + %s%0.2f)' % x
                        value.append(eq)
                        
                        x2 = (a, str(key), value[0], a, str(key), value[1], b,
                             str(key), high[key][0], b, str(key), high[key][1])
                        eq2 = ("%s['%s'][%0.2f] / (%s['%s'][%0.2f] + "
                             "%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                        value.append(eq2)     
                    else:
                        #donor is homozygous at this marker
                        x = (a, value[0], a, value[1], b, high[key][0])
                        eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                        value.append(eq)

                        x2 = (a, str(key), value[0], a, str(key), value[1],
                              b, str(key), high[key][0])
                        eq2 = ("%s['%s'][%0.2f] / (%s['%s'][%0.2f] + "
                               "%s['%s'][%0.2f])" % x2)
                        value.append(eq2)
                elif value[3] == 'Informative':
                    # heterozygous and both informative
                    if high[key][0] != high[key][1]:
                        # donor is heterozygous at this marker
                        x = (a, value[0], a, value[1], a, value[0], a, value[1],
                             b, high[key][0], b, high[key][1])
                        eq = ('(%s%0.2f + %s%0.2f) / '
                              '(%s%0.2f + %s%0.2f + %s%0.2f + %s%0.2f)' % x)
                        value.append(eq)

                        x2 = (a, str(key), value[0], a, str(key), value[1], a,
                              str(key), value[0], a, str(key), value[1], b,
                              str(key), high[key][0], b, str(key), high[key][1])
                        eq2 = ("(%s['%s'][%0.2f] + %s['%s'][%0.2f]) / "
                              "(%s['%s'][%0.2f] + %s['%s'][%0.2f] + "
                               "%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                        value.append(eq2)
                    else:
                        # donor is homozygous at this marker
                        x = (a, value[0], a, value[1], a, value[0], a, value[1],
                             b, high[key][0])
                        eq = ('(%s%0.2f + %s%0.2f) / '
                              '(%s%0.2f + %s%0.2f + %s%0.2f)' % x)
                        value.append(eq)

                        x2 = (a, str(key), value[0], a, str(key), value[1], a,
                              str(key), value[0], a, str(key), value[1], b,
                              str(key), high[key][0])
                        eq2 = ("(%s['%s'][%0.2f] + %s['%s'][%0.2f]) / "
                              "(%s['%s'][%0.2f] + %s['%s'][%0.2f] + "
                               "%s['%s'][%0.2f])" % x2)
                        value.append(eq2)
                elif high[key][0] == high[key][1]:
                    # heterozygous w/ 1 informative and donor is homozygous
                    if (value[3] == 'Not unique' and high[key][2] ==
                        'Not unique' and high[key][3] == 'Not unique'):
                        x = (a, value[0], a, value[0], b, a, high[key][0])
                        eq = '(%s%0.2f * 2) / (%s%0.2f + %s%s%0.2f)' % x
                        value.append(eq)
                        #CHANGE: %s%s
                        x2 = (a, str(key), value[0], a, str(key), value[0], b,
                              str(key), high[key][0])
                        eq2 = ("(%s['%s'][%0.2f] * 2) / "
                               "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                        value.append(eq2)                  
                    else:
                        x = (a, value[0], a, value[0], b, high[key][0])
                        eq = '(%s%0.2f * 2) / ((%s%0.2f * 2) + %s%0.2f)' % x
                        value.append(eq)

                        x2 = (a, str(key), value[0], a, str(key), value[0], b,
                              str(key), high[key][0])
                        eq2 = ("(%s['%s'][%0.2f] * 2) / "
                               "((%s['%s'][%0.2f] * 2) + %s['%s'][%0.2f])" % x2)
                        value.append(eq2)

                # heterozygyous w/ 1 informative and donor is heterozygous
                elif high[key][2] == 'Informative':
                    x = (a, value[0], a, value[0], b, high[key][0])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[0], a, str(key), value[0], b,
                          str(key), high[key][0])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)                       
                elif high[key][3] == 'Informative':
                    x = (a, value[0], a, value[0], b, high[key][1])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[0], a, str(key), value[0], b,
                          str(key), high[key][1])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][2] == 'Stutter':
                    x = (a, value[0], a, value[0], b, high[key][0])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[0], a, str(key), value[0], b,
                          str(key), high[key][0])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][3] == 'Stutter':
                    x = (a, value[0], a, value[0], b, high[key][1])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[0], a, str(key), value[0], b,
                          str(key), high[key][1])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][2] == 'Overlap':
                    x = (a, value[0], a, value[0], b, high[key][0])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[0], a, str(key), value[0], b,
                         str(key), high[key][0])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][3] == 'Overlap':
                    x = (a, value[0], a, value[0], b, high[key][1])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[0], a, str(key), value[0], b,
                          str(key), high[key][1])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)

            elif value[3] == 'Informative':
                if high[key][0] == high[key][1]:
                    # heterozygous w/ 1 informative and donor is homozygous
                    if (value[2] == 'Not unique' and high[key][2] ==
                        'Not unique' and high[key][3] == 'Not unique'):
                        x = (a, value[1], a, value[1], b, a, high[key][0])
                        eq = '(%s%0.2f * 2) / (%s%0.2f + %s%s%0.2f)' % x
                        value.append(eq)
                        #CHANGE: %s%s
                        x2 = (a, str(key), value[1], a, str(key), value[1], b,
                              str(key), high[key][0])
                        eq2 = ("(%s['%s'][%0.2f] * 2) / "
                               "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                        value.append(eq2)         
                    else:
                        x = (a, value[1], a, value[1], b, high[key][0])
                        eq = '(%s%0.2f * 2) / ((%s%0.2f * 2) + %s%0.2f)' % x
                        value.append(eq)

                        x2 = (a, str(key), value[1], a, str(key), value[1], b,
                              str(key), high[key][0])
                        eq2 = ("(%s['%s'][%0.2f] * 2) / "
                               "((%s['%s'][%0.2f] * 2) + %s['%s'][%0.2f])" % x2)
                        value.append(eq2)
                        
                # heterozygyous w/1 informative and donor is heterozygous
                elif high[key][2] == 'Informative':
                    x = (a, value[1], a, value[1], b, high[key][0])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[1], a, str(key), value[1], b,
                          str(key), high[key][0])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)               
                elif high[key][3] == 'Informative':
                    x = (a, value[1], a, value[1], b, high[key][1])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[1], a, str(key), value[1], b,
                          str(key), high[key][1])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][2] == 'Stutter':
                    x = (a, value[1], a, value[1], b, high[key][0])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[1], a, str(key), value[1], b,
                          str(key), high[key][0])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][3] == 'Stutter':
                    x = (a, value[1], a, value[1], b, high[key][1])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[1], a, str(key), value[1], b,
                          str(key), high[key][1])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][2] == 'Overlap':
                    x = (a, value[1], a, value[1], b, high[key][0])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[1], a, str(key), value[1], b,
                          str(key), high[key][0])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)
                elif high[key][3] == 'Overlap':
                    x = (a, value[1], a, value[1], b, high[key][1])
                    eq = '%s%0.2f / (%s%0.2f + %s%0.2f)' % x
                    value.append(eq)

                    x2 = (a, str(key), value[1], a, str(key), value[1], b,
                          str(key), high[key][1])
                    eq2 = ("%s['%s'][%0.2f] / "
                           "(%s['%s'][%0.2f] + %s['%s'][%0.2f])" % x2)
                    value.append(eq2)

def create_info_dict(d, output, name):
    ''' Creates a dictionary with only the 'Informative' alleles as values and
    simple loci as keys'''
    key_list = []
    value_list = []
    for key, value in d.items():
        if 'Informative' in value:
            if value[2] == 'Informative':
                value_list.append(value[0])
                key_list.append(key)
            if value[3] == 'Informative' and value[0] != value[1]:
                value_list.append(value[1])
                key_list.append(key)
    # Zip together a dictionary
    temp = dict(zip((key_list), (value_list)))
    output.update(temp)
    #Error checking
    if not output:
        e9 = ("ERROR:  No 'Informative' alleles identified in "+name+".  "
              "Quitting app...")
        error_shutdown(e9)
        # window.destroy? - yes
       
def write_csv(d, name, key):
    ''' Writes dictionary (d) to a created csv file (w_comp).'''
    #if key not in path_dict: print error
    w_comp.writerow([name, '', '(' + path_dict[key] + ')'])
    w_comp.writerow('\n')
    for i, m in enumerate(all_loci):
        if 'b' in simple_loci[i] and i == 0 :
            row = ['Blue']
        elif 'g' in simple_loci[i] and i == 4:
            row = ['Green']
        elif 'y' in simple_loci[i] and i == 9:
            row = ['Yellow']
        elif 'r' in simple_loci[i] and i == 13:
            row = ['Red']
        else:
            row = ['']

        # if not d[simple_loci[i]]: print error    
        row = row + [m, d[simple_loci[i]][0], d[simple_loci[i]][1]]      
        if 'Informative' in d[simple_loci[i]]:
            #Error checking
            #new 1.3 (changed if/else statement and set to 'Not unique')
            if len(d[simple_loci[i]]) < 5:
                w13 = ("An equation was not properly created for "+name+" "
                       +str(conv[simple_loci[i]])+". This allele is possibly "
                       "informative, but will be treated as uninformative.")
                new_index = d[simple_loci[i]].index('Informative')
                d[simple_loci[i]][new_index] = 'Not unique'
                warning(w13)
            else:
                row.append('I')
                row.append(d[simple_loci[i]][4])
                
        w_comp.writerow(row)
    w_comp.writerow('\n')
    w_comp.writerow('\n')

def user_remove_equation(d, ck_d):
    temp = []
    for value in ck_d.values():
        temp.append(value.get())
    #Error checking
    if 1 not in temp:
        e11 = ('ERROR:  All equations for Patient(Pre) or Donor were '
               'unchecked.  Please leave at least one equation checked or '
               'complete by hand.  Quitting app...')
        error_shutdown(e11)
    for key, value in ck_d.items():
        if value.get() == 0:
            if d[key][2] == 'Informative' and d[key][3] == 'Informative':
                d[key][2] = 'Offscale'
                d[key][3] = 'Offscale'
            elif d[key][2] == 'Informative':
                d[key][2] = 'Offscale'
            elif d[key][3] == 'Informative':
                d[key][3] = 'Offscale'   
    
def create_followup_dict(filepath, output):
    ''' Create big dictionary for follow-up files'''
    fu = open(filepath, 'r')
    for i, row in enumerate(fu):
        row_list = row.strip().split('\t')
        #Error checking
        if len(row_list) < 4:
            e12 = ('ERROR:  The follow-up file does not contain enough '
                   'columns.  All text files should contain the following '
                   'columns:  Dye, Size, Height, and Area.  Quitting app...')
            error_shutdown(e12)
        if len(row_list) > 5: #changed from 4 to 5
            e13 = ('ERROR:  The uploaded file is not in the correct format.  '
                   'Quitting app...')
            error_shutdown(e13)
        # Set row from string to list, split on '\t'
        output[i] = ({'Dye':row_list[0], 'Size':row_list[1],
                      'Height':row_list[2], 'Area':row_list[3]})
    fu.close()

def fu_info_heights(i_dict, fu_dict, h_list):
    '''Finds peak heights in follow up file which correspond to informative
    allele heights (from pre and donor) +\- 1.0 and adds to a new list.  THIS
    FUNCTION IS USED TO CREATE A LIST TO BE USED TO DETERMINE LOW DONOR VS. LOW
    PATIENT, NOT TO DETERMINE THE PERCENT OF EACH ALLELE PRESENT.'''
    for ikey, ivalue in i_dict.items():
        for key, d in fu_dict.items():
            if 'B' in d['Dye'] and 'blue' in ikey:
                if (ivalue-1) <= float(d['Size']) <= (ivalue+1):
                    h_list.append(float(d['Height']))
            if 'G' in d['Dye'] and 'green' in ikey:
                if (ivalue-1) <= float(d['Size']) <= (ivalue+1):
                    h_list.append(float(d['Height']))
            if 'Y' in d['Dye'] and 'yellow' in ikey:
                if (ivalue-1) <= float(d['Size']) <= (ivalue+1):
                    h_list.append(float(d['Height']))
            if 'R' in d['Dye'] and 'red' in ikey:
                if (ivalue-1) <= float(d['Size']) <= (ivalue+1):
                    h_list.append(float(d['Height']))
    #delete: print i_dict
    
def print_dict(d):
    for key, value in d.items():
        print key, value
    print '\n'

def print_simple(d):
    for locus in simple_loci:
        print locus, d[locus]
    print '\n'

def find_closest(temp, val, SizeF, key, out, name): #new 1.1
    '''If more than one peak found +/- 1.0 from a pre or donor allele, finds the
    closest and highest peak.'''
    #Todo: do not use peaks +/- 1.0 that are due to pull-up
    
    #print_dict(pre_dict)  remove this
    #print_dict(don_dict)  remove this
    #print pre_dict[key]  remove this
    #print don_dict[key]  remove this
    
    diff = []
    heights = []            
    #Warning
    w2 = ("Two or more peaks are identified in a follow-up sample within +/- "
          "1.0 of a pre or donor allele at a single locus.  The follow-up peak "
          "size that is closest to the pre or donor allele size will be used "
          "in the calculations.  This has the potential for inaccuracy.  "
          "Please double check the follow-up heights used in the percent "
          "calculations for the following allele by hand:  "
          + conv[key] + "  " + str(val) + "  " + name + "\n\nNOTE:  This is "
          "only relevant if " +str(val)+ " is present in one of the equations "
          "used to calculate final percent.\n\nContinuing app...")
    t2 = 'Warning:  2 or more peaks in a follow-up sample at one locus!'
    #Only output warning message if locus is 'Informative'
    if 'Informative' in pre_dict[key] or 'Informative' in don_dict[key]:
        warning2(t2, w2)
    
    for siznheight in temp:
        t = abs(round((siznheight[0] - val), 2))
        diff.append(t)
        heights.append(siznheight[1])
        
    #index of the closest size
    closest = diff.index(min(diff))
    #index of the highest peak
    highest = heights.index(max(heights))

    #print diff.count(min(diff)), 'count'  remove this
    #print closest, 'closest'  remove this
    
    #if there are two peaks in follow-up that are equally close, choose
    #the peak with the highest peak.
    if diff.count(min(diff)) > 1:
        #Warning
        w3 = ("Two or more peaks are identified in a follow-up sample within "
              "+/- 1.0 of a pre or donor allele at a single locus.  The "
              "follow-up peaks are exactly the same distance from the pre or "
              "donor allele, and thus, finding the one closest allele is not "
              "possible.  Of these equidistant peaks, the follow-up peak with "
              "the highest height will be used in the calculations.  This has "
              "the potential for inaccuracy.  Please double check the results "
              "for the following allele by hand:  " + conv[key] + "  " +
              str(val) + "  " + name + "\n\nContinuing app...")
        t3 = 'Warning:  Equidistant follow-up peaks!'
        #Only output warning message if locus is 'Informative'
        if 'Informative' in pre_dict[key] or 'Informative' in don_dict[key]:
            warning2(t3, w3)
        
        min_dict = {}
        for i, d in enumerate(diff):
            if d == min(diff):
                min_dict.update({heights[i] : i})
        highest_min = min_dict[max(min_dict.keys())]

        #print min_dict  remove this
        #print highest_min, 'highest min'  remove this
            
        out[key].update({val : temp[highest_min][1]})
        out[key].update({SizeF : temp[highest_min][0]})
        #since both the min peaks are the closest, but only one index
        #can be chosen for closest. closest = highest_min prevents
        #closest != highest warning below from evaluating to true when it isnt.
        closest = highest_min
    else:
        out[key].update({val : temp[closest][1]})
        out[key].update({SizeF : temp[closest][0]})
        
    #Warning
    if closest != highest:
        w4 = ("Of the 2 or more peaks identified in a follow-up sample within "
              "+/- 1.0 of a pre or donor allele at a single locus, the "
              "follow-up peak that is the closest to the pre or donor allele "
              "is not, also, the follow-up peak that is the highest.  "
              "Generally, the true follow-up peak is expected to be the "
              "closest and the highest.  This further empasizes the need to "
              "double check the results for the following allele by hand:  " +
              conv[key]+ "  " + str(val) + "  " + name + "\n\nContinuing app...")
        t4 = 'Warning:  Closest peak not equal to highest peak!'
        #Only output warning message if locus is 'Informative'
        if 'Informative' in pre_dict[key] or 'Informative' in don_dict[key]:
            warning2(t4, w4)
            
    #remove all of these           
    #print closest
    #print temp[closest][0]
    #print highest
    #print temp[highest][1]
    #print heights
    #print diff

def create_fu_value_dict(dictionary, fu_dict, out, name):
    '''Creates a dictionary associating pre and donor allele sizes and loci
    with follow-up sizes, loci, and corresponding size heights.  The final
    percent patient or percent donor will be determined from the values in
    these dictionaries and the equations from get_equations.  'SizeF' =
    followup allele size.  The size(key) will be called in eval(equation) to
    determine the height(val) used in the equation.  If an allele is not found,
    sets that allele equal to zero.  If two alleles are found at a locus...'''
    #TODO-eh..: if no val[0] or val[1] = error. no peaks found at that locus
    #TODO: could have just created one follow up dictionary with both pre and 
    #donor peak sizes and heights in one dictionary. Would need to alter
    #equations by removing 'p' and 'd' and replacing with 'fu' or something
    for key, val in dictionary.items():
        temp0 = [] #new 1.1
        temp1 = [] #new 1.1
        for k, d in fu_dict.items():
            if 'B' in d['Dye'] and 'blue' in key:
                # if decide to make this more stringent (+/- 0.5), can change
                # overlap stringency to +/- 0.5
                if (val[0]-1) <= float(d['Size']) <= (val[0]+1):
                    #assuming here that key not in 'out'. Not safe to assume.
                    #key will be in 'out' if 2 peaks identified within +/- 1.
                    #but doesnt matter as correct peak info will be added later.
                    #if val[1] is ever < val[0], will need to update this code
                    #to handle key in out and key not in out as below for val[1]
                    #-code is now updated for this with 1.1.
                    if key not in out: #new 1.1
                        out[key] = {val[0] : float(d['Height'])}
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new

                    elif key in out: #new 1.1
                        out[key].update({val[0] : float(d['Height'])})
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new
                                        
                elif (val[1]-1) <= float(d['Size']) <= (val[1]+1):
                    if key in out:
                        out[key].update({val[1] : float(d['Height'])})
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
                    elif key not in out:
                        out[key] = {val[1] : float(d['Height'])}
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
            if 'G' in d['Dye'] and 'green' in key:
                if (val[0]-1) <= float(d['Size']) <= (val[0]+1):
                    if key not in out: #new 1.1
                        out[key] = {val[0] : float(d['Height'])}
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new

                    elif key in out: #new 1.1
                        out[key].update({val[0] : float(d['Height'])})
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new

                elif (val[1]-1) <= float(d['Size']) <= (val[1]+1):
                    if key in out:
                        out[key].update({val[1] : float(d['Height'])})
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
                    elif key not in out:
                        out[key] = {val[1] : float(d['Height'])}
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
            if 'Y' in d['Dye'] and 'yellow' in key:
                if (val[0]-1) <= float(d['Size']) <= (val[0]+1):
                    if key not in out: #new 1.1
                        out[key] = {val[0] : float(d['Height'])}
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new

                    elif key in out: #new 1.1
                        out[key].update({val[0] : float(d['Height'])})
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new
                 
                elif (val[1]-1) <= float(d['Size']) <= (val[1]+1):
                    if key in out:
                        out[key].update({val[1] : float(d['Height'])})
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
                    elif key not in out:
                        out[key] = {val[1] : float(d['Height'])}
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
            if 'R' in d['Dye'] and 'red' in key:
                if (val[0]-1) <= float(d['Size']) <= (val[0]+1):
                    if key not in out: #new 1.1
                        out[key] = {val[0] : float(d['Height'])}
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new

                    elif key in out: #new 1.1
                        out[key].update({val[0] : float(d['Height'])})
                        out[key].update({'SizeF0' : float(d['Size'])})

                        temp0.append([float(d['Size']), float(d['Height'])])#new
                 
                elif (val[1]-1) <= float(d['Size']) <= (val[1]+1):
                    if key in out:
                        out[key].update({val[1] : float(d['Height'])})
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
                    elif key not in out:
                        out[key] = {val[1] : float(d['Height'])}
                        out[key].update({'SizeF1' : float(d['Size'])})

                        temp1.append([float(d['Size']), float(d['Height'])])#new
                        
        #if alleles not found, sets to zero
        if key not in out:
            out[key] = {val[0] : 0}
            if val[0] != val[1]:
                out[key].update({val[1] : 0})
        elif val[0] not in out[key]:
            out[key].update({val[0] : 0})
        elif val[1] not in out[key]:
            out[key].update({val[1] : 0})

        #print temp0 remove this
        #print temp1 remove this
        #Warning check if 2 or more followup peaks found at a single locus.
        #new 1.1 
        if len(temp0) > 1:
            find_closest(temp0, val[0], 'SizeF0', key, out, name)
        if len(temp1) > 1:
            find_closest(temp1, val[1], 'SizeF1', key, out, name)
    #remove
    #print out, name
    
def determine_low(fuh_pre, fuh_don):
    '''Determines whether pre or donor alleles are less prevalent in the
    follow-up sample by using lists of heights from follow-up results
    corresponding to donor and pre 'Informative' alleles only. Returns str'''
    #Error checking
    if not pre_info or not don_info:
        e14 = ("ERROR:  No 'Informative' alleles identified for a sample.  "
               "Quitting app...")
        error_shutdown(e14)
    average_pre = sum(fuh_pre)/len(pre_info)
    average_don = sum(fuh_don)/len(don_info)
    
    if average_pre < 0 or average_don < 0:
        return 'ERROR: negative values'
    elif average_pre == 0 and average_don == 0:
        return ("Neither 'pre' nor 'donor' is in the follow-up.  Please make "
                "sure the correct patient's files were uploaded.  Quitting "
                "app...")
    elif average_don == 0:
        return 'don'
    elif (average_pre/average_don) < 1.0:
        return 'pre'
    elif (average_pre/average_don) > 1.0:
        return 'don'
    elif average_pre == average_don:
        return 'equal'

def calc(p, d, equation, key):
    '''Given pre and donor follow-up dictionaries (created by
    create_fu_value_dict), calculates the equation from pre_dict or don_dict.
    Returns the float result. By naming my dictionaries 'p' and 'd', i use
    them directly in my equation, which was previously set up using 'p' and
    'd'.'''
    #new version 1.3 (Error handling try/except)
    try:
        return eval(equation)
    except Exception, e:      
        e20 = ("An error occurred when calculating the equation at the "
               "following locus:  "+conv[key]+".\n\nI recommend re-running "
               "ChimerAnalyzer and unchecking this locus."
               "\n\nError Message:  "+str(e)+"\n\nQuitting app...")
        error_shutdown(e20)
    
#new 1.2
def get_dom_height(dom, equation, val, key, d):
    '''Using the equation form pre_dict or don_dict, slices string to find
    size/s of dominant component peak/s. Uses these sizes to get dominant
    component peak height from uns_val_p type dictionaries. Also uses pre_dict
    and don_dict to determine if homozygous or heterozygous.  Returns list of
    dominant heights and string indicating homozgyous or heterozygous.'''
    #print equation
    #print n
    #print d[key]

    n = equation.count(dom)
    
    if n == 1:
        #print 'n=1'
        fir = equation.find(dom)
        start = equation[fir:].rfind('[')
        stop = equation[fir:].rfind(']')
        size = equation[fir:][start+1:stop]
        dom_peak = int(val[key][float(size)])

        if d[key][0] == d[key][1]:
            copy = 'hom'
        else:
            copy = 'het'
            
        return [copy, dom_peak]
        
    elif n == 2:
        #print 'n=2'
        fir = equation.find(dom)
        sec = equation.rfind(dom)
        start = equation[fir:sec].rfind('[')
        stop = equation[fir:sec].rfind(']')
        
        start_two = equation[sec:].rfind('[')
        stop_two = equation[sec:].rfind(']')
        
        size_one = equation[fir:sec][start+1:stop]
        size_two = equation[sec:][start_two+1:stop_two]

        dom_peak_one = int(val[key][float(size_one)])
        dom_peak_two = int(val[key][float(size_two)])

        if d[key][0] == d[key][1]:
            copy = 'hom'
        else:
            copy = 'het'
            
        return [copy, dom_peak_one, dom_peak_two]
        
    else:
        w9=("There was an error finding the dominant component "
            "peak height in the follow-up for " +conv[key]+ "."
            "\n\nContinuing app...")
        warning(w9)
        return 'Error!'

def create_final_dict(fuh_p, fuh_d, val_p, val_d, fin_dict, dom_dict):
    '''determines whether pre or donor is 'low' and uses the appropriate
    equations from pre_dict or don_dict to calculate amount of 'low' present
    and adds the calculation result to a dictionary with key = locus.'''
    if (determine_low(fuh_p, fuh_d) == 'pre' or
        determine_low(fuh_p, fuh_d) == 'equal'):
        for key, value in pre_dict.items():
            if 'Informative' in value:
                #Error checking
                if not pre_dict[key][5]:
                    e15 = ("ERROR:  An equation was not properly created for "
                           +key+".  Quitting app...")
                    error_shutdown(e15)
                fin_dict[key] =(calc(val_p, val_d, pre_dict[key][5], key) * 100)
                
                #new 1.2
                dom_dict[key] = get_dom_height('d[', pre_dict[key][5], val_d,
                                               key, don_dict)
        #print_dict(val_d)
        #print dom_dict

    elif determine_low(fuh_p, fuh_d) == 'don':
        for key, value in don_dict.items():
            if 'Informative' in value:
                #Error checking
                if not don_dict[key][5]:
                    e16 = ("ERROR:  An equation was not properly created for "
                           +key+".  Quitting app...")
                    error_shutdown(e16)
                fin_dict[key] =(calc(val_p, val_d, don_dict[key][5], key) * 100)

                #new 1.2
                dom_dict[key] = get_dom_height('p', don_dict[key][5], val_p,
                                               key, pre_dict)
        #print_dict(val_p)
        #print dom_dict
                
    #Error checking
    else:
        e17 = determine_low(fuh_p, fuh_d)
        error_shutdown(e17)

def mean_and_stdev(fin_dict):
    '''Given a dictionary of values, calculates the arithmetic mean and
    standard deviation (using n-1).  Adds these values to the dictionary
    created in create_final_dict.'''
    #Error checking
    if not fin_dict:
        e18 = ("ERROR:  No 'Informative' alleles identified or equations "
               "unable to be calculated.  Quitting app...")
        error_shutdown(e18)
    # calculate mean
    total = float(0)
    temp = float(0)
    for value in fin_dict.values():
        total += value
    mean = total/float(len(fin_dict))
    
    #calculate standard deviation
    #Warning
    if len(fin_dict) == 1:
        w1 = ("Only one 'Informative' allele identified.  Standard deviation "
              "cannot be calculated.")
        warning(w1)
    else:
        for value in fin_dict.values():
            temp += ((value - mean)**2)
        variance = temp/(float(len(fin_dict) - 1))
        stdev = math.sqrt(variance)
        fin_dict['stdev'] = stdev
    
    fin_dict['mean'] = mean

def write_csv_results(d, name, fuh_p, fuh_d, key, dom_d):
    ''' Writes dictionary (d) and dominant heights dictionary(dom_d) to a
    created csv file (w_results). Also calculates number of dominant component
    peaks that are below 2000 or 4000.'''
    w_results.writerow([name, '', '(' + path_dict[key] + ')'])
    if determine_low(fuh_p, fuh_d) == 'pre':
        w_results.writerow(['low patient'])
        temp = 'Patient'
    elif determine_low(fuh_p, fuh_d) == 'don':
        w_results.writerow(['low donor'])
        temp = 'Donor'
    elif determine_low(fuh_p, fuh_d) == 'equal':
        w_results.writerow(['patient and donor are present in equal amounts'])
        temp = 'Patient'
    else:
        w_results.writerow(['"low" could not be determined!'])
        temp = '"low" could not be determined!'
    w_results.writerow('\n')

    #new 1.2 (if and else below are new. write dominant component height to
    #file if the mean is <= 10 %.
    #print d['mean']
    if d['mean'] <= float(10):
        low = 0
        total = 0
        w_results.writerow(['', 'LOCUS', 'PERCENT', '',
                            'DOMINANT COMPONENT HEIGHT/HEIGHTS'])
        for key in simple_loci:
            if key in d:
                if dom_d[key][0] == 'hom':
                    if dom_d[key][1] <= 4000:
                        row = ['', conv[key], '%0.2f' % d[key], '', 'Hom',
                           dom_d[key][1], 'LOW!']
                        w_results.writerow(row)
                        low += 1
                        total += 1
                    else:
                        row = ['', conv[key], '%0.2f' % d[key], '', 'Hom',
                               dom_d[key][1]]
                        w_results.writerow(row)
                        total += 1
                elif dom_d[key][0] == 'het':
                    if len(dom_d[key]) == 2:
                        if dom_d[key][1] <= 2000:
                            row = ['', conv[key], '%0.2f' % d[key], '', 'Het',
                                   dom_d[key][1], 'LOW!']
                            w_results.writerow(row)
                            low += 1
                            total += 1
                        else: 
                            row = ['', conv[key], '%0.2f' % d[key], '', 'Het',
                                   dom_d[key][1]]
                            w_results.writerow(row)
                            total += 1
                    elif len(dom_d[key]) == 3:
                        if dom_d[key][1] <= 2000 or dom_d[key][2] <= 2000:
                            row = ['', conv[key], '%0.2f' % d[key], '', 'Het',
                                   dom_d[key][1], dom_d[key][2], 'LOW!']
                            w_results.writerow(row)
                            low += 1
                            total += 1
                        else:
                            row = ['', conv[key], '%0.2f' % d[key], '', 'Het', 
                                   dom_d[key][1], dom_d[key][2]]
                            w_results.writerow(row)
                            total += 1
                    else:
                        w10=("An error occurred writing the dominant heights "
                             "to file. \n\nContinuing app...")
                        warning(w10)       
                else:
                    w11 = ("An error occurred writing the dominant heights to "
                           "file.\n\nContinuing app...")
                    warning(w11)

        det_low_dom_comp(low, total, name)
    
    else:
        w_results.writerow(['', 'LOCUS', 'PERCENT'])

        for key in simple_loci:
            if key in d:
                row = ['', conv[key], '%0.2f' % d[key]]
                w_results.writerow(row)
    #end of new code for 1.2
              
    w_results.writerow('\n')
    #TODO: update to not include mean in csv file if only one informative
    #allele.  similar to stdev below and in mean_and_stdev
    w_results.writerow(['', 'MEAN', '%0.2f' % d['mean'], '% ' + temp])
    if 'stdev' in d:
        w_results.writerow(['', 'StDev', '%0.2f' % d['stdev']])
    w_results.writerow('\n')
    w_results.writerow('\n')

    #remove
    #print pre_dict
    #print don_dict

#new 1.2
def det_low_dom_comp(low, total, name):
    '''determines if any dominant component peak heights are too low and prints
    out a warning message.'''
    if low > 0:
        if low == 1 and total == 1:
            w12 = ("The " +str(total)+ " informative locus identified had at "
                   "least one dominant component peak that was not greater "
                   "than 2000 (if heterozygous) or 4000 (if homozygous).  See "
                   +name+ " follow-up results.\n\nContinuing app...")
        else:
            w12 = (str(low)+ " of " +str(total)+ " informative loci had at "
                   "least one dominant component peak that was not greater "
                   "than 2000 (if heterozygous) or 4000 (if homozygous).  See "
                   +name+ " follow-up results.\n\nContinuing app...")
        warning(w12)
   
   
   
    
# MAIN

# UPLOAD FILES GRAPHICAL USER INTERFACE (Interface 1, Toplevel GUI)
# Create root=tk.Tk() and first Toplevel GUI (Browse files GUI)
root = tk.Tk()
root.withdraw()

window = tk.Toplevel()
#new version 1.3 (title)
window.title('Bone Marrow Engraftment Analysis')
window.geometry('800x575+270+70')

# Create custom fonts
customFontHeader = tkFont.Font(family='Segoe UI', size=23, weight='bold')
customFontTitle = tkFont.Font(family='Segoe UI', size=13, weight='bold')
customFontSmall = tkFont.Font(family='Segoe UI', size=8)
customFontBig = tkFont.Font(family='Segoe UI', size=12, underline=1)
customFontLabel = tkFont.Font(family='Segoe UI', size=9, weight='bold')
customFontSelected = tkFont.Font(family='Segoe UI', size=9, weight='bold')
customFontEvaluate = tkFont.Font(family='Segoe UI', size=12, weight='bold')
customFontEq = tkFont.Font(family='Segoe UI', size=10)

# Frame 1 Header and Titles
frame1 = tk.Frame(window)
frame1.pack()

#new version 1.3 (text)
frame1_header = tk.Label(frame1, text='ChimerAnalyzer', font=customFontHeader,
                         anchor=tk.N)
frame1_header.pack()

frame1_title = tk.Label(frame1, text='Please click "Browse" to select text '
                        'files to evaluate.  Once a file has been selected for '
                        'a sample, \nthe sample name will turn green.  When '
                        'finished selecting, click "EVALUATE".',
                        font=customFontTitle, height=3, anchor=tk.S)
frame1_title.pack()

frame1_small = tk.Label(frame1, text='(Files must be in tab-delimited format, '
                        'saved as a text file (.txt), and consist of 4 '
                        'columns:  Dye, Size, Height, and Area)',
                        font=customFontSmall, height=3, anchor=tk.N)
frame1_small.pack()

# Frame 2 Title
frame2 = tk.Frame(window)
frame2.pack()

frame2_title = tk.Label(frame2, text='Pre-Transplant Analysis',
                        font=customFontBig, width=35, pady=9)
frame2_title.pack()

# Frame 3, Labels, and Buttons (Pre-Transplant)
frame3 = tk.Frame(window)
frame3.pack()

label_pre = tk.Label(frame3, text='Patient ("Pre")', font=customFontLabel)
label_pre.grid(row=0, column=0, padx=4, pady=4)
label_don = tk.Label(frame3, text='Donor ("Don")', font=customFontLabel)
label_don.grid(row=1, column=0, padx=4, pady=4)

# If I tried to pass parameters without lambda,Python would call get_path and
# assign the result to the command parameter (Campbell, pg 305)
button_pre = tk.Button(frame3, text='Browse', bg='gray93',
                       command=lambda: get_path(window, 'pre', label_pre))
button_pre.bind('<Enter>', enter_darker_gray)
button_pre.bind('<Leave>', leave_gray)
button_pre.grid(row=0, column=1, padx=4, pady=4)

button_don = tk.Button(frame3, text='Browse', bg='gray93',
                       command=lambda: get_path(window, 'don', label_don))
button_don.bind('<Enter>', enter_darker_gray)
button_don.bind('<Leave>', leave_gray)
button_don.grid(row=1, column=1, padx=4, pady=4)

# Frame 4 Title
frame4 = tk.Frame(window)
frame4.pack()

frame4_title = tk.Label(frame4, text='Post-Transplant Analysis (Follow-Up)',
                        font=customFontBig, width=35, pady=9)
frame4_title.pack()

# Frame 5, Labels, and Buttons (Post-Transplant)
frame5 = tk.Frame(window)
frame5.pack()

label_uns = tk.Label(frame5, text='Peripheral Blood Unsorted ("PB-unsorted")',
                     font=customFontLabel)
label_uns.grid(row=0, column=0, padx=4, pady=4)
label_cd3 = tk.Label(frame5, text='Peripheral Blood CD3 ("PB-CD3")',
                     font=customFontLabel)
label_cd3.grid(row=1, column=0, padx=4, pady=4)
label_bm = tk.Label(frame5, text='Bone Marrow ("BM")', font=customFontLabel)
label_bm.grid(row=2, column=0, padx=4, pady=4)
label_oth = tk.Label(frame5, text='Other', font=customFontLabel)
label_oth.grid(row=3, column=0, padx=4, pady=4)


button_uns = tk.Button(frame5, text='Browse', bg='gray93',
                       command=lambda: get_path(window, 'uns', label_uns))
button_uns.bind('<Enter>', enter_darker_gray)
button_uns.bind('<Leave>', leave_gray)
button_uns.grid(row=0, column=1, padx=4, pady=4)

button_cd3 = tk.Button(frame5, text='Browse', bg='gray93',
                       command=lambda: get_path(window, 'cd3', label_cd3))
button_cd3.bind('<Enter>', enter_darker_gray)
button_cd3.bind('<Leave>', leave_gray)
button_cd3.grid(row=1, column=1, padx=4, pady=4)

button_bm = tk.Button(frame5, text='Browse', bg='gray93',
                      command=lambda: get_path(window, 'bm', label_bm))
button_bm.bind('<Enter>', enter_darker_gray)
button_bm.bind('<Leave>', leave_gray)
button_bm.grid(row=2, column=1, padx=4, pady=4)

button_oth = tk.Button(frame5, text='Browse', bg='gray93',
                       command=lambda: get_path(window, 'oth', label_oth))
button_oth.bind('<Enter>', enter_darker_gray)
button_oth.bind('<Leave>', leave_gray)
button_oth.grid(row=3, column=1, padx=4, pady=4)

# Frame 6 'EVALUATE' Button
frame6 = tk.Frame(window)
frame6.pack()

button_evaluate = tk.Button(frame6, text='EVALUATE', font=customFontEvaluate,
                            bg='#%02x%02x%02x' % (102, 232, 102),
                            command=lambda: evaluate_button(window))
button_evaluate.bind('<Enter>', enter_darker_green)
button_evaluate.bind('<Leave>', leave_green)
button_evaluate.pack(pady=30)

window.protocol('WM_DELETE_WINDOW', shutdown)
window.focus_set()
window.grab_set()
window.wait_window()
# END GUI



# LOGIC 1    
evaluate_file(path_dict['pre'], pre_dict, pre_control, pre_ht)
evaluate_file(path_dict['don'], don_dict, don_control, don_ht)

# serious error checking here for creation of dictionaries.  all equations
# dependent on location of values in dictionary.  If a marker has more 
# than 2 peaks > 500 or no peaks, equation at that locus with be erroneous.
#(remember Ming's example of MSI).  

get_informative(pre_dict, don_dict)
get_informative(don_dict, pre_dict)
               
get_equations(pre_dict, don_dict, 'p', 'd')
get_equations(don_dict, pre_dict, 'd', 'p')

create_info_dict(pre_dict, pre_info, 'PATIENT(Pre)')
create_info_dict(don_dict, don_info, 'Donor')


# Create csv file and save to it
# where would you like to save comp results
fout = None
while fout == None:
    fout = tkfd.asksaveasfile(parent=root, mode='wb',
                          title='Select Where to Save "Comp" Results',
                          defaultextension='.csv',
                          initialfile='comp_results'+str(datetime.date.today()),
                          filetypes=[('CSV file', '.csv')],
                          initialdir='C:')

w_comp = csv.writer(fout)
write_csv(pre_dict, 'PATIENT(Pre)', 'pre')
write_csv(don_dict, 'DONOR', 'don')
fout.close()

    

# UNCHECK EQUATIONS GRAPHICAL USER INTERFACE (Interface 2)
# IF FOLLOW-UP FILES WERE UPLOADED...       
if ('uns' in path_dict or 'cd3' in path_dict or 'bm' in path_dict
    or 'oth' in path_dict):
    eq_win = tk.Toplevel()
    eq_win.title('Equation Selection')
    eq_win.geometry('+285+0')

    label_title = tk.Label(eq_win, text='Please uncheck any equations that '
                           'include offscale peaks in the follow-up '
                           'electropherogram.\nWhen finished unchecking, '
                           'click "CONTINUE".', font=customFontTitle)
    label_title.pack(padx=10, pady=5)

    f_pre = tk.Frame(eq_win)
    f_pre.pack()

    f_don = tk.Frame(eq_win)
    f_don.pack()

    f_cont = tk.Frame(eq_win)
    f_cont.pack()

    label_p = tk.Label(f_pre, text='Low Patient ("Pre") Equations',
                       font=customFontLabel)
    label_p.pack(pady=8)

    var_pre = {} #move to top
    for key in simple_loci:
        var = tk.IntVar()
        if 'Informative' in pre_dict[key]:
            if 'blue' in key:
                check = tk.Checkbutton(f_pre,
                            text=conv[key]+':  '+pre_dict[key][4],
                            variable=var, selectcolor='dodgerblue2',
                            font=customFontEq)
            elif 'green' in key:
                check = tk.Checkbutton(f_pre,
                            text=conv[key]+':  '+pre_dict[key][4],
                            variable=var, selectcolor='green',
                            font=customFontEq)
            elif 'yellow' in key:
                check = tk.Checkbutton(f_pre,
                            text=conv[key]+':  '+pre_dict[key][4],
                            variable=var, selectcolor='yellow',
                            font=customFontEq)
            elif 'red' in key:
                check = tk.Checkbutton(f_pre,
                            text=conv[key]+':  '+pre_dict[key][4],
                            variable=var, selectcolor='red',
                            font=customFontEq)
            #change 'key' in text to key[:-1] to use only color in display
            check.pack(anchor=tk.W)
            check.select()
            var_pre.update({key : var})

    label_d = tk.Label(f_don, text='Low Donor', font=customFontLabel)
    label_d.pack(pady=8)

    var_don = {} #move to top
    for key in simple_loci:
        var = tk.IntVar()
        if 'Informative' in don_dict[key]:
            if 'blue' in key:
                check = tk.Checkbutton(f_don,
                            text=conv[key]+':  '+don_dict[key][4],
                            variable=var, selectcolor='dodgerblue2',
                            font=customFontEq)
            if 'green' in key:
                check = tk.Checkbutton(f_don,
                            text=conv[key]+':  '+don_dict[key][4],
                            variable=var, selectcolor='green',
                            font=customFontEq)
            if 'yellow' in key:
                check = tk.Checkbutton(f_don,
                            text=conv[key]+':  '+don_dict[key][4],
                            variable=var, selectcolor='yellow',
                            font=customFontEq)
            if 'red' in key:
                check = tk.Checkbutton(f_don,
                            text=conv[key]+':  '+don_dict[key][4],
                            variable=var, selectcolor='red',
                            font=customFontEq)
            #change 'key' in text to key[:-1] to use only color in display
            check.pack(anchor=tk.W)
            check.select()
            var_don.update({key : var})
            
    button_continue = tk.Button(f_cont, text='CONTINUE',
                                font=customFontEvaluate,
                                bg='#%02x%02x%02x' % (102, 232, 102),
                                command=eq_win.destroy)
    button_continue.bind('<Enter>', enter_darker_green)
    button_continue.bind('<Leave>', leave_green)
    button_continue.pack(pady=8)

    eq_win.protocol('WM_DELETE_WINDOW', shutdown)
    eq_win.focus_set()
    eq_win.grab_set()
    eq_win.wait_window()
    #END EQ_WIN

    # only need to remove equations if follow-up files uploaded
    user_remove_equation(pre_dict, var_pre)
    user_remove_equation(don_dict, var_don)
# END GUI 



# LOGIC 2 (FOLLOW-UP CONTINUED)

# Create follow-up dictionaries.  Get list of heights of informative alleles
# in follow-up sample.  Determine low patient or low donor.
if 'uns' in path_dict:
    create_followup_dict(path_dict['uns'], uns_dict)
    fu_info_heights(pre_info, uns_dict, uns_fuh_pre)
    fu_info_heights(don_info, uns_dict, uns_fuh_don)

    create_fu_value_dict(pre_dict, uns_dict, uns_val_p, 'PB-Unsorted')
    create_fu_value_dict(don_dict, uns_dict, uns_val_d, 'PB-Unsorted')
    create_final_dict(uns_fuh_pre, uns_fuh_don, uns_val_p, uns_val_d, fin_uns,
                      dominant_uns)
    mean_and_stdev(fin_uns)

if 'cd3' in path_dict:
    create_followup_dict(path_dict['cd3'], cd3_dict)
    fu_info_heights(pre_info, cd3_dict, cd3_fuh_pre)
    fu_info_heights(don_info, cd3_dict, cd3_fuh_don)
    
    create_fu_value_dict(pre_dict, cd3_dict, cd3_val_p, 'PB-CD3')
    create_fu_value_dict(don_dict, cd3_dict, cd3_val_d, 'PB-CD3')
    create_final_dict(cd3_fuh_pre, cd3_fuh_don, cd3_val_p, cd3_val_d, fin_cd3,
                      dominant_cd3)
    mean_and_stdev(fin_cd3)

if 'bm' in path_dict:
    create_followup_dict(path_dict['bm'], bm_dict)
    fu_info_heights(pre_info, bm_dict, bm_fuh_pre)
    fu_info_heights(don_info, bm_dict, bm_fuh_don)
    
    create_fu_value_dict(pre_dict, bm_dict, bm_val_p, 'Bone Marrow')
    create_fu_value_dict(don_dict, bm_dict, bm_val_d, 'Bone Marrow')
    create_final_dict(bm_fuh_pre, bm_fuh_don, bm_val_p, bm_val_d, fin_bm,
                      dominant_bm)
    mean_and_stdev(fin_bm)

if 'oth' in path_dict:
    create_followup_dict(path_dict['oth'], oth_dict)
    fu_info_heights(pre_info, oth_dict, oth_fuh_pre)
    fu_info_heights(don_info, oth_dict, oth_fuh_don)
    
    create_fu_value_dict(pre_dict, oth_dict, oth_val_p, 'Other')
    create_fu_value_dict(don_dict, oth_dict, oth_val_d, 'Other')
    create_final_dict(oth_fuh_pre, oth_fuh_don, oth_val_p, oth_val_d, fin_oth,
                      dominant_oth)
    mean_and_stdev(fin_oth)


# Create csv file and save to it
if ('uns' in path_dict or 'cd3' in path_dict or 'bm' in path_dict
    or 'oth' in path_dict):
    fo = None
    while fo == None:
        fo = tkfd.asksaveasfile(parent=root, mode='wb',
                        title='Select Where to Save Follow-Up Results',
                        defaultextension='.csv',
                        initialfile='fol_up_results'+str(datetime.date.today()),
                        filetypes=[('CSV file', '.csv')],
                        initialdir='C:')
    w_results = csv.writer(fo)

    if 'uns' in path_dict:
        write_csv_results(fin_uns, 'PB-UNSORTED', uns_fuh_pre, uns_fuh_don,
                          'uns', dominant_uns)
    if 'cd3' in path_dict:
        write_csv_results(fin_cd3, 'PB-CD3', cd3_fuh_pre, cd3_fuh_don, 'cd3',
                          dominant_cd3)
    if 'bm' in path_dict:
        write_csv_results(fin_bm, 'BONE MARROW', bm_fuh_pre, bm_fuh_don, 'bm',
                          dominant_bm)
    if 'oth' in path_dict:
        write_csv_results(fin_oth, 'OTHER', oth_fuh_pre, oth_fuh_don, 'oth',
                          dominant_oth)

    fo.close()

    os.startfile(fo.name)
# Opens file path with whatever application is default for on system for csv
# files (os.startfile is Windows only).
os.startfile(fout.name)


root.protocol('WM_DELETE_WINDOW', shutdown)

analysis_complete()

root.mainloop()
