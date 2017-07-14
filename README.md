# LLDB Eigen Data Formatter

LLDB Data Formatter for dense matrices and vectors of the [Eigen](http://eigen.tuxfamily.org) library.

## Example

```cpp
Eigen::Matrix<double, 3, 3> A;
A << 1, 0, 0,
	 0, 2, 0,
	 0, 0, 3;
```

Corresponding output in LLDB

```
(lldb) print A
(Eigen::Matrix<double, 3, 3, 0, 3, 3>) $11 = rows: 3, cols: 3
[ 1 0 0 ]
[ 0 2 0 ]
[ 0 0 3 ]
```

The code has been modified to allow printing of arbirary/dynamically sized Eigen types. If the Eigen type uses Eigen::PlainObjectBase storage (MatrixXd, VectorXd, Quaternion, etc) it will print the contents in a viewable format (up to a maximum of 25x25 items)

## Installation

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/timjj22/LLDB-Eigen-Data-Formatter/master/tools/install.sh)"
```

__Manual Installation__

```bash
INSTALL_PATH=~/.lldb-eigen-data-formatter
git clone https://github.com/timjj22/LLDB-Eigen-Data-Formatter.git $INSTALL_PATH
echo 'command script import "'$INSTALL_PATH'/LLDB_Eigen_Data_Formatter.py"' >> ~/.lldbinit
```

__Uninstallation__

```bash
rm -fr ~/.lldb-eigen-data-formatter
```

Afterwards remove the `command script import` command in `~/.lldbinit`.

## License

Original work Copyright © 2016 Till Ehrengruber
Modified work Copyright © 2017 Timothy Jeruzalski

Distributed under the GNU GENERAL PUBLIC LICENSE.
