[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)

# GWN3 Quick Start
GR: [GNU Radio](https://www.gnuradio.org/). Version 3.8 required.

GRC: GNU Radio Companion, the GR graphic environment.

In Ubuntu based Linux distributions (e.g. LinuxMint), the easiest way to install GNU Radio is to follow the instructions on [UbuntuInstall](https://wiki.gnuradio.org/index.php/UbuntuInstall). For general instructions, please see [InstallingGR](https://wiki.gnuradio.org/index.php/InstallingGR).

## Install GWN3
1. Clone the project.
  ```
	cd <your_install_directory>
	git clone https://github.com/vagonbar/gr-gwn3.git  
  ```
2.Build the project.
  ```
	cd gr-gwn3
	mkdir build  
	cd build  
	# for a system space installation:
	cmake ../  
	# for a user space installation use this instead:
	#cmake -DCMAKE_INSTALL_PREFIX=<your_GNURadio_install_dir> ../
	make
	sudo make install  
	sudo ldconfig   # on Debian/Ubuntu based distributions
  ```
3. Adjust environment variables.
  To make `gr-gwn3` accesible you may have to add some lines to the `~/.bashrc` file. For a system wide GNU Radio installation, something like the following:
  ```
  export PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3/dist-packages/gwn3:$PYTHONPATH
  export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
  ```
  The exact form may depend on the GR installation. To verify, `import gwn3` must work in a Python environment:
  ```
  $ python3
  >>> import gwn3
  >>> dir(gwn3)
  ```
  The list shown must contain the GWN blocks defined.

4. Run a test example:
  ```
	python3 ../python/qa_msg_passer.py 
  ```
5. Run an example GRC flowgrtaph:
	1. Open GRC. In a terminal,
		```gnuradio-companion```
	2. In GRC, open file `gr-gwn3/examples/msg_passer_test.grc`.
6. Now you are ready to create your own GWN blocks.

## Create a new GWN block
The following procedure creates a block called `my_block` with 1 input port, 1 output port, 0 timers, and 2 timeouts; this example is similar to the `msg_passer` block. The new block is created through the GWN `gwn_modtool` script, similar to GR `gr_motdool`. Please note the script must be run from the project's `build` directory, usually `gr-gwn3/build`.

1. Create new block:
	```
	cd build    # script must be executed from the build directory
	python3 ../libgwn/gwn_modtool.py add my_block 1 1 0 2
	```
	The script will ask for
	-	an optional list of user defined parameters, e.g. `nr_times=12,payload="This is my payload"`
	-	a label to name the new block in GRC., e.g. `Message passer`.
2. Edit the new block files, referred from the `build` directory;
	-	`../python/my_block_py`, add your own processing code.
	-	`../python/qa_my_block_py`, write your test code for the new block.
	-	`../grc/gwn3_my_block.block.yml`, adjust for GRC visibility.
3. Run the tests and correct the code until the desired results are obtained.
4. Build the project. From the `build` directory, issue the usual commands to integrate the new block into GR and GRC.
	```
	make
	sudo make install
	sudo ldconfig     # required for Ubuntu based Linux
	```
5. In GRC, create a flowgraph to complete the testing of the new block.
	
## Remove a GWN block
To delete a GWN block, use the same `gwn_modtool` script, always running it from the `build` directory.

1. Remove block.
	```
	cd build    # script must be executed from the build directory
	python3 ../libgwn/gwn_modtool.py rm my_block
	```
	The block is removed.
2. Update changes in the project, removing block from it.
	```
	make
	sudo make install
	sudo ldconfig     # required for Ubuntu based Linux
	```
	
[Back to README](../../README.md)

