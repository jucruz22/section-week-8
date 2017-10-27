import json
import requests
from config import FLICKR_API_KEY

CACHE_FNAME = 'cache_file.json'
DEBUG = False

def load_cache_json():
    # global CACHE_DICTION
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}

    return CACHE_DICTION

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

# changing function so its less specific to tags - multipurpose function
params_diction_search = {
    "method": "flickr.photos.search",
    "format": "json",
    "api_key": FLICKR_API_KEY,
    "tags": tags,
    "per_page": per_page,
    "nojsoncallback": 1
}

params_diction_getInfo = {
    "method": "flickr.photos.getInfo"
    "format": "json",
    "api_key": FLICKR_API_KEY,
    "photo_id": photo_id,
    # "per_page": per_page,
    "nojsoncallback": 1
}

def search_flickr(params_diction):
    if not FLICKR_API_KEY:
        raise Exception('Flickr API Key is missing!')

    baseurl = "https://api.flickr.com/services/rest/"
    params_diction = params_diction
    #    {
    #     "method": method, # "flickr.photos.search",
    #     "format": "json",
    #     "api_key": FLICKR_API_KEY,
    #     "tags": tags,
    #     "per_page": per_page,
    #     "photo_id": photo_id,
    #     "nojsoncallback": 1
    # }

    unique_ident = params_unique_combination(baseurl,params_diction)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(baseurl, params_diction)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

class Photo:
    def __init__(self, photo_dict):
        self.title = photo_dict['title']
        self.id = photo_dict['id']
        self.owner = photo_dict['owner']
        try:
            self.owner_username = photo_dict['owner']['username']
        except:
            self.owner_username = ""

    def __str__(self):
        return '{0} by {1}'.format(self.title, self.owner_username)



CACHE_DICTION = load_cache_json()
if DEBUG:
    print(CACHE_DICTION)

results = search_flickr_by_tags('sunset summer')

photos_list = []
for r in results['photos']['photo']:
    photos_list.append(Photo(r))

print()
print("= compare these outputs = >> ")
print(photos_list)
print("\n= vs = >> \n")

for photo in photos_list:
    print(photo)

    # if you get encoding error, try this
    # print(str(photo).encode('utf-8'))

print()
