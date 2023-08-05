import subprocess
import os
from datapungi_imf.utils import getUserSettings


def runTests(outputPath='',testsPath='',verbose = True):
    if not testsPath:
       testsPath =  os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
       print('**************************** \nWill run tests in: ' + testsPath)
    if not outputPath:
        outputPath = "U:/"
        try:
            settingsFile = getUserSettings()
            outputPath = settingsFile['TestsOutputPath']
        except:
            print("Could not load TestOutputPath from user settings.  Perhaps run util.setTestFolder( FilePath )  ")
    subprocess.Popen('pytest ' + testsPath + ' --html='+outputPath+'datapungi_imf_Tests.html --self-contained-html')
    if verbose:
        print('Tests will be saved in '+outputPath+'datapungi_imf_Tests.html \n****************************')

if __name__ == '__main__':
    from sys import argv    
    import subprocess
    import os 
    
    runTests()