import time, glob, os.path, pathlib, datetime
from subprocess import run, PIPE
report_file = "report.txt"

def exec_command(command):
   
    output = run(command, shell=True, stdout=PIPE)
    results = output.stdout.decode('utf-8')
    return results

def append_report(reportfile, msg):

    
    f = open(reportfile, "a")
    f.write(msg)
    f.close()

def start_remote_autopsy():

    os.system("sshpass  -p munge@2021 ssh -t esho@23.254.224.106 'sudo autopsy 41.215.47.126'")

def get_case_details():

    print("Enter the following details")
    case_name = input("Case Name: ")
    case_no = input("Case No: ")
    case_examiner = input("Case Examiner: ")
    case_desc = input("Case Description: ")
    
    details = "\n"
    details += "Case Name: " + case_name + "\n"
    details += "Case No: " + case_no + "\n"
    details += "Case Examiner: " + case_examiner + "\n"
    details += "Case Description: " + case_desc + "\n"
    details += "IP of Server: 23.254.224.106\n"

    return details
    
def check_drives(filename):
    file_exists = os.path.exists(filename)
    if (file_exists): 
     thefile = open(filename, 'r')
     nonempty_lines = [line.strip("\n") for line in thefile if line != "\n"]
     line_count = len(nonempty_lines)
     
     thefile.close()
     
     if (line_count != 0):
      return True
     else:
      return False
          
def list_drives(filename):   
    
     if (check_drives(filename)):
      
      thefile = open(filename, 'r')
      
      nonempty_lines = [line.strip("\n") for line in thefile if line != "\n"]
      line_count = len(nonempty_lines)
      thefile.close()      
      thefile = open(filename, 'r')
      lines = thefile.readlines()
      msg = 'Found '+ str(line_count) + ' drive(s)'
      print(msg)
      append_report(report_file, msg)
      thefile.close()
    
      for theline in lines:
       res = theline.split(' ')[0]
       res = " " + res 
       print(res)
       append_report(report_file, res)
     else:
      msg = 'No portable storage media (external drive(s)) was found! Please ensure that the PSM is/are properly attached to the local machine and the operating system detects the plug'
      print(msg)
      append_report(report_file, msg)
      print (' ')
      
def chkdsk_drives(filename):
    
   if (check_drives(filename)):
    thefile = open(filename, 'r')
    lines = thefile.readlines()
    thefile.close()
    
    for theline in lines:
     res = theline.split(' ')[0]
     msg = "Executing fsck on " + res + "\n"
     print(msg)
      
     append_report(report_file, msg)
     
     msg = exec_command("sudo umount " + res)
    
     msg += exec_command("sudo fsck -a -v -V -t -p " + res )
     
     msg += "\n Finished fsck on " + res + "\n"
     
     print(msg)
      
     append_report(report_file, msg)

def image_drives(filename):
    
    if (check_drives(filename)):
     thefile = open(filename, 'r')
     lines = thefile.readlines()
     thefile.close()
    
     for theline in lines:
      res = theline.split(' ')[0]
      msg = "Preparing image for " + res
      print(msg)
      
      append_report(report_file, msg)
      
      the_pwd = exec_command("pwd")
      the_pwd = the_pwd.strip()
      img_dest = the_pwd+"/img_dest"
      
      msg = "to be imaged to "+img_dest+" "
      print(msg)
      append_report(report_file, msg)
      print('The image directory shall be created if it does not exist')
      print (exec_command("sudo mkdir "+img_dest))
      path = pathlib.PurePath(res)
      drive_name = path.name
      msg = "Generating the image, == "+drive_name+".dd == at "+img_dest+"/"
      print(msg)
      append_report(report_file, msg)
      print(exec_command("sudo dd if=" + res + " of="+img_dest+"/"+drive_name+".dd count=10MB status=progress "))
      msg = "Finished imaging of " + res + " "
      print(msg)
      append_report(report_file, msg)
 
def compute_file_hash():
      pwd = os.getcwd()
      os.chdir(pwd + "/img_dest/")
      reportfile = pwd+"/"+report_file
      
      for file in glob.glob("*.dd"):
      	   md5_time = datetime.datetime.now()
      	   sha1_time = datetime.datetime.now()
      	   
      	   print(exec_command("ls -sh " + file))
      	   md5_hash = exec_command("rhash --md5 " + file)
      	   md5_time = datetime.datetime.now()
      	   md5_time = md5_time.strftime("%Y-%m-%d %H:%M:%S.%f")
      	   sha1_hash = exec_command("rhash --sha1 " + file)
      	   sha1_time = datetime.datetime.now()
      	   sha1_time = sha1_time.strftime("%Y-%m-%d %H:%M:%S.%f")
      	   md5_hash = md5_hash + " as at " + md5_time
      	   sha1_hash = sha1_hash + " as at " + sha1_time
      	   md5_hash = "MD5 hash: " + md5_hash
      	   sha1_hash = "SHA1 hash: " + sha1_hash
      	   print(md5_hash)
      	   print(sha1_hash)
      	   append_report(reportfile, md5_hash)
      	   append_report(reportfile, sha1_hash)
      	   print('')
    	   
def copy_image_to_remote():
	
      for file in glob.glob("*.dd"):
          msg = "Start copying image file: " + file + " to cloud server"
          print(msg)
          append_report(reportfile, msg)
          os.system("rsync -av --info=progress2 -e ssh  "+pwd+"/img_dest/"+file+"  esho@23.254.224.106:/home/esho/project")
          msg = "Finished copying " + file + " to server"
          print(msg)
          
          append_report(reportfile, msg)
          
 
          

