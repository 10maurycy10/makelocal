import sys
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urlunparse
from bs4 import BeautifulSoup
import argparse

newbase = "file:///home/mz/archive/"

#src_prefix = ".bak"
#make_copy = False

make_copy = True
src_prefix = ""

# Base is the default base for reletive URLS, it should be the url the document was retreved from
# srcfile is the location to read the document to.
def convert(srcfile, base):
    with open(srcfile + src_prefix, "r") as src:
        # read srcfile.
        srchtml = src.read()
        # backup orgiginal
        if make_copy:
            with open(srcfile + ".bak", "w") as new:
                new.write(srchtml)
        # parse html
        soup = BeautifulSoup(srchtml, 'html5lib')
        # <base> tags can change the base of urls, we have to handle that
        document_base = base
        for tag in soup.find_all("base"):
            document_base = tag.attrs.get("href")
        # for all tags..
        for tag in soup.find_all(True):
            # for all attrs...
            for attr in tag.attrs.keys():
                # if attr is a string...
                if type(tag[attr]) is type(""):
                    # attr is href or src..
                    if attr in ["href", "src"]:
                        # parse the url and extract the path and host
                        url = urlparse(urljoin(document_base, tag[attr]))
                        path = url.path
                        netloc = url.netloc
                        # Fix for <a> tags with wget --adjust-extention
                        if tag.name == "a":
                            #print(tag.name, tag.text)
                            if path.endswith("/"):
                                #print("changing path in ", tag.text)
                                path = path + "index.html"
                        tag[attr] = newbase + netloc + path
    # reseralize the html
    return str(soup)



parser = argparse.ArgumentParser(description = "Convert links in html files for local viewing. file names are read from stdin.")
parser.add_argument("directory", help="The absolute location of the files.", type=str)
parser.add_argument("-b", "--backup", help = "Backup origninal files, recomemded for first run", action="store_true")
parser.add_argument("-o", "--original", help = "Used backedup files, recomemeded for later rust", action="store_true")
args = parser.parse_args()

newbase = "file://" + args.directory
make_copy = args.backup
if args.original:
    src_prefix = ".bak"
else:
    src_prefix = ""

for line in sys.stdin.readlines():
    try:
        line = line.rstrip("\n")
        print(line)
        converted = convert(line,"https://" + line);
        with open(line, "w") as new:
            new.write(converted)
    except Exception as e:
        print("ERROR" + e)
