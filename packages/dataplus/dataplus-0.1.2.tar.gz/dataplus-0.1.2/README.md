# datasync
A tool written in Python to synchronize databases in a simple way

The format of the configuration file is as follows:

```
[sourcedb]
host = *.*.*.*
user = yourusername
password = yourpassword
port = 1521
database = databasename
charset = AL32UTF8
timestamp = UPDATETIME
[targetdb]
host = *.*.*.*
user = yourusername
password = yourpassword
port = 3306
database = databasename
charset = utf8mb4
timestamp = UPDATETIME
tablelist = tablename1
            tablename2
            tablename3
```
