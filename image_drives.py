import time, glob, os.path, pathlib, datetime
from subprocess import run, PIPE

from proj_functions import *        	   
           
def main():
    print(exec_command("clear"))
    print("Starting Script ... Please wait")
    for x in range(10):
     time.sleep(1/10)
     print("= = ", end=" ", flush=True)
     
    print()

    print ("=================STEP1:CASE DETAILS=====================================")
    time.sleep(3)
    for x in range(10):
     time.sleep(1/10)
    print(".", end=" ", flush=True)
    case_details = get_case_details()
    print ("Confirmation of case details; you entered: " + case_details)
    f = open(report_file, "w")
    f.write(case_details)
    f.close()
    
    print ("=================STEP2:DETECTION OF DRIVE(S) FOR IMAGING================")
    time.sleep(3)
    print("Listing drives . . .")
    output_file_1 = "driveslist.txt"
    def_command = "sudo sfdisk -l | grep -v '/dev/sda' | grep -E '^/dev' > " + output_file_1
    output = exec_command(def_command)
    list_drives(output_file_1)
    
    print("=================STEP3: EXECUTING fsck on PORTABLE STORAGE MEDIA========")
    time.sleep(3)
    print('The system utility fsck is a tool for checking the consistency of file system of the drive(s).') 
    print('Changes on drive sectors shall be documented')
    print("Checking drives ... ")
    chkdsk_drives(output_file_1)
    
    print("=================STEP4: IMAGING OF THE PORTABLE STORAGE MEDIA==========")
    time.sleep(3)
    image_drives(output_file_1)
    print("Create img_dest directory if it does not exist ... ")
    exec_command("sudo mkdir img_dest")
    print("Imaging drives ... ")
    
    print("=================STEP5: COMPUTING FILE HASH OF THE IMAGE======")
    print("The file hash shall be maintained through out the case life cycle to ensure case integrity preservation.")
    compute_file_hash()

    print("=================STEP6: REPLICATING IMAGE TO CLOUD FOR PROCESSING======")
    print("Copy image to remote server ... ")
    copy_image_to_remote()
    
    print("=================STEP7: INDEXING THE IMAGE WITH AUTOPSY FOR ANALYSIS===")
    print("Start autopsy ... ")
    start_remote_autopsy()

if __name__ == '__main__':
    main()
