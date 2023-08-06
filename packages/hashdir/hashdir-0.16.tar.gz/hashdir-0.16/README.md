# hashdir

A command line tool to calculate hash of directory trees using various hash algorithms.

## installation

To install run the following command in your terminal:

```pip3 install hashdir```

## usage

```text
usage: hashdir [-h] [-a {md5,sha1,imohash}] [--log-level {error,info,debug}]
               [directory]

hashdir

positional arguments:
  directory

optional arguments:
  -h, --help            show this help message and exit
  -a {md5,sha1,imohash}, --algorithm {md5,sha1,imohash}
                        warning: imohash is a constant-time hashing library,
                        and while being fast for large files, it produces
                        approximate results.
  --log-level {error,info,debug}
```

## contributing

Contributions are welcome! Please use black for formatting code before sending a PR.
