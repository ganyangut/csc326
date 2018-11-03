from data_structures import *
from pagerank import *


document_index = document_index()
document_index[1] = document()
document_index[2] = document()
document_index[4] = document()
document_index[3] = document()


document_index[1].incoming_links_set = None
document_index[1].outgoing_links_set = ([2])
document_index[2].incoming_links_set = ([1])
document_index[2].outgoing_links_set = ([4])
document_index[4].incoming_links_set = ([2])
document_index[4].outgoing_links_set = ([3])
document_index[3].incoming_links_set = ([4])
document_index[3].outgoing_links_set = None

print page_rank(document_index)