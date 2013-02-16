import urllib2
from Bio.Phylo import Newick
import os
import tarfile


col_delimiter = '\t|\t'
row_delimiter = '\t|\n'

# download the taxonomy archive
url = 'ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz'
filename = url.split('/')[-1]
if os.path.exists(filename):
    print 'Using existing copy of %s' % filename
else:
    print 'Downloading %s...' % filename
    r = urllib2.urlopen(urllib2.Request(url))
    assert r.geturl() == url
    with open(filename, 'wb') as output_file:
        output_file.write(r.read())
    r.close()

# extract the text dump
for filename in ('nodes.dmp', 'names.dmp'):
    if os.path.exists(filename):
        print 'Using existing copy of %s' % filename
    else:
        print 'Extracting %s...' % filename
        archive = tarfile.open(name=filename, mode='r:gz')
        archive.extract(filename)

# get names for all tax_ids from names.dmp
scientific_names = {}
common_names = {}
with open('names.dmp') as names_file:
    for line in names_file:
        line = line.rstrip(row_delimiter)
        values = line.split(col_delimiter)
        tax_id, name_txt, _, name_type = values[:4]
        if name_type == 'scientific name':
            scientific_names[tax_id] = name_txt
        elif name_type == 'common name':
            common_names[tax_id] = name_txt

# create tree from nodes.dmp
