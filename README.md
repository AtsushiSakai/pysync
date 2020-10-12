# pysync
A rsync like tool by pure python only using standard libraries.

# How to use

1. Clone this repo

>$ git clone https://github.com/AtsushiSakai/pysync.git

2. Copy config json file to home dir

>$ cp pysync/pysync_conf.json ~/

3. Modify the config file.

Example:

    {
        "sources": ["../pysync"],
        "dest_dir": "~/backup_test",
        "excludes": [".git", ".idea"]
    }

In Windows, you can set path like:

> C:\\Users\\hoge\\Desktop

4. Run the script

>$ python3 pysql/pysql.py

# Requirements

- Python 3.8

# LICENSE

MIT

# Author

- [AtsushiSakai](https://github.com/AtsushiSakai)