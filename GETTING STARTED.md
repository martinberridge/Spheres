Setup instructions

Install choco using instructions from chocolatey.org
choco install python2
choco install graphviz
choco install jdk7

pip install --upgrade pip
pip install networkx
pip install pydot
pip install pydot2

download numpy-1.10.1+mkl-cp27-none-win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install numpy-1.10.1+mkl-cp27-none-win_amd64.whl
download pandas-0.17.0-cp27-none-win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install pandas-0.17.0-cp27-none-win_amd64.whl
download QuantLib_Python-1.6.1-cp27-none-win_amd64.whl from http://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install QuantLib_Python-1.6.1-cp27-none-win_amd64.whl
 
download Gephi from gephi.github.com
install Gephi
edit c:\program files (x86)\gephi\etc\gephi.conf to change jdk path as described in https://forum.gephi.org/viewtopic.php?f=3&t=3580&p=10712#p10712
install "Graph Streaming" plugin in Gephi (from Tools->Plugins menu)
start Gephi graph streaming server (from Windows->Streaming, then right click on the 'Master Server' and select start)