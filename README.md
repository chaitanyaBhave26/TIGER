# TIGER

TIGER is a Python module for directly accessing Exodus and Nemesis file data as numpy arrays. Examples demonstrate how to generate high quality figures using matplotlib and the TIGER interface.

## Installation instructions:
1. Go to your installation directory
    ```
    cd ~/projects/
    ```
3. Clone the TIGER repo
    ```
    git clone https://github.com/chaitanyaBhave26/TIGER.git
    ```

### Option A - Conda installation (Recommended):
If you don't already have Conda, install by following the instructions on the [Conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

3. If installing on a HPC
    ```
    module load conda
    ```
 
4. Create the TIGER environment and install dependencies
    ```
    conda create --name tiger_env h5py netcdf4 matplotlib scipy numpy
    ```
6. Activate the TIGER environment. This step needs to be run whenever you want to use TIGER in a new terminal tab or window)
    ```
    conda activate tiger_env
    ```   
7. Install the TIGER package in development mode
    ```
    conda develop ~/projects/TIGER
    ```                 
8. Optionally, you can install OpenCV if you want to perform Computer Vision operations on your exodus file outputs.
    ```
    conda install -c menpo opencv
    ```
  
### Option B - Pip installation :
3. If installing on a HPC, load python module
    ```
    module load python
    ```
4. Install dependencies using PIP
    ```
    pip install matplotlib numpy scipy h5py netcdf4 opencv-python
    ```
5. Change to TIGER directory
    ```
    cd ~/projects/TIGER/
    ```
6. Add TIGER directory to PYTHONPATH
    ```
    export PYTHONPATH=$PYTHONPATH:~/projects/TIGER
    ```
7. Importing modules from TIGER requires you to run step #6 every time you open the window. Alternatively you can copy that command into your bash profile (~/.bash_profile) using your choice of text editor. After copying the command, either restart the terminal window or run
  ```
  source ~/.bash_profile
  ```
Once added to your bash profile you can access the python module from any location on the computer.
