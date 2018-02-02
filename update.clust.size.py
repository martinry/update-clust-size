#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

clusters = []
otus = {}
not_found = []


class Cluster(object):
    
    def __init__(self, row): #name, size, stype, top):
        
        identifier = line[0].split(';')
        self.name = identifier[0]
        self.size = int(identifier[1].replace('size=',''))
        self.stype = line[1]
        
        rel = line[2].split(';')
              
        if self.stype == 'OTU':
            self.top = None
        elif self.stype != 'OTU':
            self.top = rel[1].replace('top=','')
  
    
if __name__ == '__main__':
    up_file_name = sys.argv[1]
    
    with open(up_file_name, 'r') as up:
        for line in up:
            line = line.strip()
            line = line.split() 
            
            clust = Cluster(line)
            clusters.append(clust)

for clust in clusters:
    if clust.stype == 'OTU':
        otus[clust.name] = clust.size

for clust in clusters:
    if clust.stype == 'match':
        if clust.top in otus.keys():
            otus[clust.top] += clust.size
        else: not_found.append(clust.top)

### Perfect chimeras
#for clust in clusters:
#    if clust.name in not_found:
#        print(clust.name, clust.size, clust.stype)

up_file_name = up_file_name.replace('.up', '')
fixed_rank_filename = up_file_name + '.fixedRank'
output_file_name = up_file_name + '.update.fixedRank'

fw = open(output_file_name, 'w')
with open(fixed_rank_filename, 'r') as up:
    for line in up:
        line = line.strip()
        line = line.split()
        splitline = (line[0].split(';'))
        otu = splitline[0]
        updated = '%s;size=%d;\t' % (otu, otus[otu])
        x = '\t'.join(map(str,(line[1:])))
        y = (updated + '\t' + x)
        fw.write(y)
        fw.write('\n')
fw.close()
