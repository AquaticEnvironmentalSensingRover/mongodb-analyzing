'''
closestSonar(dDepth, dTime, time)
function: cycle through dTime until the closest value to time is found, record index, use index to find the corresponding depth value from dDepth, add to an array time and depth to separate arrays
that will be return
repeat 5 times and return the arrays
outside of function: append depth and time into 2 new arrays that will be plotted
'''

def closestSonar(timeData, depthData, time):
    finalDepth = []
    finalTime = []
    
    #print (size(timeData))
    #print (size(depthData))
    #print (size(time) )
    
    for index in range(5):
        minTime = None
        index = 0
        for indexInner, ii in enumerate(timeData):
            if not minTime == None:
                if (checkVal(finalTime, ii) and abs(minTime-time) > abs(ii-time)):
                    minTime = ii
                    index = indexInner
                    
            else:
                minTime = ii
               
        finalTime.append(minTime)
        finalDepth.append(depthData[index]) 
        
    return (finalTime, finalDepth)
        
                
def checkVal(array, val):  
    
    for ii in array:
        if ii == val:
            return False
            
    return True
                