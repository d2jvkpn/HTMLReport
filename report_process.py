import os, argparse, json
from configparser import ConfigParser
from glob import glob

HELP = '''Generate HTML5 using template and ini confgiure.
Specify html5:
  <"tag">.check to reserve an element: data-file, data-file-match, data-file-miss
  <div> attribution data-level: children of <div>#main
  <figure>.myTable binding data: data-file, data-xcols, data-ncols, data-nrows
  <figure>.mySlide binding data: data-file(comma as seperator), data-file-match
  <div>#reference match anchor: <a>.name correspond with children <p>.id

  1. write your owner <header> and <footer>;
  2. data-file-match support wildcard by glob.glob;
  3. required packages: pandas, beautifulsoup4, jinja2, html5print.
'''

__author__ = "d2jvkpn"
__version__ = "0.7"
__release__ =  "2019-08-30"
__project__ =  "https://github.com/d2jvkpn/HTMLreport"
__license__ = "GPLv3  (https://www.gnu.org/licenses/gpl-3.0.en.html)"


parser = argparse.ArgumentParser ()

parser.add_argument ('-i', dest='input', help = 'input html as template')
parser.add_argument ('-o', dest='output', help = 'output html')

parser.add_argument ('-ini', dest='ini', default="", help = 'ini config " + \
    "file(s), which default section(s) to be converted to a dict')

parser.add_argument ('-remove', dest='remove', default="", 
    help = 'remove element by id(s)')

parser.add_argument ('-reserve', dest='reserve', default="", 
    help = 'reserve element(s) that may be decomposed')

if len(os.sys.argv) == 1 or os.sys.argv[1] in ['-h', '--help']:
    print(HELP)
    parser.print_help ()

    _ = '\nauthor: {}\nversion: {}\nrelease: {}\nproject: {}\nlicense: {}\n'
    __ = [__author__,  __version__, __release__, __project__, __license__]
    print (_.format (*__))

    os.sys.exit(2)

args = parser.parse_args ()

templ, out = args.input, args.output, 
cfgs = args.ini.replace(",", " ").split()
remove = args.remove.replace(",", " ").split()
reserve = args.reserve.replace(",", " ").split()
pp = os.path.dirname(os.path.abspath(out))
os.makedirs(pp, exist_ok=True)

import pandas as pd
from bs4 import BeautifulSoup, Tag
from jinja2 import Template
from html5print import HTMLBeautifier


## read config to dict
dm = {"Project": "Play Web Front", "lang": "en"}

for p in cfgs:
    if p == "": continue
    if p.endswith(".ini") or p.endswith(".cfg"):
        cfg = ConfigParser ()
        cfg.optionxform = str
        with open(p, "r") as f: s = f.read()
        cfg.read_string ("[DEFAULT]\n" + s)
        d = dict(cfg.defaults())
        for k in d: dm[k] = d[k] if d[k] != "" else dm.get(k, "")
    elif p.endswith(".json"):
        with open(p, "r") as f:
            d = json.load(d)

        for k in d: dm[k] = d[k] if d[k] != "" else dm.get(k, "")
    else:
        os.exit("config file \"%s\" is neither ini/cfg or json" % p)

with open(templ, "r") as f: soup = BeautifulSoup(f.read(), 'html5lib')
main = soup.find(id="main")
wd = os.getcwd(); os.chdir(pp)


## remove elements by id
for i in remove:
    if i == "": continue
    el = soup.find(id=i)
    if el == None: os.sys.exit("not found element by id \"%s\"" % i)
    
    el.decompose()
    print("decompose element %s by id \"%s\""  % (el.name, i))


## check file exits or file miss to drop element
for el in main.find_all(attrs={"class" :"check"}, recursive=True):
    if el is None or el.attrs is None: continue
    if el.attrs.get("id", "") in reserve: continue
    ## don't split to a list
    p = el.attrs.get("data-file")
    pn = el.attrs.get("data-file-miss")
    ps = el.attrs.get("data-file-match")
    drop = False
    if not (p is None) and p != "" and not os.path.exists(p): drop = True
    if not (pn is None) and pn != "" and os.path.exists(pn): drop = True
    if not (ps is None) and ps != "":
        if len(glob(ps)) == 0: drop = True

    if drop:
        et, name = el.name, el.attrs.get("name", "")
        el.decompose()
        print("decompose %s named \"%s\"" % (et, name))


## process figure.myTable
pd.set_option('display.max_colwidth', -1)
for el in main.find_all("figure", {"class":"myTable"}):
    for e in el.find_all("table"): e.decompose() 

    p, name = el.attrs.get("data-file"), el.attrs.get("name", "")

    if p is None:
        print("not data-fille of figure.myTable: \"%s\"" % name)
        continue

    if not os.path.isfile(p):
        os.sys.exit("file not exist: " + p)

    print("fullfill figure.myTable \"%s\" with \"%s\"" % (name, p))
    d1 = pd.read_csv(p, sep="\t", index_col=0)
    idx = str(soup.new_string(d1.index.name))
    d1.index.name = None

    x = el.attrs.get("data-ncols")
    if not (x is None):
        try:
            y = int(x); d1 = d1.iloc[:, 0:y] ## not including index
        except:
            os.sys.exit("faild convert data-ncols to integer: " + x)

    x = el.attrs.get("data-nrows")
    if not (x is None):
        try:
            y = int(x); d1 = d1.iloc[0:y, :] ## not including header
        except:
            os.sys.exit("faild convert data-nrows to integer: " + x)

    x = el.attrs.get("data-xcols")
    if x is None:  ## split table in vertical
        k = d1.shape[1] ## k=6
    else:
        try:
            k = int(x)
        except:
            os.sys.exit("faild convert data-xcols \"%s\" to integer: " % x)

    if k < 1: k = d1.shape[1]
    n, m = divmod(d1.shape[1], k)
    if m > 0: n+=1

    for i in range(n):
       d2 = d1.iloc[:, (i*k):(i*k+k)]
       if d2.shape[1] == 0: continue

       t1 = BeautifulSoup(d2.to_html(na_rep=""), 'html5lib').find("table")
       t1.attrs = {}
       t1.find("th").append(idx)
       el.insert(i+2, t1)


## process figure.mySlide
for el in main.find_all("figure", {"class":"mySlide"}):
    if el is None: continue
    p, ps = el.attrs.get("data-file"), el.attrs.get("data-file-match")
    if p is None and ps is None: continue
    for e in el.find_all("img"): e.decompose()

    fs = []
    if not (p is None) and p != "": fs.extend(p.relpace(",", " ").split())

    if not (ps is None):
        for r in ps.replace(",", " ").split():
            for i in glob(r): fs.append(i)

    name = el.attrs.get("name", "")
    
    if len(fs) == 0:
        print("not image(s) for figure.mySilde \"%s\"" % name)
        continue

    for i in range(len(fs)):
        p = fs[i]
        if not os.path.isfile(p):
            os.sys.exit("image not found for \"%s\": \"%s\"" % (name, p))

        print("fullfill figure.mySilde \"%s\" with \"%s\"" % (name, p))
        el.insert(i, Tag(name="img", attrs={"src": p}))


## write html5
os.chdir(wd)
with open(out, "w") as f:
    content = Template(str(soup)).render(**dm)
    f.writelines(HTMLBeautifier.beautify(content, indent=2))

print("saved", out)
