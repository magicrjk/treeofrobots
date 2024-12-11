from nptdms import TdmsFile
import os

root = "new_robot" #convert all the .tdms files in this folder
new_extension = ".csv" #new file extension (.csv tested only)
for path, subdirs, files in os.walk(root):
    for file in files:
        if file.endswith(".tdms"):
            tdms_filename = os.path.abspath(os.path.join(path, file))
            with TdmsFile.open(tdms_filename) as tdms_file:
                base_name = os.path.splitext(tdms_filename)[0]
                new_filename = base_name + new_extension
                tdms_file.as_dataframe().to_csv(new_filename, sep=',', index=False, encoding='utf-8')
            try: 
                os.remove(tdms_filename)
                os.remove(tdms_filename+"_index")
            except Exception as error:
                print("Exception occurred:", error)




