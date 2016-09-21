
import re
import string
import datetime
from bs4 import BeautifulSoup, element
from . models import DecisionBibliographyModel
from . EpoSearchFacade import EpoSearchFacade

class EpoConverter(object):
    """
    Functions for converting responses from EPO Search to useful data
    """

    CASENUMBERFINDER = r'([DGJRTW][_ ]\d{4}/\d{2})'


    def ResponseToDecisionList(self, response):
        responsesPerCase = self._splitRespnsePerCase(response)
        decisionList = []
        for case in responsesPerCase:
            decisionList.append(self._singleresponseToBibliography(case))
        return decisionList

    def _splitRespnsePerCase(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.find_all('r')
        return result

    def _singleresponseToBibliography(self, single_response): 
        if not single_response:
            return   

        result = self._extractFromMeta(single_response)        
        return result


    # may contain duplicates
    def _responseToCaseList(self, response):
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all('r')
        decisionList = []
        finder = re.compile(self.CASENUMBERFINDER)
        for res in results:
            caseString = res.t.string
            found = re.search(finder, caseString)
            if found:
                decisionList.append(found.group(1))
        return decisionList

    
    # delete _metaToBibliography if we decide to keep _metatoBibliographyList?
    def _metaToBibliography(self, response):    
        soup = BeautifulSoup(response.text, "html.parser")

        #Get proceedings case number 
        #And create or update a decision
        caseNumber = self._parseMeta(soup, 'dg3CSNCase')
        procedureLanguage = self._parseMeta(soup, 'dg3DecisionPRL')
        decision = DecisionBibliographyModel.objects.create_or_update(caseNumber)
    
        if decision is None: #will happen if we cannot extract a usable caseNumber
            return decision

        #Find a result that has the decision in the procedure language
        theResult = None
        results = soup.find_all("r")
        for res in results:
            decisionLanguage = self._parseMeta(res, 'dg3DecisionLang')
            if decisionLanguage == procedureLanguage:
                theResult = res
                break

        if theResult is None:
            theResult = results[0]  # no decision in the language of proceedings? Weird. Take whatever is first
         
        decision = self._extractFromMeta(theResult)
        return decision
    

    def _extractFromMeta(self, tag):
        metaDictionary = self._parseToMetaDictionary(tag)
        decision = DecisionBibliographyModel.objects.Find_or_create(**metaDictionary)
        return decision


    def _parseToMetaDictionary(self, tag):
        ddate = self._parseMeta(tag, 'dg3DecisionDate')
        odate = self._parseMeta(tag, 'dg3DecisionOnline')

        hw = self._parseMeta(tag, 'DC.title')
        finder = re.compile(r'\((.*)\)')
        found = re.search(finder, hw)
        if found:
            hw = found.group(1)
        else:
            hw = ""

        metaDictionary = {
            'CaseNumber': self._parseMeta(tag, 'dg3CSNCase'),
            'DecisionDate': datetime.datetime.strptime(ddate, '%d.%m.%Y'),       
            'OnlineDate': datetime.datetime.strptime(odate, '%d.%m.%Y'),
            'DecisionLanguage': self._parseMeta(tag, 'dg3DecisionLang'), 
            'Applicant': self._parseMeta(tag, 'dg3Applicant'),
            'Opponents': self._parseMeta(tag, 'dg3Opponent'),
            'ApplicationNumber': self._parseMeta(tag, 'dg3APN'),
            'IPC': self._parseMeta(tag, 'dg3CaseIPC'),
            'Title': self._parseMeta(tag, 'dg3TLE'),
            'Headword': hw,
            'Board': self._parseMeta(tag, 'dg3DecisionBoard'),
            'Keywords': self._parseMeta(tag, 'dg3KEY'),
            'Articles': self._parseMeta(tag, 'dg3ArtRef'),
            'Rules': self._parseMeta(tag, 'dg3RuleRef'),
            'ECLI': self._parseMeta(tag, 'dg3ECLI'),
            'CitedCases': self._parseMeta(tag, 'dg3aDCI'),
            'Distribution': self._parseMeta(tag, 'dg3DecisionDistributionKey'),
            'ProcedureLanguage': self._parseMeta(tag, 'dg3DecisionPRL'),
            'PDFLink': self._parseMeta(tag, 'dg3DecisionPDF'),
            'Link' + self._parseMeta(tag, 'dg3DecisionLang'): tag.u.string,
            }        

        return metaDictionary

            
    def _parseMeta(self, soup, name):
        tag = soup.find('mt', {'n':name})
        if not tag:
            return ""

        v = tag['v'].strip(string.whitespace)
        w = v.strip(string.punctuation + string.whitespace)
        if w == "":
            return w
        else:
            return v

    #region Text extraction  - not yet re-worked
    def TextToDecision(self, response, caseNumber, procedureLanguage):
    
        textDictionary = self._parseToTextDictionary(response)
        decision = DecisionBibliographyModel.objects.create_or_update(caseNumber, **textDictionary)
        return decision


    def _loopToHeader(self, textList, para):
        while para:
            textList.append(para)
            para = para.nextSibling
            if para:
                nextSib = para.nextSibling
                if not nextSib or nextSib.find('b'):    
                    textList.append(para)                    
                    return textList
                else:
                    pass # there is still at least one <p>
            else:
                return textList # we have just dealt with the last <p>   


    def _parseToTextDictionary(self, response):        
        soup = BeautifulSoup(response.content, "html.parser")

        textSection = soup.find('div', {'id':'body'})
        if not textSection:
            return

        # strip out all tags other than <p>
        for tag in textSection.children:
            if isinstance(tag, element.Tag):
                if not tag.name == 'p':
                    tag.decompose()
            elif tag.string == '\n':
                del tag


        # Now, textSection is a <div/> that contains the facts, reaons, order, 
        # or whatever they are called in our decision.
        # Try to find the secions by looking for <b> tags
                
        headers = textSection.find_all('b')
        if not len(headers) == 3:
            parseDictionary = {
                'FactsHeader': "See Reasons",
                'Facts':  "",
                'ReasonsHeader': "",
                'Reasons': self._parasToString(textSection.find_all('p')),
                'OrderHeader': "See Reasons",
                'Order': "",
                'TextDownloaded': True,
                'HasSplitText': False,
                }          
        
        else:
            parseDictionary = {
                'FactsHeader': headers[0].string,
                'Facts': self._parasToString(_loopToHeader([], headers[0].parent.nextSibling)),
                'ReasonsHeader': headers[1].string,
                'Reasons': self._parasToString(_loopToHeader([], headers[1].parent.nextSibling)),
                'OrderHeader': headers[2].string,
                'Order': self._parasToString(_loopToHeader([], headers[2].parent.nextSibling)),
                'TextDownloaded': True,
                'HasSplitText': True,
                }

        return parseDictionary


    def _parasToString(self, paraList):                
            text = "\n\n".join(para.string.strip() for para in paraList if not para.string.strip(string.whitespace + string.punctuation) == "")
            return text  
    #endregion      
    

