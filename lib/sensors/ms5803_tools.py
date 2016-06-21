''' Series of fuctions in order to analyze pressure sensor data '''

# returns altitude above sealevel in m
def altitude(pressure, temp):
    
    # pressure [Pa]
    P = pressure * 100.0
    
    # Measured temp [K]
    T = temp + 273.15
    
    # pressure at sealevel [Pa]
    P0 = 101325.0
    
    # altitude equation
    h = ((((P0/P)**(1/5.257)) - 1) * T) / 0.0065
    
    return h
    
def depth(pressure):
    
    # density of fluid [kg/m3]
    r = 1000.0
    
    # acceleration of gravity [m/s2]
    g = 9.81
    
    # pressure [Pa]
    P = pressure * 100.0
    
    # pressure of atmosphere [Pa]
    # Briyard Pond is at sealevel
    P0 = 101325.0
    
    # depth equation
    d = (P - P0) / (r * g)
    
    return d
        
    
    
    
    
    

    