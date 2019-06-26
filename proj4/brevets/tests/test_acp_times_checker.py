import acp_times
import nose
import arrow




def test_open():
        '''
        This function is meant to test a open_time function solo.
        '''

        date = arrow.Arrow(2008,11,11)
        assert acp_times.open_time(200, 600, arrow.get(date)) == (date.shift(hours=5,minutes=53)).isoformat()


def test_close():
        '''
        This funciton tests the close_time function by itself
        '''

        date = arrow.Arrow(2008,11,11)
        assert acp_times.close_time(200, 600, arrow.get(date)) == (date.shift(hours=13,minutes=20)).isoformat()

def test_boundry_case():
	'''
	This function will use a case that is on the edge of one boundry
	'''
	
	date = arrow.Arrow(2008,11,11)
	assert acp_times.open_time(400, 400, arrow.get(date)) == (date.shift(hours=12,minutes=8)).isoformat()
	assert acp_times.close_time(400, 400, arrow.get(date)) == (date.shift(hours=26,minutes=40)).isoformat()


def test_small_cases():
        '''
        This function is meant to test the smallest values of the ACP table which in this case is 0 to 200. This will show that simple and small values will work for thetable."

        '''
        date = arrow.Arrow(2008,11,11)
        assert acp_times.open_time(4, 200, arrow.get(date)) == (date.shift(hours=0,minutes=7)).isoformat()
        assert acp_times.close_time(4, 200, arrow.get(date)) == (date.shift(hours=0, minutes=16)).isoformat()



def test_big_cases():
        '''
        This function is meant to test the biggest value of the ACP table which boboundries range from about 700 to 1000.

        '''
        date = arrow.Arrow(2008,11,11)
        assert acp_times.open_time(899, 1000, arrow.get(date)) == (date.shift(hours=29,minutes=29)).isoformat()
        assert acp_times.close_time(899, 1000, arrow.get(date)) == (date.shift(hours=66,minutes=10)).isoformat()
