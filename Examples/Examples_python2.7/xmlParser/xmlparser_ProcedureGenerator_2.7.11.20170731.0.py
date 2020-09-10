
import xml.sax
import sys; print(sys.version)


class Device( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.consolePartNumber = ""
      self.BuildModelString = ""
      self.equipmentType = ""
      self.TypeName = ""
      self.Enabled = ""
      
      
   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "Config":
         print "*******Part Inspection Procedure*******, \n"
      elif tag == "FeatureItem":
         print "*******Feature Items********, \n"
         feature = attributes["xsi:type"]
         print "Feature:", feature

   # Call when an elements ends
   def endElement(self, tag):
      if self.CurrentData == "consolePartNumber":
         print "Part Number:", self.consolePartNumber, "\n"
      elif self.CurrentData == "BuildModelString":
         print "Description:", self.BuildModelString, "\n"
      elif self.CurrentData == "equipmentType":
         print "Product Type:", self.equipmentType, "\n"
      elif self.CurrentData == "TypeName":
         print "Display Type:", self.TypeName, "\n"
      elif self.CurrentData == "Enabled":
         print "Enabled:", self.Enabled, "\n"
      self.CurrentData = ""

   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "consolePartNumber":
         self.consolePartNumber= content
      elif self.CurrentData == "BuildModelString":
         self.BuildModelString = content
      elif self.CurrentData == "equipmentType":
         self.equipmentType = content
      elif self.CurrentData == "TypeName":
         self.TypeName = content
      elif self.CurrentData == "Enabled":
         self.Enabled = content
  
  
if ( __name__ == "__main__"):

   # enter the .xml file name
   filename = raw_input("Enter File Name:\n")
      
   # create an XMLReader
   parser = xml.sax.make_parser()
   
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   
   # override the default ContextHandler
   Handler = Device()
   parser.setContentHandler( Handler )
   
   parser.parse(filename)
