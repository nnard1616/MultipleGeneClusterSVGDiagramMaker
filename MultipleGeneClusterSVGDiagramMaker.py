"""Written by Nathan Nard 20111206"""

import re
import sys
###Classes##########################
class Line(object):
  def __init__(self, ID, locus, position, regionSize, rStart, rEnd, seg1=[]):
    self.position = position #list in form of [x,y]
    self.seg1 = seg1 #list in form of [x,y]
    self.ID = ID # path1, path2, path3...
    self.locus = locus
    self.regionSize = regionSize #size of the dna region to be represented by the line
    self.rStart = rStart #start of region being diagrammed on locus
    self.rEnd = rEnd #end of region being diagrammed on locus

class Arrow(object):
  def __init__(self, ID, locus, start, end, rStart, rEnd, complement, yLoc = 0, regionSize = 0, diagramSize = 0, position=[], seg1=[], seg2=[], seg3=[], seg4=[], seg5=[], seg6=[]):
    self.position = position #list in form of [x,y]
    self.seg1 = seg1 #list in form of [x,y]
    self.seg1 = seg2 #list in form of [x,y]
    self.seg1 = seg3 #list in form of [x,y]
    self.seg1 = seg4 #list in form of [x,y]
    self.seg1 = seg5 #list in form of [x,y]
    self.seg1 = seg6 #list in form of [x,y]
    self.ID = ID #rect + oid
    self.locus = locus
    self.complement = complement #either + or -
    self.start = start #starting place on locus
    self.end = end #ending place on locus
    self.regionSize = regionSize
    self.yLoc = yLoc
    self.rStart = rStart #start of region being diagrammed on locus
    self.rEnd = rEnd #end of region being diagrammed on locus


  

###Functions#########################
def draw_line(line, svg): #takes line object as argument, and draws it onto svg 
  #svg is the file to which the following will be written to.
  svg.write('    <path\n')
  svg.write('       style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none"\n')
  svg.write('       d="m '+ str(line.position[0]) +','+ str(line.position[1]) + ' ' + str(line.seg1[0]) + ',' + str(line.seg1[1]) + '"\n')
  svg.write('       id="'+line.ID+'"\n')
  svg.write('       inkscape:connector-curvature="0"\n')
  svg.write('       sodipodi:nodetypes="cc" />\n')
  return

def draw_arrows(arrowList, num, svg): #takes list of arrow objects as argument, and draws it onto svg
  
  for arr in arrowList:
    
    xtot = float(int(arr.end) - int(arr.start))/int(arr.regionSize)*int(arr.diagramSize)
    ahw = 50.0/(2*1.618) #arrow head width
    shoulder = 50.0/(2.618*2)
    if arr.complement == "+":
      location = str(round(80.0 + float(int(arr.end))/int(arr.rEnd)*int(arr.diagramSize), 5)) + "," + str(arr.yLoc)
      
      sizeCorrection = 0
      shaftLength = xtot - ahw
      if shaftLength <= 2:
        sizeCorrection = 2-(shaftLength)
        shaftLength = 2
        
      seg1 = str(round(-1*(ahw-sizeCorrection), 5)) + ",25"
      seg2 = "0," + str(round(-1*shoulder, 5))
      seg3 = str(round(-1*(shaftLength), 5)) + ",0"
      seg4 = "0," + str(round(-1*(50-shoulder), 5))
      seg5 = "" + str(round(shaftLength, 5)) + ",0"
      seg6 = "0," + str(round(-1*shoulder))

      if sizeCorrection >= 15:
        seg1 = "-1,25"
        seg3 = "-1,0"
        seg5 = "1,0"

    elif arr.complement == "-":


      location = "" + str(round(80.0 + float(int(arr.start))/int(arr.rEnd)*int(arr.diagramSize), 5)) + "," + str(arr.yLoc)

      sizeCorrection = 0
      shaftLength = xtot - ahw
      if shaftLength <= 2:
        sizeCorrection = 2-(shaftLength)
        shaftLength = 2
     
      
      seg1 = str(round(ahw-sizeCorrection, 5)) + ",-25"
      seg2 = "0," + str(round(shoulder, 5))
      seg3 = str(round((shaftLength), 5)) + ",0"
      seg4 = "0," + str(round((50-shoulder), 5))
      seg5 = str(round(-1*(shaftLength), 5)) + ",0"
      seg6 = "0," + str(round(shoulder))

      if sizeCorrection >= 15:
        seg1 = "1,-25"
        seg3 = "1,0"
        seg5 = "-1,0"
        
    svg.write('    <path\n')
    svg.write('      style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none"\n')
    svg.write('       d="m ' + str(location) + ' ' + seg1 + ' ' + seg2 + ' ' + seg3 + ' ' + seg4 + ' ' + seg5 + ' ' + seg6 + ' z"\n')
    svg.write('       id="' + str(arr.ID) + '-' + str(num) + '"\n')
    svg.write('       inkscape:connector-curvature="0"\n')
    svg.write('       sodipodi:nodetypes="cccccccc" />\n')
  return


def main():
  if len(sys.argv) < 2 or len(sys.argv) >2:
    print "error, please type 'python svgWriter.py <mjn filename>'"
  else:
    ###Begin writing svg file
    try:
      mjn =  open(sys.argv[1], "r")
      lines = mjn.readlines()
      mjn.close()
    except:
      print "error: file does not exist, did you type file name in correctly?"
      return
    if sys.argv[1][-4:] != ".mjn":
      print "error: please be sure to include the file extension, '.mjn', at the end of the mjn filename"
      return
    countClusters = 0
    countRegion = 0
    for line in lines:
      if line.find("//") != -1:
        countClusters += 1
      if line.find("Region:") != -1:
        countRegion += 1
    if countClusters != countRegion:
      print "Mjn file is not formatted correctly.  Make sure to separate clusters with '//' and to make the second line of each cluster \"Region:<start>..<end>\""
      return

    docname = sys.argv[1][:-4] + ".svg"
    svg = open(docname,"w")

    svg.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    svg.write('<!-- Created By Nate -->\n')
    svg.write("\n")


    tWidth = '1560'
    tHeight = str(100*(countClusters+1))

    svg.write('<svg\n')
    svg.write('   xmlns:svg="http://www.w3.org/2000/svg"\n')
    svg.write('   xmlns="http://www.w3.org/2000/svg"\n')
    svg.write('   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n')
    svg.write('   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n')
    svg.write('   width="'+tWidth+'"\n')
    svg.write('   height="'+tHeight+'"\n')
    svg.write('   id="svg4789"\n')
    svg.write('   version="1.1"\n')
    svg.write('   inkscape:version="0.48.2 r9819"\n')
    svg.write('   sodipodi:docname="'+docname+'">\n')

    svg.write('  <defs\n')
    svg.write('     id="defs4791" />\n')
    svg.write('  <sodipodi:namedview\n')
    svg.write('     id="base"\n')
    svg.write('     pagecolor="#ffffff"\n')
    svg.write('     bordercolor="#666666"\n')
    svg.write('     borderopacity="1.0"\n')
    svg.write('     inkscape:pageopacity="0.0"\n')
    svg.write('     inkscape:pageshadow="2"\n')
    svg.write('     inkscape:zoom="0.84852814"\n')
    svg.write('     inkscape:cx="746.41462"\n')
    svg.write('     inkscape:cy="-142.34502"\n')
    svg.write('     inkscape:current-layer="svg4789"\n')
    svg.write('     inkscape:document-units="px"\n')
    svg.write('     showgrid="false"\n')
    svg.write('     inkscape:window-width="1440"\n')
    svg.write('     inkscape:window-height="838"\n')
    svg.write('     inkscape:window-x="-8"\n')
    svg.write('     inkscape:window-y="-8"\n')
    svg.write('     inkscape:window-maximized="1" />\n')

    svg.write('  <g\n')
    svg.write('     id="layer1"\n')
    svg.write('     inkscape:label="Layer 1"\n')
    svg.write('     inkscape:groupmode="layer">\n')

    ###Algorithm that draws all arrows and lines, makes use of the classes and functions defined above
    clusterArrows = {}
    clusterLines = {}
    count = 0
    arrows = []
    sizes = []
    for line in lines:
      try:
        if line != locus and (line.find("Region:") == -1) and (line.find("//") == -1):


          sline = line.split()
          if len(sline) > 4 or len(sline) <4:
            print "gene specifications do not appear to be formatted correctly.  Make sure they follow the format : <geneID> <geneStart> <geneEnd> <Strand>, separated by tabs"
            print "Please do not use spaces in gend ID's"
            return

          if sline[-1] != "-" and sline[-1] != "+":
            print "Be sure to use either + or - to indicate which strand are the genes on"
            return
          if int(sline[1]) < int(rStart) or int(sline[2]) > int(rEnd):
            print "error: Be sure to check that all genes are within the cluster regions specified in the mjn file."
            return
          arr = Arrow("rect" + sline[0], locus, sline[1], sline[2], rStart, rEnd, sline[3])
          arr.regionSize = int(regionSize)
          arr.yLoc = yLoc
          arrows.append(arr)

          
        if line.find("//") != -1:

          clusterArrows[locus] = arrows

          arrows = []
               
          del locus
          
      except:
        count += 1
        if count == countClusters +1:
          break
        locus = line.split()[0]
        if len(line.split()) > 1:
          print "Mjn file is not formatted correclty.  Please do not use spaces in cluster titles and make sure to use numbers to indicated start and end of genes."
          return
        try:
          rStart, rEnd = re.findall("[0-9]+", lines[lines.index(line)+1])[0], re.findall("[0-9]+", lines[lines.index(line)+1])[1]
        except:
          print "mjn file does not appear to be formatted correctly, please double check region specifications for each cluster are correclty formatted"
          return
        regionSize = str(int(rEnd) - int(rStart))
            
        sizes.append(int(regionSize))
        yLoc = 50+100*(count-1)
        try:
          clusterLines[locus]
          print "please use unique cluster ID's"
          return
        except:
          clusterLines[locus] = Line(locus, locus, [50, yLoc], regionSize, rStart, rEnd)





    maxSize = max(sizes)



    for locus in clusterLines:
      clusterLines[locus].seg1= [round((float(int(clusterLines[locus].regionSize))/maxSize*1400)+60, 5), 0]
      draw_line(clusterLines[locus], svg)
      for arr in clusterArrows[locus]:
        arr.diagramSize = round(float(int(clusterLines[locus].regionSize))/maxSize*1400, 5)

    num = 0
    for locus in clusterArrows:
      num +=1
      draw_arrows(clusterArrows[locus], num, svg)

    #next chunk draws the scale

    svg.write('    <path\n')
    svg.write('       style="fill:none;stroke:#000000;stroke-width:2.5;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none"\n')
    svg.write('       d="m 1510,'+ str(int(tHeight) - 50) + ' ' + str(-1*(2000.0/int(maxSize)*1460)) + ',0"\n')
    svg.write('       id="anchor"\n')
    svg.write('       inkscape:connector-curvature="0"\n')
    svg.write('       sodipodi:nodetypes="cc" />\n')
    svg.write('    <text\n')
    svg.write('       xml:space="preserve"\n')
    svg.write('       style="font-size:40px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"\n')
    svg.write('       x="1425.1443"\n')
    svg.write('       y="838.14221"\n')
    svg.write('       id="text3046"\n')
    svg.write('       sodipodi:linespacing="125%"><tspan\n')
    svg.write('         sodipodi:role="line"\n')
    svg.write('         x="1425.1443"\n')
    svg.write('         y="838.14221"\n')
    svg.write('         id="tspan3050">2kbp</tspan></text>\n')
      
    svg.write('  </g>\n')
    svg.write('</svg>\n')
    svg.close()


if __name__ == '__main__':
  main()

