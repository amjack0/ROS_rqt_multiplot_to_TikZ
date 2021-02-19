#To run:
# python rqtcsv_tikz.py [your csv file]
#
import sys
import os.path
import pandas as pd
import numpy

if len(sys.argv) == 1:
    print("No argument. Only name of .csv file required.\n")
    print("To use: ")
    print("python rqtcsv_tikz.py [your csv file]")
    exit()
elif len(sys.argv) > 2:
    print("Too many arguments. Only name of .csv file required.")
    exit()

filename = str(sys.argv[1])

if '.tex' in filename:
    print("Not a csv file. Exiting.")
    exit()
try:
    dataframe = pd.read_csv(filename)
except IOError:
    print("File doesn't exist or isn't a .csv file!")
    exit()

print("Converting rqt_plot csv to tikzpicture .tex file ...")
colors = ["black", "yellow", "green", "blue", "purple", "cyan", "magenta"]

# get labels
labels = list(dataframe.columns.values)
time_labels = labels[::2]  
data_labels = labels[1::2] 

tex_filename = filename.split('.')[0]+".tex"
original_stdout = sys.stdout

with open(tex_filename, 'w') as f:
    sys.stdout = f

    print("\\begin{figure}[htb]")
    print("\\centering")
    #print("\\resizebox{\\textwidth}{!}{")
    print("\t\\begin{tikzpicture}")
    print("\t\t\\begin{{axis}}[ xlabel={}, ylabel={}, width=\\textwidth, height=7cm]".format('time', 'y'))

    i = 0
    for data_label in data_labels:
        nr_of_datapoints = dataframe[data_label].shape[0]
        print("\t\t\\addplot[smooth, color={}]".format(colors[i%len(colors)]))
        print("\t\t\tplot coordinates {")
        
        for datapoint in range(nr_of_datapoints):
            valid = True
            x_ = dataframe[time_labels[i]].loc[datapoint] 
            y_ = dataframe[data_label].loc[datapoint]

            

            try:
                if numpy.isnan(x_) :
                    valid = False
            except TypeError:
                if type(x_) == type(''):
                    x_ = x_.replace(' ','')
                    y_ = y_.replace(' ','')

                if x_=='' or y_=='':
                    valid = False
            
            if valid:
                print("\t\t\t\t({}, {})".format(str(x_), str(y_))) 


        print("\t\t\t};")
        print("\t\t\\addlegendentry{{{}}}".format(data_label.replace('/','').replace('_','-')))
        print("\t\n")

        i+=1
    
    print("\t\t\\end{axis}")
    print("\t\\end{tikzpicture}")
    #print("}")
    print("\\caption{My dummy caption}")
    print("\\end{figure}")

    sys.stdout = original_stdout

print ("Conversion complete! {} is ready.".format(tex_filename) )
