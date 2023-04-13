import glob

from subprocess import Popen,PIPE

import sys,re

import os

print("\n***************************************************\n")
print(">Artifact execution for reproducing the results<")
print("\n***************************************************\n")

val = input("1. amgmk v1.0\n2. UA-NAS\n->Select the benchmark you want to test by entering the number:\n")

if(val == '1'):
    baseline = input("\n1.Serial\n2.Cetus-Output-WithoutSubSub\n->Select the baseline for comparison:\n")
    if(baseline == '1'):
        print("{Serial baseline selected}\n")
        ans = input("->Do you want to run the experiment for all input matrices?yes or no\n")
        if(ans == 'yes'):
            for i in range(1,6):
                input_matrix = 'MATRIX'+ str(i)
                print(input_matrix)
                #subprocess.call([],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        elif(ans == 'no'):
            mat_num = input("->Enter the number of the matrix from 1 to 5 to use as input:")
            input_matrix = 'MATRIX' + str(mat_num)
            print("{Input matrix selected for experiment: ", input_matrix,"}\n")
            print("->Running the baseline code 5 times and displaying the execution time...") 
            root = os.getcwd()
            path = root+'/amgmk-v1.0/Baselines/Serial/'+input_matrix
            os.chdir(path)
            make_result = Popen('make',stdout=PIPE,stderr=PIPE)
            output, err = make_result.communicate()
            error = str(err, 'UTF-8')

            if(error == ''):
                print("Compilation successfull...")
            else:
                print("Compilation failed...")

            times = []
            for i in range(1,6):
                exec_result = Popen('./AMGMk',stdout=PIPE,stderr=PIPE)
                output, err_val = exec_result.communicate()
                
                output = str(output,'UTF-8')
                error = str(err_val, 'UTF-8')
                if(isinstance(output,str)):
                    search = re.search('Wall time =(.*)seconds.', output)
                    wall_time = [float(i) for i in re.findall("\d+\.\d+", search.group(1))]
                    times.append(wall_time.pop())
            
            sum = 0.0
            for i in range(0,len(times)):
                print(i)
                sum += times[i]
            
            print("Average Application execution time = ", sum/5 , 's')
    
                
    elif(baseline == '2'):
        print("Cetus Output without technique applied selected as baseline")

elif(val == '2'):
    print("UA-NAS selected for evaluation")
else:
    print("Invalid input")
