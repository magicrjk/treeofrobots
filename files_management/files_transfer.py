import yaml,os
import pathlib
import shutil
from pathlib import Path

def transfer_files(source_dir,target_dir):
    print("Transfering files from "+source_dir+" to "+target_dir)
    file_names = os.listdir(source_dir)
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)
    print("success")

def check_number_files(data_fold,req_num_files):
    print(""" checking that number of files in " """+data_fold+""" " is """+req_num_files)
    num_files = len(os.listdir(data_fold))
    print("number of files = "+str(num_files))
    result = eval(str(num_files)+req_num_files)
    if not result:
        raise Exception("number of files in "+data_fold+" = "+str(num_files)+" does not respect the requirement: "+req_num_files)

def find_num_robot():
    print("")
    folders = os.listdir()
    try:
        folders.remove(".git")
    except ValueError:
        pass
    nums = []
    for fold in folders:
        full_path = [x[0] for x in os.walk(fold)]
        removed_first = [pathlib.Path(*pathlib.Path(x).parts[1:]) for x in full_path]
        all_fold = [x.parts[-1] for x in removed_first if len(x.parts) > 0 ]
        nums.extend([int(x.split("_")[0]) for x in all_fold if x.split("_")[0].isnumeric()])
    return max(nums)

def main():
    with open(os.path.join("files_management","files_structure.yaml"), 'r') as file:
        files_struct = yaml.safe_load(file)
    num_robot = find_num_robot()+1
    prefix_robot = str(num_robot)+"_"
    for class_name,items in files_struct.items():
        datapath = os.path.join("new_robot",class_name) #path files of the user
        codepath = items["destination"]  
        items.pop("destination",None)
        for metric_name,metric_items in items.items():
            if type(metric_items["destination"]) is list:
                metric_items["destination"][-1] = prefix_robot+metric_items["destination"][-1]
                metric_dest = os.path.join(*metric_items["destination"])
                codepath_metric = os.path.join(codepath,metric_dest)
            else:
                metric_dest = metric_items["destination"]
                codepath_metric = os.path.join(codepath,prefix_robot+metric_dest)
            if 'measurement_point' in metric_items.keys():
                codepath_metric = os.path.join(codepath_metric,"C_files")
            datapath_metric = os.path.join(datapath,metric_name)
            if 'num_files' in metric_items.keys():
                check_number_files(datapath_metric,metric_items['num_files'])
            transfer_files(source_dir=datapath_metric,target_dir=codepath_metric)
        
if __name__ == "__main__":
    main()
        
#function checks maximum number in each folder and finds next_robot number

#function throw error if mandatory folder is not existing
    
#function throw error if number of files is less than required