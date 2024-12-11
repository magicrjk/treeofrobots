# Basic Flask Website for Tree of Robots

To run, in a Python environment, first install the required packages with Conda and pip on python 3.12.
* `conda env -n my_env python==3.12`
* `requirements.txt` lists the "clean" `pip` package installs.
    - `pip install -r requirements.txt`
* `environment.yml` lists the packages installed by `conda`, 
    - With your desired environment ACTIVE, `conda env update --file environment.yml` 

Then run the server by running this command in the `FlaskWebsite` directory: `python3 app.py`. The starting directory matters, since there is relative import via `sys.path.append`.
(Tested by running the above commands)

## Current features
- Form submission & data transfer back to python backend working, specifically `display()`
    - For renaming the checkbox text, given this line: 
        `<input type="checkbox" name="process" value="process1"> Process 1<br>`
        Change the one between the brackets, i.e. `...> Process 1<br>` to whatever you want.
        The value field is what you will see in the python side, e.g.
        - if the user chooses Process 1, 2, 3, you will see: 
        `['process1', 'process2', 'process3']`. You can then process this as the correct input format for retrieving the robots.
- SQLite3 connection working
- Morphology graph construction working, with correct colors
- Fitness graph construction working, with correct colors

## To-do
- Implement the functions for querying the robots based on the user's selected processes, specifically `retrieve_robot_numbers`