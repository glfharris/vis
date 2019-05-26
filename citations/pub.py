import requests as r

## GET https://www.ebi.ac.uk/europepmc/webservices/rest/src/ext_id/citations/[page]/[pageSize]/[format]/[callback]
## GET https://www.ebi.ac.uk/europepmc/webservices/rest/src/ext_id/references/[page]/[pageSize]/[format]/[callback]

class Publication:
    def __init__(self, pmid):
        self.pmid = pmid
        self.cites = []
        self.got_cites = False
        self.references = []
        self.got_refs = False
        self.title = ""
        self.pub_year = 0
        self.jrnl = ""
        self.distance = 0

    def get_meta(self):
        data = r.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ext_id:" + str(self.pmid) + "%20src:med&format=json").json()
        self.pub_year = data['resultList']['result'][0]['pubYear']
        self.jrnl = data['resultList']['result'][0]['journalTitle']
        self.title = data['resultList']['result'][0]['title']
    
    def get_citations(self):
        results = []
        page_num = 1
        while True:
            data = r.get('https://www.ebi.ac.uk/europepmc/webservices/rest/MED/' + str(self.pmid) + '/citations/'+ str(page_num) + '/100/json').json()
            if len(data['citationList']['citation'])> 0:
                for x in data['citationList']['citation']:
                    tmp = Publication(x['id'])
                    tmp.title = x['title']
                    try:
                        tmp.pub_year = x['pubYear']
                        tmp.jrnl = x['journalAbbreviation']
                    except:
                        pass
                    tmp.distance = self.distance + 1
                    self.cites.append(tmp.pmid)
                    results.append(tmp)
                page_num += 1
            else:
                break
        self.got_cites = True
        return results

    def get_references(self):
        results = []
        page_num = 1
        while True:
            data = r.get('https://www.ebi.ac.uk/europepmc/webservices/rest/MED/' + str(self.pmid) + '/references/'+ str(page_num) + '/100/json').json()
            if len(data['referenceList']['reference'])> 0:
                for x in data['referenceList']['reference']:
                    if 'id' in x.keys():
                        tmp = Publication(x['id'])
                        tmp.title = x['title']
                        try:
                            tmp.pub_year = x['pubYear']
                            tmp.jrnl = x['journalAbbreviation']
                        except:
                            pass
                        tmp.distance = self.distance + 1
                        self.references.append(tmp.pmid)
                        results.append(tmp)
                page_num += 1
            else:
                break
        self.got_refs = True
        return results
    
    def node_dict(self):
        return {
            'title': self.title,
            'id': self.pmid,
            'journal': self.jrnl,
            'distance': self.distance,
            'year': self.pub_year
        }
    
    def link_dicts(self):
        links = []
        for x in self.cites:
            links.append({'source': x, 'target': self.pmid})
        for x in self.references:
            links.append({'source': self.pmid, 'target': x})
        return links

if __name__ == '__main__':
    
    pub = Publication(19620960)
    pub.get_references()
    print(pub.references)