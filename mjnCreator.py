#
import os
import re
f = open("sagD-scaffolds-selected.gbk","r")
lines = f.readlines()
f.close()


scaffoldList = {
"APTF_contig10049": ["1", "6069"],
"CLOF_contig30738": ["1", "8377"],
"ACOFG987_contig19579": ["1", "4730"],
"ACOFG988_contig16625": ["1", "7036"],
"AECF_contig21270": ["1", "7329"],
"APTF_contig15600": ["1", "3896"],
"ACOFG987_contig46931": ["1", "8235"],
"ACEF_contig07455": ["1", "5948"]}

f = open("test.mjn", "w")
LocusSwitch = False
geneSwitch = False
for line in lines:
  sline = line.split()
  if (sline[0] == "LOCUS") and (len(sline) > 1):
    try:
      scaffoldList[sline[1]]
      f.write(sline[1] + "\n")
      LocusSwitch = True #remember to turn switch off
    except:
      continue

  if LocusSwitch:
    if (sline[0] == "CDS") and (len(sline) > 1):
      address = sline[1]
      geneSwitch = True
    elif (geneSwitch) and (line.find("/note=") != -1):
      oid = re.findall("[0-9]+", line)[0] #will return first object in list generated by re.findall.  example output of re.findall: ['2001399384']
    elif (geneSwitch) and (line.find(" "*21 + "/translation") != -1):
      geneSwitch = False
      start = re.findall("[0-9]+", address)[0]
      end = re.findall("[0-9]+", address)[1]
      if address.find("complement") != -1:
        comp = "-"
      else:
        comp = "+"
      try:
        print oid, start, end
        f.write(oid + "\t" + start + "\t" + end + "\t" + comp + "\n")
      except:
        continue
  if line == ("//\n"):
    LocusSwitch = False
    f.write("//\n")
f.close()
    
      
      
