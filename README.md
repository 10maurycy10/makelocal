# makelocal

A tool to prepare websites grabbed with wget for local viewing.

## exapmples

After fetching xkcd.com with: 

```
wget -r -no-remove-listing -r -N --page-requisites --adjust-extension -HD xkcd.com xkcd.com
```

You can run this command convert links in the HTML documents to refrence your local version.

```
find xkcd.com | grep '\.html' | grep -v '\.bak'| python3 convert.py -b `pwd`
```

## Usage

```
usage: convert.py [-h] [-b] [-o] directory

Convert links in html files for local viewing. file names are read from stdin.

positional arguments:
  directory       The absolute location of the files.

options:
  -h, --help      show this help message and exit
  -b, --backup    Backup origninal files, recommended for first run
  -o, --original  Used backed up files, recommended for later runs
  ```
  
  - -b save the original file to \[filename\].bak this is usefull to avoid having to grab a fresh tree if you mess something up or move the files.
 
