# Hello Password

A very simple secure password management tool.

**Why?** Because I can't believe the current password management software. In addition, the fact that the data file cannot be exported bothers me.

## Quick Start

### Use `hpass -i` Initialize password data file in specified directory

```powershell
$  hpass -i
Your primary password:
Enter your primary password again:
Find the password storage file in the current directory
Password storage file initialized successfully
```

### Use `hpass` enter Workbench

```powershell
$ hpass
Your primary password:
H-Pass>
```

#### Use `random` generate a secure random password

```powershell
H-Pass> random 16
hiSVJ@77AEYFaZhu
```

#### Use `add` generate a secure random password

```powershell
H-Pass> add
The following is the information required for the new password :
Website = https://www.yeah.net/
Notes = 163 Yeah Mail
Username = xxxxxxx@yeah.net
Email =
Phone =
Password = hiSVJ@77AEYFaZhu
The new password has been successfully added!
```

#### Use `search` search password data

```powershell
H-Pass> search yeah
+----+-----------------------+--------------+
| ID |        Website        |    Notes     |
+----+-----------------------+--------------+
| 18 | https://www.yeah.net/ | 163 Yeah Mail |
+----+-----------------------+--------------+
```

#### Use `get` view password data

```powershell
H-Pass> get 18
website = https://www.yeah.net/
notes = 163 Yeah Mail
username = xxxxxxx@yeah.net
email =
phone =
password = hiSVJ@77AEYFaZhu
```

#### Use `set` change password data

```powershell
H-Pass> set 18 notes
Original notes = 163 Yeah Mail
Now notes = Yeah Mail
Password value modified successfully!
```

#### Use `help` view help information

```powershell
H-Pass> help
filepath           - Print the absolute path of the password storage file
all                - View the basic information of all password data
add                - Enter a new password data
search <keyword>   - Find password data by keyword
random <length>    - Generate a secure password of specified length
get <id>           - View the password data of the specified id
del <id>           - Delete the password data of the specified id
set <id> <key>     - Modify the key value of the password data of specified id
```

## Installation

As usual, the easiest way is with pip:

```powershell
$ pip install hpass
```

Alternatively you can [download](https://pypi.org/project/hpass/#files) the `hpass-x.x.x.tar.gz` installation file:

```powershell
$ pip install hpass-x.x.x.tar.gz
```

Pip will install dependencies *([colorama](https://pypi.org/project/colorama/) and [PrettyTable](https://pypi.org/project/PrettyTable/))* for you. Alternatively you can clone the repository:

```powershell
$ git clone https://github.com/hekaiyou/hpass.git --recursive
$ cd hpass
$ python setup.py install
```

## License

`hpass` is free and open-source software licensed under the [MIT License](https://github.com/hekaiyou/hpass/blob/master/LICENSE).