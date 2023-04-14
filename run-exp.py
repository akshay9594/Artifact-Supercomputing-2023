import matplotlib

from subprocess import Popen,PIPE

import sys,re

import os


print("\n*************************************************************************\n")
print("\t\t>Artifact execution for reproducing the results<")
print("\n*************************************************************************\n")


def compile_amgmk(base_path):
    os.chdir(base_path)
    make_result = Popen('make',stdout=PIPE,stderr=PIPE)
    output, err = make_result.communicate()
    output = str(output, 'UTF-8')
    error = str(err, 'UTF-8')

    if(('error:' in output) or ('error:' in error)):
        print("Compilation failed...")
        exit()
    else:
        print("Compilation successfull...")
    return


def compile_UA(baseline,base_path,input_class):
    os.chdir(base_path)

    make_result = ''
   
    if(baseline == '1'):
        make_result = Popen(['make','CLASS='+input_class],stdout=PIPE,stderr=PIPE)
    elif(baseline == '2'):
        make_result = Popen('make',stdout=PIPE,stderr=PIPE)
    
    output, err = make_result.communicate()
    output = str(output, 'UTF-8')
    error = str(err, 'UTF-8')

    if(('error:' in output) or ('error:' in error)):
        print("Compilation failed...")
        exit()
    else:
        print("Compilation successfull...")
    return


def execute_amgmk(iters):
    app_times = []
    loop_times = []

    cores = 0
    for i in range(1,iters):
        exec_result = Popen('./AMGMk',stdout=PIPE,stderr=PIPE)
        output, err_val = exec_result.communicate()
                
        output = str(output,'UTF-8')
        error = str(err_val, 'UTF-8')
        if(isinstance(output,str)):
            search = re.search('Wall time =(.*)seconds.', output)
            wall_time = [float(i) for i in re.findall("\d+\.\d+", search.group(1))]
            app_times.append(wall_time.pop())

            search = re.search('Target loop time=(.*)seconds', output)
            loop_time = [float(i) for i in re.findall("\d+\.\d+", search.group(1))]
            loop_times.append(loop_time.pop())

            if(i == 1):
                search = re.search('max_num_threads =(.*)', output)
                cores = [int(s) for s in re.findall(r'\b\d+\b', search.group(1))].pop()
            
    app_time_sum = 0.0
    for i in range(0,len(app_times)):
        app_time_sum += app_times[i]
    loop_time_sum = 0.0
    for i in range(0,len(loop_times)):
        loop_time_sum += loop_times[i]

    Popen(['make','clean'],stdout=PIPE,stderr=PIPE)
    return (app_time_sum/iters,loop_time_sum/iters,cores)


def select_baseline():

    baseline = input("\n\t1.Serial\n\t2.Cetus-Output-WithoutSubSub\n\t->Select the baseline for comparison:\n")
    if(baseline == '1'):
        print("{Serial baseline selected}\n")
    elif(baseline == '2'):
        print("{Cetus Output without technique applied selected as baseline}\n")
    else:
        print('Invalid Input')
        exit()

    return baseline



def run_exp_amgmk(base_path,opt_code_path,iters):

    print("\nCompiling and Running the baseline code", iters,"times and displaying the execution time...") 
    compile_amgmk(base_path)
    app_time,loop_time,cores = execute_amgmk(iters)
      
    print("\nCompiling and Running the optimized code", iters,"times and displaying the execution time...") 
    compile_amgmk(opt_code_path)
    opt_app_time,opt_loop_time,cores = execute_amgmk(iters)

    print("\n----------------------Timing Results for the application--------------------------\n")
    print("->Average baseline application execution time=", app_time, " s")
    print("->Average application execution time of Cetus Parallelized Code (with technique applied)=", opt_app_time, " s")
    print("->Application Speedup=",app_time/opt_app_time)
    print("->Cores used=",cores)

    print("\n------------Timing Results for the Matrix-Vector Multiplication kernel-------------\n")
    print("->Average baseline kernel execution time=", loop_time, " s")    
    print("->Average kernel execution time of Cetus Parallelized Code (with technique applied)=", opt_loop_time, " s")
    print("->Kernel Speedup=",loop_time/opt_loop_time)
    print("->Cores used=",cores)


def run_exp_UA(baseline,base_path,opt_code_path,input_class,iters):
    print("\nCompiling and Running the baseline code", iters,"times and displaying the execution time...") 
    compile_UA(baseline,base_path,input_class)


val = input("\t1. amgmk-v1.0\n\t2. UA-NAS\n\t->Select the benchmark you want to test by entering the number:\n")

if(val == '1'):
    print("{amgmk-v1.0 selected for evaluation}\n")
    input_matrix = ''
    baseline = select_baseline()
    ans = input("\t->Do you want to run the experiment for all input matrices?yes or no\n")
    base_path = ''
    root = os.getcwd()
    opt_code_path = root+'/amgmk-v1.0/Technique_Applied/'

    if(ans == 'yes'):
        for i in range(1,6):
            input_matrix = 'MATRIX'+ str(i)
            print(input_matrix)

    elif(ans == 'no'):
        print("\n========================= Producing the results ===================================\n")
        mat_num = input("->Enter the number of the matrix from 1 to 5 to use as input:")
        input_matrix = 'MATRIX' + str(mat_num)
        print("{Input matrix selected for experiment: ",input_matrix,"}\n")

        if(baseline == '1'):
            base_path = root+'/amgmk-v1.0/Baselines/Serial/'+input_matrix
            
        elif(baseline == '2'):
            base_path = root+'/amgmk-v1.0/Baselines/Cetus-Output-WithoutSubSub/'+input_matrix
        
        iters = 3
        opt_code_path += input_matrix
        run_exp_amgmk(base_path,opt_code_path,iters)

        os.chdir(root)
    else:
        print("Invalid Input")
        exit()

elif(val == '2'):
    print("{UA-NAS selected for evaluation}")

    input_class = ''
    baseline = select_baseline()
    ans = input("\t->Do you want to run the experiment for all input matrices?yes or no\n")

    base_path = ''
    root = os.getcwd()
    opt_code_path = root+'/UA-NAS/Technique_Applied/'


    print("\n========================= Producing the results ===================================\n")

    if(ans == 'yes'):
        input_classes = ['CLASS=A', 'CLASS=B', 'CLASS=C', 'CLASS=D']
        for cl in input_classes:
            print(cl)

    elif(ans == 'no'):
        input_class = input("Enter the Input Class (A,B,C or D) to use:")

        if(baseline == '1'):
            base_path = root+'/UA-NAS/Baselines/Serial/UA'
            
        elif(baseline == '2'):
            base_path = root+'/UA-NAS/Baselines/Cetus-Output-WithoutSubSub/CLASS-'+input_class
        
        iters = 3
        run_exp_UA(baseline,base_path,opt_code_path,input_class,iters)

        os.chdir(root)
    else:
        print("Invalid Input")
        exit()

else:
    print("Invalid input")
