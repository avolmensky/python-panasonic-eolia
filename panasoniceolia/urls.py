
BASE_URL = 'https://app.rac.apws.panasonic.com/eolia/v2'

def login():
    return '{base_url}/auth/login'.format(
        base_url=BASE_URL)

def get_devices():
    return '{base_url}/devices'.format(
        base_url=BASE_URL)

# def get_groups():
#     return '{base_url}/device/group'.format(
#         base_url=BASE_URL)

def status(id):
    return '{base_url}/devices/{id}/status'.format(
        base_url=BASE_URL,
        id=id
    )

def statusCache(guid):
    return '{base_url}/deviceStatus/now/{guid}'.format(
        base_url=BASE_URL,
        guid=guid
    )

# def control(id):
#     return '{base_url}/devices/{id}/control'.format(
#         base_url=BASE_URL
#     )

def history():
    return '{base_url}/deviceHistoryData'.format(
        base_url=BASE_URL,
    )
