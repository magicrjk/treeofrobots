import os

def generate_init_robots(selected_robots):
 file_path = "init_robots.txt"  
 if os.path.exists(file_path):
        os.remove(file_path)
 else:
        print(f"{file_path} being written.")
 with open('init_robots.txt', 'w') as file:
        if len(selected_robots)==3:
              file.write(f"{selected_robots[0]}\n")
              file.write(f"{selected_robots[1]}\n")
              file.write(f"{selected_robots[2]}\n")
        elif len(selected_robots)==2:
              file.write(f"{selected_robots[0]}\n")
              file.write(f"{selected_robots[1]}\n")
        elif len(selected_robots)==1:
              file.write(f"{selected_robots[0]}\n")
        elif len(selected_robots)<1:
              file.write(f"1\n")
              file.write(f"2\n")
              file.write(f"3\n")
              print('no choince made, using robots nr. 1-3 instead')
        else :
              file.write(f"{selected_robots[0]}\n")
              file.write(f"{selected_robots[1]}\n")
              file.write(f"{selected_robots[2]}\n")
              print('Too many robots selected, using first 3 provided robots')

              
              

 print("init_robots.txt file created successfully!")
