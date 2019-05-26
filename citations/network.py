from pub import Publication

import json

def gen_network(pmid, radius=1):
    
    net = []
    orginial = Publication(pmid)
    orginial.get_meta()
    orginial.origin = True
    net.append(orginial)

    complete = False

    while not complete:
        complete = True
        for pub in net:
            if pub.distance <= radius and (pub.got_cites == False or pub.got_refs == False):
                print("Getting Results for: " + pub.title + ' - ' + str(pub.pmid))
                try:
                    net = merge_node_lists(net, pub.get_references())
                except:
                    print("Failed to get references for " + str(pub.pmid))
                try:
                    net = merge_node_lists(net, pub.get_citations())
                except:
                    print("Failed to get citations for " + str(pub.pmid))
                complete = False
    return net

def merge_node_lists(a, b):
    a_pmids = [x.pmid for x in a]
    b_pmids = [x.pmid for x in b]

    overlap = set(a_pmids).intersection(b_pmids)
    diff = set(a_pmids).symmetric_difference(b_pmids)

    a_dict = {}
    for pub in a:
        a_dict[pub.pmid] = pub

    b_dict = {}
    for pub in b:
        b_dict[pub.pmid] = pub

    for pub in b:
        if pub.pmid in overlap:
            orig = a_dict[pub.pmid]
            orig.cites += pub.cites
            orig.references += pub.references
            orig.distance = min(orig.distance, pub.distance)
        else:
            a_dict[pub.pmid] = pub
    
    return list(a_dict.values())

def output_graph(net):
    data = {'nodes': []}
    tmp = []
    for x in net:
        data['nodes'].append(x.node_dict())
        tmp += x.link_dicts()
    
    links = []
    for link in tmp:
        if link not in links:
            links.append(link)
    data['links'] = links

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    net = gen_network('19620960', radius=0)
    output_graph(net)
    print(len(net))