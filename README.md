#TIGER
A Python module for directly accessing Exodus and Nemesis file data as numpy arrays. I have also provided example scripts for plotting 1D, 2D and 3D exodus files.

Installation instructions:
1. cd ~/projects/
2. git clone https://github.com/chaitanyaBhave26/TIGER.git
3. module load python                             (optional, needed on Hipergator )
4. pip install matplotlib numpy scipy h5py netcdf4
5. cd ~/projects/TIGER/
6. export PYTHONPATH=$PYTHONPATH:~/projects/TIGER (Or whichever location you cloned TIGER to.)

Importing modules from TIGER requires you to run step #6 every time you open the window. Alternatively you can copy that command into your bash profile (~/.bash_profile) using your choice of text editor. After copying the command, either restart the terminal window or run

source ~/.bash_profile

Once added to your bash profile you can access the python module from any location on the computer.
