># Krypter
>* Krypter is a simple file encryption tool that uses AES-256 and Twofish ciphers.
>## Requirements
>* Python 3.5 or higher
>*  *Pycryptodomex* library (Docs: https://bit.ly/3vdV5kF), which can be installed using
>````
> pip install pycryptodomex
> ````
>* *Twofish* library (Pypi: https://bit.ly/3pHbFpK), which can be installed using
>````
> pip install twofish
>````
>* The GUI is implemented using *Tkinter* version 8.6. Verify your version using
>````
> python -m tkinter
> ````
>## Setup
>#### *Make sure all the requirements stated above are satisfied before proceeding!*
> * Clone or download the repository to your PC and extract if need be.
> * The directory structure currently in use is familiar in `Windows` but can be changed to suit `another OS` in the `krypter.py` file
> ![Alt text](screenshots/sub_directories_section.png?raw=true "Directory Structure")
> *Files can be located in the directories that have been set above*
> * Run `krypter.py` to launch the GUI
> > #### *Please note that AES-256 encrypts both .pdf and .txt files successfully whereas Twofish only encrypts .txt files at the moment.* 
