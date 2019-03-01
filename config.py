# path settings --------------------------------------------------
path_data = r'./data/'
path_img = r'imgs/'
path_driver = r'./drivers'
# -------------------------------------------------- path settings

# target urls ----------------------------------------------------
base_url = 'https://www.freelancer.com/'
url_login = base_url + 'login'
user_pages = base_url + 'search/users/any_skill/{}/{}/'
# ---------------------------------------------------- target urls

# time settings --------------------------------------------------
sleep_short = 1
sleep_med = 3
sleep_long = 10
# -------------------------------------------------- time settings

# selenium settings ----------------------------------------------
f_cookie = 'cookies.pkl'

start = 0
concurrent = 3
partition = 3
timeout = 10
# ---------------------------------------------- selenium settings

# Latin American countries available on Freelancer ---------------
countries = [
    'Antigua and Barbuda',
    'Aruba',
    'Bahamas',
    'Barbados',
    'Cayman Islands',
    'Cuba',
    'Dominica',
    'Dominican Republic',
    'Grenada',
    'Guadeloupe',
    'Haiti',
    'Jamaica',
    'Martinique',
    'Puerto Rico',
    'Saint Barthelemy',
    'Saint Kitts and Nevis',
    'Saint Lucia',
    'Saint Vincent and the Grenadines',
    'Trinidad and Tobago',
    'Turks and Caicos Islands',
    'Virgin Islands',
    'Belize',
    'Costa Rica',
    'El Salvador',
    'Guatemala',
    'Honduras',
    'Mexico',
    'Nicaragua',
    'Panama',
    'Argentina',
    'Bolivia',
    'Brazil',
    'Chile',
    'Colombia',
    'Ecuador',
    'French Guiana',
    'Guyana',
    'Paraguay',
    'Peru',
    'Suriname',
    'Uruguay',
    'Venezuela',
]
# --------------- Latin American countries available on Freelancer
