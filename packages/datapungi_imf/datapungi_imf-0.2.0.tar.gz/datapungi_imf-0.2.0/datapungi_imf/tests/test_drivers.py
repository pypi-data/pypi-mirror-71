import datapungi_imf as dp 
import time
import pandas as pd
import os


def executeCode(stringIn):
    '''
      auxiliary function for tests: get the requests code as a string and try to execute it.
    '''
    try:
        exec(stringIn+'\n')      #exec('print("hi")') #
        return(dict( codeRun = True, codeOutput = locals()['df_output']   ))   #try to output the dataframe called df_output
    except:
        try:
            exec(stringIn)  #if no dataframe called output, try to see it at least can exec the code
            return(dict(codeRun = True, codeOutput = pd.DataFrame([])))
        except:
            return(dict(codeRun = False, codeOutput = pd.DataFrame([])))

# start  the driver - used by all tests
def startDriver(cmdopt):
    if not cmdopt == "":
        connectionParameters = {"key": cmdopt, "url": ""}
    else:
        connectionParameters = {}
    data = dp.data(connectionParameters)
    return(data)    

# content of test_sample.py
def test_startDriver(cmdopt):
    data = startDriver(cmdopt)
    assert data


###########################################################################################################
###  Tests of the categories dbgroup
                
def test_list  (cmdopt):
    data = startDriver(cmdopt)
    driver = data.clist (,verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  
                
def test_params  (cmdopt):
    data = startDriver(cmdopt)
    driver = data.cparams (,verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  
                
def test_data  (cmdopt):
    data = startDriver(cmdopt)
    driver = data.cdata (,verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  
                
def test_meta  (cmdopt):
    data = startDriver(cmdopt)
    driver = data.cmeta (,verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  



if __name__ == '__main__':
    pass