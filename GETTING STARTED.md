## Setup instructions

#### Install windows packages

1. Install choco using instructions from https://chocolatey.org
2. `choco install python2`
3. `choco install graphviz`
4. `choco install jdk7`

#### Install python packages

1. `pip install --upgrade pip`
2. `pip install networkx`
3. `pip install pydot`
4. `pip install pydot2`

#### Install pre-built python packages which require more complex setup

1. download numpy-1.10.1+mkl-cp27-none-win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/
2. `pip install numpy-1.10.1+mkl-cp27-none-win_amd64.whl`
3. download pandas-0.17.0-cp27-none-win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/
4. `pip install pandas-0.17.0-cp27-none-win_amd64.whl`
5. download QuantLib_Python-1.6.1-cp27-none-win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/
6. `pip install QuantLib_Python-1.6.1-cp27-none-win_amd64.whl`

#### Install and configure Gephi

1. download Gephi from http://gephi.github.io
2. install Gephi
3. edit `c:\program files (x86)\gephi\etc\gephi.conf` to change jdk path as described in https://forum.gephi.org/viewtopic.php?f=3&t=3580&p=10712#p10712
4. install "Graph Streaming" plugin in Gephi (from `Tools->Plugins` menu)
5. start Gephi graph streaming server (from `Windows->Streaming`, then right click on the 'Master Server' and select start)
