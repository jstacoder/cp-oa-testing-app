import json 

def get_providers(calendars):
    return list(
        set(
            [ 
                cal.get('provider_name') for cal in calendars
            ]
        )
    )

def get_calenders_by_provider(calendars):
    rtn = {}
    for provider in get_providers(calendars):
        rtn[provider] = [
            {
                'calendar_id' : cal.get('calendar_id'),
                'calendar_name': cal.get('calendar_name'),
                'profile_id': cal.get('profile_id'),
                'profile_name': cal.get('profile_name')
            }
            for cal in calendars\
                if cal.get('provider_name') == provider
            
        ]
    return rtn

test_data = [{u'calendar_deleted': False,
  u'calendar_id': u'cal_WIjjxfYZxUwpAAZm_Xjq6asKSQGIhwbirVbPwQQ',
  u'calendar_name': u'jstacoder@gmail.com',
  u'calendar_primary': True,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIjjxfYZxUwpAAZm',
  u'profile_name': u'jstacoder@gmail.com',
  u'provider_name': u'google'},
 {u'calendar_deleted': False,
  u'calendar_id': u'cal_WIjjxfYZxUwpAAZm_MjhNa3OtNEppTHIYkDbLVQ',
  u'calendar_name': u'Savvy Appointments',
  u'calendar_primary': False,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIjjxfYZxUwpAAZm',
  u'profile_name': u'jstacoder@gmail.com',
  u'provider_name': u'google'},
 {u'calendar_deleted': False,
  u'calendar_id': u'cal_WIjn1PYZxUwpAAn4_KdBPnKRFGH-9c7M@BO8aMw',
  u'calendar_name': u'Calendar',
  u'calendar_primary': False,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIjn1PYZxUwpAAn4',
  u'profile_name': u'jstacoder@outlook.com',
  u'provider_name': u'live_connect'},
 {u'calendar_deleted': False,
  u'calendar_id': u'cal_WIffNPYZxRbxAA8h_Zrdo8oXmrf3lkRJd6LcNnA',
  u'calendar_name': u'kyle@casepeer.com',
  u'calendar_primary': True,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIffNPYZxRbxAA8h',
  u'profile_name': u'kyle@casepeer.com',
  u'provider_name': u'google'},
 {u'calendar_deleted': False,
  u'calendar_id': u'cal_WIjhsfYZxUwJAAv3_l1kd@ZR8yBavux9nP6E9bw',
  u'calendar_name': u'Family',
  u'calendar_primary': False,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIjhsfYZxUwJAAv3',
  u'profile_name': u'jstacoder@gmail.com',
  u'provider_name': u'apple'},
 {u'calendar_deleted': False,
  u'calendar_id': u'cal_WIjhsfYZxUwJAAv3_9CFv2VHLYMj24LVZpcTbUA',
  u'calendar_name': u'Home',
  u'calendar_primary': False,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIjhsfYZxUwJAAv3',
  u'profile_name': u'jstacoder@gmail.com',
  u'provider_name': u'apple'},
 {u'calendar_deleted': False,
  u'calendar_id': u'cal_WIjhsfYZxUwJAAv3_uoZijBN0yypQZzvdX7ljXg',
  u'calendar_name': u'Work',
  u'calendar_primary': False,
  u'calendar_readonly': False,
  u'permission_level': u'sandbox',
  u'profile_id': u'pro_WIjhsfYZxUwJAAv3',
  u'profile_name': u'jstacoder@gmail.com',
  u'provider_name': u'apple'}]

def test():
    print json.dumps(get_calenders_by_provider(test_data))

if __name__ == "__main__":
    test()
            