# Advanced Cognitive Neuroscience; Autumn 2025

This is the readme for the course Advanced Cognitive Neuroscience run at the Cognitive Science programme at Aarhus University 2025.  
  
All code is tested using Coder Python version **1.103.1**  
  
Some text and code shamelessly stolen from Laura Bock Paulsen's repository: https://github.com/laurabpaulsen/CogNeuro2025/tree/main/EEG_LAB#readme

## Overview

This repository contains the notebooks necessary to the course and the MEG lab. The following important files are included:  
 - `setup_env.sh`: This is a Bash script that sets up a virtual environment for the project. It installs the necessary packages and saves them in a folder called `env`.
 - `env_to_jupyter.sh`: This is a Bash script that installs the virtual environment as a kernel in in Jupyter Notebooks. This is necessary for running the notebooks using the virtual environment.
 - `requirements.txt`: This file lists the packages that are installed in the virtual environment, which the scripts have been tested on.

 Some advanced plotting of brains and such will sadly not work on UCloud, so you would want to create a local environment as well. There will be instructions for that as well.

### Setting up the virtual environment 

To avoid having to install the needed packages every time a new UCloud run is initialised, we will use a virtual environment. This is a way to create a Python environment that is independent of the system Python installation and it is saved in a folder, which means that you can just activate it everytime you start a new run.

Run the following command in the UCloud terminal - (you only need to run this command once)

```
bash setup_env.sh
```

You should notice that a folder called `env`has been created. This is your virtual environment. To activate it, run the following command:

```
source env/bin/activate
```

Within this environment, you are now able to run Python scripts (.py) from your UCloud terminal  
To use the environment inside a Jupyter notebook, you need to install the virtual environment as a kernel. This can be done using the following command:

```
bash env_to_jupyter.sh
```

This latter command can be run when initialising the job. See *Additional parameters* before running job

#### Do it

Now, create your virtual environment and check that you can run Coder Python (use version **1.103.1**)

### Local environment

For maximum compatibility, make sure you have Python **3.12.3** installed (that is what Coder Python 1.103.1 is using).  
`requirements.txt` is the same as on UCloud.  
**Remember**, no sensitive data locally; that is, no FreeSurfer data. I recommend Power Shell on Windows.

Then run:

```
python3 -m venv "<your_path>/env"
source "<your_path/env/bin/activate>  # for Windows: & "<your_path>\env\Scripts\Activate.ps1" (says ChatGPT)
pip install --upgrade pip
python3 -m pip install -r "<your_path/requirements.txt">
```

(Remember `\` instead of `/` in Power Shell)