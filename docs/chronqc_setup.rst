Install ChronQC
===============

Requirement
```````````

ChronQC is implemented in Python (tested with v2.7 / v3.5 / v3.6) and runs on all common operating systems (Windows, Linux and Mac OS X).

Installation
````````````

You can install ChronQC from PyPI using pip as follows::
    
    pip install chronqc
..
        Alternatively, you can install using Conda from the Bioconda channel::

        INSTALL_PATH=~/anaconda
        wget http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
        # or wget http://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
        bash Miniconda2-latest* -fbp $INSTALL_PATH
        PATH=$INSTALL_PATH/bin:$PATH

        conda update -y conda
        conda config --add channels bioconda
        conda install -c bioconda chronqc
..

Alternatively, you can install from GitHub::

    git clone https://github.com/nilesh-tawari/ChronQC_dev.git
    cd ChronQC
    pip install -r requirements.txt
    pip install --editable .

If you would like the development version instead, the command is::

    pip install --upgrade --force-reinstall git+https://github.com/nilesh-tawari/ChronQC_dev.git
    

Alternatively, ChronQC can also be used as Docker::

    #Pull docker image
    docker pull nileshtawari/chronqc:chronqc_1.0.3
   
    #Run docker
    docker run -it chronqc_1.0.3
   
    #Test ChronQC using example data
    cd /home/ChronQC
    
    Then follow instructions given in `getting started. <http://chronqc.readthedocs.io/en/latest/run_chronqc.html#generating-chronqc-plots>`__. 
    
    


