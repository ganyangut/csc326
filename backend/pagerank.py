# Copyright (C) 2011 by Peter Goodman
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

def page_rank(document_index, num_iterations=20, initial_pr=1.0):
    from collections import defaultdict
    import numpy as np

    page_rank = defaultdict(lambda: float(initial_pr))
    num_outgoing_links = defaultdict(float)
    incoming_link_sets = defaultdict(set)
    incoming_links = defaultdict(lambda: np.array([]))
    damping_factor = 0.85

    for doc_id in document_index:
        # convert each set of incoming links into a numpy array
        if document_index[doc_id].incoming_links_set != None:
            incoming_links[doc_id] = np.array([from_doc_id for from_doc_id in document_index[doc_id].incoming_links_set])
        # collect the number of outbound links for every document
        if document_index[doc_id].outgoing_links_set != None:
            num_outgoing_links[doc_id] = len(document_index[doc_id].outgoing_links_set)

    num_documents = float(len(num_outgoing_links))
    lead = (1.0 - damping_factor) / num_documents
    partial_PR = np.vectorize(lambda doc_id: page_rank[doc_id] / num_outgoing_links[doc_id])

    for _ in xrange(num_iterations):
        for doc_id in num_outgoing_links:
            tail = 0.0
            if len(incoming_links[doc_id]):
                tail = damping_factor * partial_PR(incoming_links[doc_id]).sum()
            page_rank[doc_id] = lead + tail
    
    return page_rank

if __name__ == "__main__":
    #print page_rank([(1,2), (2, 4), (4, 3)])
    #print page_rank([(1,2), (2, 4), (4, 3), (3, 1), (3, 2)])
    #defaultdict(<function <lambda> at 0x7f781f91e140>, {1: 0.05000000000000001, 2: 0.09250000000000003, 4: 0.12862500000000002})
    #defaultdict(<function <lambda> at 0x7f781f91e140>, {1: 0.1566791857202851, 2: 0.2898564935825274, 3: 0.2791899914185817, 4: 0.2838780195451483})
