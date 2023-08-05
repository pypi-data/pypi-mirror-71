'''
   Base driver class
'''

import pandas as pd
import requests
import json
from copy import deepcopy
import pyperclip
import math
import re
import inspect
import yaml
import itertools
from datetime import datetime
import warnings
import functools
from textwrap import dedent
from datapungi_imf import generalSettings        #NOTE: projectName 
#import generalSettings        #NOTE: projectName 
from datapungi_imf import utils                  #NOTE: projectName  
#import utils                  #NOTE: projectName  

class driverCore():
    r'''
      Given a dbGroupName and its default db, starts a factory of query functions - ie, a function for 
      each db in the group.  If dbGroupName is empty, return the list of dbGroups, dbs in the group, and their parameters
    '''
    def __init__(self,dbGroupName='', baseRequest={},connectionParameters={},userSettings={}):  
        #TODO: place defaultQueryFactoryEntry in yaml
        self._dbParams, self.defaultQueryFactoryEntry  = self._getDBParameters(dbGroupName) 
        self._ETDB      = extractTransformDB(baseRequest,connectionParameters,userSettings) #a generic query is started
        self._ETFactory = extractTransformFactory(dbGroupName,self._ETDB,self._dbParams,self.defaultQueryFactoryEntry)
        #self._driverMeta = driverMetadata()(dbGroupName)
        self.__setdoc__(dbGroupName)
    
    def __getitem__(self,dbName):
        return(self._ETFactory.extractTransformFactory[dbName])
    
    def __call__(self,*args,**kwargs):
        out = self._ETFactory.extractTransformFactory[self.defaultQueryFactoryEntry](*args,**kwargs)
        return(out)
    
    def __setdoc__(self,dbGroupName):
        if dbGroupName == '':
            self.__doc__ = 'Returns the metadata of the dataset groups and their databases. Do not need inputs.'
        else:
            self.__doc__ = 'Queries the databases of {} \n \n'.format(dbGroupName)
            for entry in self.__docParams__: 
                self.__doc__ += '- {short name}: {description} \n'.format(**entry)
                self.__doc__ += '       parameters: {}\n'.format(str(entry['parameters']))
                self.__doc__ += '       official database name: {}\n'.format(entry['database'])
            self.__doc__ += '\nDefault query database: {}\n'.format(self.defaultQueryFactoryEntry) 
            self.__doc__ += "Sample functions: \n-data.{dbGroupName}() (default)  \n-data.{dbGroupName}['{db}']() (query the {db} database)".format(**{'dbGroupName':dbGroupName.lower(),'db':self.defaultQueryFactoryEntry})       
            self.__doc__ += "\n\nNOTE: don't need to pass most parameters.  Eg, api_key and file_type (json)."
    def __str__(self):
        return(self.__doc__)
           
    def _getDBParameters(self,dbGroupName = ''):
        r'''
          The parameters of each database in the group (if empty returns all groups x databases)
        '''  
        dataPath = utils.getResourcePath('/config/datasetlist.yaml')
        with open(dataPath, 'r') as yf:
            datasetlist = yaml.safe_load(yf)
        
        if dbGroupName == '':
            defaultDB = {}
            return((datasetlist,defaultDB))
        
        #get the entry of the group:
        selected = list(filter( lambda x: x['group'] == dbGroupName , datasetlist))[0]
        defaultDB = selected.get('default query','')
        datasets = selected.get('datasets',{})
        removeCases = lambda array: list(filter( lambda x: x not in ['api_key','file_type']  , array ))
        dbParams = { entry['short name'] : { 'urlSuffix' : entry['database'] , 'json key': entry['json key'], 'params': removeCases(entry['parameters']) } for entry in datasets }
        
        self.__docParams__ =  datasets #parameters used to write a doc string for the class instance.
        return((dbParams,defaultDB))


class extractTransformFactory():
    r'''
      given a groupName of databases, constructs dictionary of functions querying all of its databases
    '''
    def __init__(self,dbGroupName,ETDB,dbParams,defaultQueryFactoryEntry):
        if dbGroupName:
            self.dbGroupName = dbGroupName
            self.dbParams = dbParams
            self.ETDB = ETDB
            self.ETDB(self.dbGroupName,self.dbParams)  #update the connector to the databases with parameters specific to the collection of dbs.
            self.extractTransformFactory = { dbName : self.selectDBQuery(self.query, dbName)  for dbName in self.dbParams.keys() }
            self.defaultQueryFactoryEntry = defaultQueryFactoryEntry  #the entry in query factory that __call__ will use.
        else:
            self.extractTransformFactory = {}
    
    def query(self,*args,**kwargs):
        return( self.ETDB.query(*args,**kwargs) )
    
    def selectDBQuery(self,queryFun,dbName):
        r'''
          Fix a generic query to a query to dbName, creates a lambda that, from
          args/kwargs creates a query of the dbName 
        '''
        fun  = functools.partial(queryFun,dbName)
        lfun = lambda *args,**kwargs: fun(**self.getQueryArgs(dbName,*args,**kwargs))
        #add quick user tips
        lfun.options = self.dbParams[dbName]['params']
        return(lfun)
    
    def getQueryArgs(self,dbName,*args,**kwargs):
        r'''
          Map args and kwargs to driver args
        '''
        #paramaters to be passed to a requests query:
        paramArray = self.dbParams[dbName]['params']
        params = dict(zip(paramArray,args))
        paramsAdd = {key:val for key, val in kwargs.items() if key in paramArray}
        params.update(paramsAdd)
        #non query options (eg, verbose)
        otherArgs = {key:val for key, val in kwargs.items() if not key in paramArray}
        return({**{'params':params},**otherArgs})


class extractTransformDB():
    r'''
      Functions to connect and query a db given its dbName and dbParams (see yaml in config for these).
    '''
    def __init__(self,baseRequest={},connectionParameters={},userSettings={}):
        '''
          loads generic parametes (ie api key, location fo data.)
        '''
        self._connectionInfo = generalSettings.getGeneralSettings(connectionParameters = connectionParameters, userSettings = userSettings )
        self._baseRequest    = self.getBaseRequest(baseRequest,connectionParameters,userSettings)  
        self._lastLoad       = {}  #data stored here to assist functions such as clipcode 
        self._transformData  = transformExtractedData()   
        self._getCode        = transformIncludeCodeSnippet()  
        self._cleanCode      = ""  #TODO: improvable - this is the code snippet producing a pandas df
    
    def __call__(self,dbGroup,dbParams):
        r'''
         A call to an instance of the class Loads specific parameters of the dbs of dbGroup 
        '''
        self.dbGroup  = dbGroup
        self.dbParams = dbParams

    def query(self,dbName,params={},file_type='json',verbose=False,warningsOn=True):
        r'''
          Args:
            params
            file_type              
            verbose             
            warningsOn      
        '''
        # get requests' query inputs
        warningsList = ['countPassLimit']  # warn on this events.
        prefixUrl = self.dbParams[dbName]['urlSuffix']
        output = self.queryApiCleanOutput(prefixUrl, dbName, params, warningsList, warningsOn, verbose)
        return(output) 
     
    def queryApiCleanOutput(self,urlPrefix,dbName,params,warningsList,warningsOn,verbose):
        r'''
            Core steps of querying and cleaning data.  Notice, specific data cleaning should be 
            implemented in the specific driver classes

            Args:
                self - should containg a base request (url)
                urlPrefix (str) - a string to be appended to request url (eg, https:// ...// -> https//...//urlPrefix?)
                
                params (dict) - usually empty, override any query params with the entries of this dictionary
                warningsList (list) - the list of events that can lead to warnings
                warningsOn (bool) - turn on/off driver warnings
                verbose (bool) - detailed output or short output
        '''
        #get data 
        query = self.getBaseQuery(urlPrefix,params)
        retrivedData = requests.get(** { key:entry for key, entry in query.items() if key in ['params','url'] } )
        
        #clean data
        df_output,self._cleanCode = self.cleanOutput(dbName,query,retrivedData)
        
        #print warning if there is more data the limit to download
        for entry in warningsList:
            self._warnings(entry,retrivedData,warningsOn) 
        
        #short or detailed output, update _lastLoad attribute:
        output = self.formatOutputupdateLoadedAttrib(query,df_output,retrivedData,verbose)
        
        return(output)
    
    def getBaseQuery(self,urlPrefix,params):
        r'''
          Return a dictionary of request arguments.

          Args:
              urlPrefix (str) - string appended to the end of the core url (eg, series -> http:...\series? )
              dbName (str) - the name of the db being queried
              params (dict) - a dictionary with request paramters used to override all other given parameters
          Returns:
              query (dict) - a dictionary with 'url' and 'params' (a string) to be passed to a request
        '''
        query = deepcopy(self._baseRequest)
        
        #update query url -- in the IMF case all params will go to url
        query['url'] = query['url']+urlPrefix   
        if 'dbname' in params.keys():
            query['url'] += params['dbname']
        
        #query['params'].update(params)
        #query['params_dict'] = query['params']
        #query['params'] = '&'.join([str(entry[0]) + "=" + str(entry[1]) for entry in query['params'].items()])
        
        return(query)
    
    def formatOutputupdateLoadedAttrib(self,query,df_output,retrivedData,verbose):
        if verbose == False:
            self._lastLoad = df_output
            return(df_output)
        else:
            code = self._getCode.transformIncludeCodeSnippet(query,self._baseRequest,self._connectionInfo.userSettings,self._cleanCode)
            output = dict(dataFrame = df_output, request = retrivedData, code = code)  
            self._lastLoad = output
            return(output)
    
    def cleanOutput(self,dbName,query,retrivedData):
        r'''
         This is a placeholder - specific drivers should have their own cleaning method
         this generates self._cleanCode
        '''
        transformedOutput = self._transformData(self.dbGroup,dbName,self.dbParams,query,retrivedData)
        return(transformedOutput)
    
    def getBaseRequest(self,baseRequest={},connectionParameters={},userSettings={}):
        r'''
          Write a base request.  This is the information that gets used in most requests such as getting the userKey
        '''
        if baseRequest =={}:
           connectInfo = generalSettings.getGeneralSettings(connectionParameters = connectionParameters, userSettings = userSettings )
           return(connectInfo.baseRequest)
        else:
           return(baseRequest)
    
    def _warnings(self,warningName,inputs,warningsOn = True):
        if not warningsOn:
            return
        
        if warningName == 'countPassLimit':
            '''
              warns if number of lines in database exceeds the number that can be downloaded.
              inputs = a request result of a FED API 
            '''
            _count = inputs.json().get('count',1)
            _limit = inputs.json().get('limit',1000)
            if _count > _limit:
              warningText = 'NOTICE: dataset exceeds download limit! Check - count ({}) and limit ({})'.format(_count,_limit)
              warnings.warn(warningText) 


class transformExtractedData():
    def __call__(self,dbGroup,dbName,dbParams,query,retrivedData):
        #if dbGroup == 'Series':
        #    return( self.cleanOutputSeries(dbName,dbParams,query,retrivedData) )
        #else:
            return( self.cleanOutput(dbName,dbParams,query,retrivedData) )
      
    def cleanOutput(self, dbName, dbParams,query, retrivedData): #categories, releases, sources, tags
        dataKey = dbParams[dbName]['json key']
        cleanCode = "df_output =  pd.DataFrame( retrivedData.json()['{}'] )".format(dataKey)
        pdData = retrivedData.json()
        for entry in dataKey:
            pdData = pdData[entry]
        if dbName == 'list':
           return( self.cleanList(pdData) )
        if dbName == 'params':
            return(self.cleanParams(pdData))
        if dbName == 'data':
            return(self.cleanData(pdData))
        if dbName == 'meta':
            return(self.cleanMeta(pdData))
        warnings.filterwarnings("ignore", category=UserWarning)
        setattr(df_output, '_meta', dict(filter(lambda entry: entry[0] != dataKey, retrivedData.json().items())))  
        warnings.filterwarnings("always", category=UserWarning)
        return((df_output,cleanCode))
    
    def cleanList(self,preCleaned):
        cleanCode = "df_output = pd.DataFrame([ { 'id': entry['KeyFamilyRef']['KeyFamilyID'] , 'description':entry['Name']['#text'], 'language':entry['Name']['@xml:lang']} for entry in retrievedData.json()['Structure']['Dataflows']['Dataflow'] ])"
        df_output = [ { 'id': entry['KeyFamilyRef']['KeyFamilyID'] , 'description':entry['Name']['#text'], 'language':entry['Name']['@xml:lang']} for entry in preCleaned]
        df_output = pd.DataFrame(df_output)
        return((df_output,cleanCode)) 
    
    def cleanParams(self,preCleaned):   
        concepts = preCleaned.get('Concepts',{}).get('ConceptScheme',{}).get('Concept',[])
        concepts = pd.DataFrame([ {'id':entry.get('@id',''), 'text' : entry.get('Name',{}).get('#text','')}   for entry in concepts])
        
        annotations = preCleaned.get('KeyFamilies',{}).get('KeyFamily',{}).get('Annotations',{}).get('Annotation',[])
        annotations = pd.DataFrame([ {'title':entry.get('AnnotationTitle',''), 'text' : entry.get('AnnotationText',{}).get('#text','')}   for entry in annotations])
        
        codes =  preCleaned.get('CodeLists',{}).get('CodeList',[])
        codes =  {entry.get('@id',{}) : pd.DataFrame([ {'value': specs.get('@value',''), 'description' : specs.get('Description',{}).get('#text','') }  for specs in entry.get('Code',[])     ])  for entry in codes   }
        
        return((dict(concepts = concepts, annotations = annotations, codes = codes),''))
    
    def cleanData(self,preCleaned):
        df_output = pd.DataFrame.from_dict(preCleaned['Obs']) \
            .rename(columns={'@TIME_PERIOD':'date','@OBS_VALUE':'value'}) \
            .set_index('date') \
            .astype({'value':'float'})
        
        return((df_output,''))
    
    def cleanMeta(self,preCleaned):
        try:
            preCleaned = [entry.get('ReportedAttribute',entry) for entry in preCleaned]
            simplify = lambda x: {x['@conceptID']: x.get('Value',{}).get('#text',x) } if (isinstance(x,dict)) else {entry['@conceptID']: entry.get('Value',{}).get('#text','') for entry in x }
            preCleaned = [  [ simplify(x['ReportedAttribute']) for x in entry ] for entry in preCleaned ] #a list of (two) dicts
            preCleaned = [  {k: v for d in entry for k, v in d.items() } for entry in preCleaned  ]
        except:
            pass
        
        return((preCleaned,''))
    
    #def cleanOutputSeries(self, dbName, dbParams,query, retrivedData): #series
    #    dataKey = dbParams[dbName]['json key']
    #    cleanCode = "df_output =  pd.DataFrame( retrivedData.json()['{}'] )".format(dataKey)
    #    df_output = pd.DataFrame(retrivedData.json()[dataKey])  # TODO: deal with xml
    #    if dbName == 'observations':
    #        seriesID =  query['params_dict']['series_id'] #{ x.split('=')[0] : x.split('=')[1] for x in query['params'].split("&") }['series_id'] 
    #        df_output = df_output.drop(['realtime_end','realtime_start'],axis=1)
    #        df_output['date'] = pd.to_datetime(df_output['date'])
    #        df_output.set_index('date',inplace=True)
    #        df_output.value = pd.to_numeric(df_output.value,errors = 'coerse',downcast='integer') #NOTICE: downcast = float behaves oddly in GDP, default to float32 and introduce new digits.  integer will default to float64
    #        df_output = df_output.rename({'value':seriesID},axis='columns')
    #        cleanCode += "\ndf_output = df_output.drop(['realtime_end','realtime_start'],axis=1) "
    #        cleanCode += "\ndf_output['date'] = pd.to_datetime(df_output['date']) "
    #        cleanCode += "\ndf_output.set_index('date',inplace=True) "
    #        cleanCode += "\ndf_output.value = pd.to_numeric(df_output.value,errors = 'coerse',downcast='integer') "
    #        cleanCode += "\ndf_output = df_output.rename({ 'value' : "  + "'{seriesID}'".format(**{'seriesID':seriesID}) + "},axis='columns')"
    #        #TODO: relabel value column with symbol
    #    
    #    warnings.filterwarnings("ignore", category=UserWarning)
    #    setattr(df_output, '_meta', dict(filter(lambda entry: entry[0] != dataKey, retrivedData.json().items())))  
    #    warnings.filterwarnings("always", category=UserWarning)
    #    return((df_output,cleanCode))
 

class transformIncludeCodeSnippet():
    def transformIncludeCodeSnippet(self,query,baseRequest,userSettings={},pandasCode=""):      
        #load code header - get keys
        apiCode = self.getApiCode(query,userSettings)
        
        #load request's code
        queryCode = self.getQueryCode(query,baseRequest,pandasCode)
        
        return(apiCode + queryCode)
    
    def getQueryCode(self,query,baseRequest,pandasCode=""):
        queryClean = {'url':query['url'],'params':query['params']}  #passing only these two entries of query; params_dict is dropped.
        queryClean['url'] = 'url'
        queryClean['params']=queryClean['params'].replace(baseRequest['params']['api_key'],'{}')+'.format(key)'  #replace explicit api key by the var "key" poiting to it.
        
        queryCode = '''\
            query = {}
            retrivedData = requests.get(**query)
            
            {} #replace json by xml if this is the request format
        '''
        
        queryCode = dedent(queryCode).format(json.dumps(queryClean),pandasCode)
        queryCode = queryCode.replace('"url": "url"', '"url": url')
        queryCode = queryCode.replace('.format(key)"', '".format(key)')
        queryCode = queryCode.replace('"UserID": "key"', '"UserID": key')  #TODO: need to handle generic case, UserID, api_key...        
        return(queryCode)

    def getApiCode(self,query,userSettings): 
        r'''
          The base format of a code that can be used to replicate a driver using Requests directly.
        '''
        try:
            url = query['url']
            if userSettings:  
                apiKeyPath  = userSettings['ApiKeysPath']
                apiKeyLabel = userSettings["ApiKeyLabel"]
            else:
                userSettings = generalSettings.getGeneralSettings( ).userSettings['ApiKeysPath']
                apiKeyPath   = userSettings['ApiKeysPath']
                apiKeyLabel  = userSettings["ApiKeyLabel"]
        except:
            url        = " incomplete connection information "
            apiKeyPath = " incomplete connection information "
        #userSettings = utils.getUserSettings()
        #pkgConfig    = utils.getPkgConfig()
        storagePref  = apiKeyPath.split('.')[-1]
        
        passToCode = {'ApiKeyLabel': apiKeyLabel, "url":url, 'ApiKeysPath':apiKeyPath} #userSettings["ApiKeyLabel"]
        
        code = self.apiCodeOptions(storagePref)
        code = code.format(**passToCode)   
        
        return(code)
    
    def apiCodeOptions(self,storagePref):
        r''''
          storagePref: yaml, json, env
        '''
        if storagePref == 'yaml':
            code = '''\
                import requests
                import yaml 
                import pandas as pd
                
                apiKeysFile = '{ApiKeysPath}'
                with open(apiKeysFile, 'r') as stream:
                    apiInfo= yaml.safe_load(stream)
                    url,key = apiInfo['{ApiKeyLabel}']['url'], apiInfo['{ApiKeyLabel}']['key']
            '''
        elif storagePref == 'json':
            code = '''\
                import requests
                import json    
                import pandas as pd
                
                # json file should contain: {"IMF":{"key":"YOUR KEY","url": "{url}" }
                
                apiKeysFile = '{ApiKeysPath}'
                with open(apiKeysFile) as jsonFile:
                   apiInfo = json.load(jsonFile)
                   url,key = apiInfo['{ApiKeyLabel}']['url'], apiInfo['{ApiKeyLabel}']['key']    
            '''
        else: #default to env
            code = '''\
                import requests
                import os 
                import pandas as pd
                
                url = "{url}"
                key = os.getenv("{ApiKeyLabel}") 
            '''
        return(dedent(code))
    
    def clipcode(self):
        r'''
           Copy the string to the user's clipboard (windows only)
        '''
        try:
            pyperclip.copy(self._lastLoad['code'])
        except:
            print("Loaded session does not have a code entry.  Re-run with verbose option set to True. eg: v.drivername(...,verbose=True)")

if __name__ == '__main__':
    #case = driverCore(dbGroupName = 'list')
    #print(case())
    #case = driverCore(dbGroupName = 'params')
    #print(case('IFS'))
    #case = driverCore(dbGroupName = 'data')
    #print(case('IFS/A.GB.PMP_IX'))
    case = driverCore(dbGroupName = 'meta')
    print(case('IFS/A.BR.MFS'))
    #print(case('gdp',verbose=True))