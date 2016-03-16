# LLDB Eigen Data Formatter

LLDB Data Formatter for dense matrices and vectors of the [Eigen](http://eigen.tuxfamily.org) library.

## Installation

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/tehrengruber/LLDB-Eigen-Data-Formatter/master/tools/install.sh)"
```

__Manual Installation__

```bash
INSTALL_PATH=~/.lldb-eigen-data-formatter
git clone https://github.com/tehrengruber/LLDB-Eigen-Data-Formatter.git $INSTALL_PATH
echo 'command script import "'$INSTALL_PATH'/LLDB_Eigen_Data_Formatter.py"' >> ~/.lldbinit
```

## License

Copyright © 2016 Till Ehrengruber

Distributed under the GNU GENERAL PUBLIC LICENSE.