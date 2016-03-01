# Python file solrconverter.py
"""
So as it turns out, in a xml file for Solr we have to add a few more tags,
and, we also have to name every document tag field and have its name
attribute be the name of the field... well I think this is rather backwards
from how at least I think about markup, the name is the tag's name, not an
attribute called name. Therefore I am going to create this converter rather
than modifying the scrapers I already have.

Therefore this is going to take a document and turn it into an XML file
useable by Solr for indexing.

As such it needs to be of the following form:

<add>
<doc>
    <field name="...">...</field>
    <....
</doc>
</add>

We will use the StructuredDocument class as well as xmlextractor
"""
from markupcreator import StructuredDocument
from xmlextractor import XMLExtractor
import os

# this should convert from a structured document to one that is in the above
# format where each node (at the top level) is converted to field with name=
# Name of the node
def convertToSolr(document, new_document_directory):
    new_document = StructuredDocument(new_document_directory)
    # first we start the add and doc nodes
    new_document.CreateNode('add')
    new_document.FinishNode(True)
    new_document.CreateChild('doc')
    new_document.FinishNode(True)
    # now we go through the nodes in document and create the fields
    for node in document.nodes:
        new_document.CreateChild('field')
        new_document.AddAttributes(name=node.name)
        new_document.AddContent(node.content)
        new_document.FinishNode()
    new_document.FinishChildren()
    new_document.FinishChildren()
    return new_document

def convertDirectory(directory):
    # we are going to create a solr directory and then
    # run through the input directory and convert everything
    # to the solr format and save it in the solr directory
    new_directory = directory + 'Solr'
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    extractor = XMLExtractor()
    for filename in os.listdir(directory):
        # first we extract the document into a StructuredDocument
        extractor.InputFile(directory + '/' + filename)
        extractor.CreateDocument()
        document = extractor.document
        # next we convert the document
        new_document = convertToSolr(document, new_directory)
        # now we export the file
        new_document.Export(filename)
