#!/usr/bin/python

import xml.sax
validFeatures = ['UsbFeature', 'DmkFeature', 'Speedfeature', 'GradeFeature', 'Fanfeature', 'AudioFeature', 'PulseFeature', 'etc...']


class MovieHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.Enabled = ""

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "FeatureItem":
         print "*****FeatureItem*****, \n"
         feature = attributes["xsi:type"]
         if validfeatures == feature:
            print "Feature:", feature, "\n"            
            
   
   # Call when an elements ends
   def endElement(self, tag):
      if self.CurrentData == "Enabled":
         print "FeatureItem:", self.Enabled, "\n"
         self.CurrentData = ""

   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "Enabled":
         self.Enabled = content
      
  
if ( __name__ == "__main__"):

   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = MovieHandler()

   parser.setContentHandler( Handler )
   
   parser.parse("T22116xx.xml")

