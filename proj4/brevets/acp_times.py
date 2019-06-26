"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

open_table = [(1000,28),(600,30),(400,32),(200,34),(0,34)]
close_table = [(1000,11.428),(600,15),(400,15),(200,15),(0,15)]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    i = 0
    total_time = 0
    table_size = len(open_table)
    
    for i in range(table_size): #looks through the intervals of the tables
        dst = open_table[i][0] # looks for the proper distance 
        if control_dist_km >= dst: #compares the controlled distance in km to the distance through out the table so it can evenutally find proper speed
            #print(open_table[i][0])
            distance = control_dist_km - dst #finds out the different of the control distance and the last interval of the so we can eventually divide by the proper speed
            time = distance / open_table[i-1][1] #this is where it divide so we can find the time
            total_time += time #this gets the total time 
            control_dist_km -= distance  #this will continously keep updating the distance as it goes 

    brevet_start_time = arrow.get(brevet_start_time)
    hrs = int(total_time) 
    #print(hrs)
    mts = round(60*(total_time-hrs))
    #print(mts)
    opening_time = brevet_start_time.shift(hours=hrs,minutes=mts) #This will convert the hours and minutes into a proper time format    

    return opening_time.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    
    total_time = 0
    table_size = len(close_table)
    
    i = 0 
    for i in range(table_size):
        dst = close_table[i][0] 
        print(dst)
        if control_dist_km >= dst:
            distance = control_dist_km - dst #This is the distance between the current and closes interval'd distance
            time = distance / close_table[i-1][1] #Gets the distance to help find the time
            total_time += time #this continously keeps at the time
            control_dist_km -= distance #this updates the total distance

    brevet_start_time = arrow.get(brevet_start_time)
    hrs = int(total_time)
    #print(hrs)
    mts = round(60*(total_time - hrs))
    #print(mts)

    closing_time = brevet_start_time.shift(hours = hrs, minutes = mts) #This will take the proper hours and minutes and format it to proper time

    return closing_time.isoformat()




date = arrow.Arrow(2008,11,11)
print(open_time(200, 600, arrow.get(date)))
print(close_time(200, 600, arrow.get(date)))


#date = arrow.Arrow(2008,11,11)
#print(open_time(150, 200, arrow.get(date)))
#print(close_time(150, 200, arrow.get(date)))
