import requests
from requests import Session
from requests.exceptions import HTTPError

try:
    from urllib.parse import urlencode, quote
except:
    from urllib import urlencode, quote
import json
from requests.packages.urllib3.contrib.appengine import is_appengine_sandbox

def initialize_app(config):
    return Firebase(config)

class Firebase:
    """ Firebase Interface """
    def __init__(self, config):
        self.storage_bucket = config["storageBucket"]
        self.credentials = None
        self.requests = requests.Session()
        if config.get("serviceAccount"):
            scopes = [
                'https://www.googleapis.com/auth/firebase.database',
                'https://www.googleapis.com/auth/userinfo.email',
                "https://www.googleapis.com/auth/cloud-platform"
            ]
            service_account_type = type(config["serviceAccount"])
            if service_account_type is str:
                self.credentials = ServiceAccountCredentials.from_json_keyfile_name(config["serviceAccount"], scopes)
            if service_account_type is dict:
                self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(config["serviceAccount"], scopes)
        if is_appengine_sandbox():
            # Fix error in standard GAE environment
            # is releated to https://github.com/kennethreitz/requests/issues/3187
            # ProtocolError('Connection aborted.', error(13, 'Permission denied'))
            adapter = appengine.AppEngineAdapter(max_retries=3)
        else:
            adapter = requests.adapters.HTTPAdapter(max_retries=3)

        for scheme in ('http://', 'https://'):
            self.requests.mount(scheme, adapter)

    def storage(self):
        return Storage(self.credentials, self.storage_bucket, self.requests)

class Storage:
    """ Storage Service """
    def __init__(self, credentials, storage_bucket, requests):
        self.storage_bucket = "https://firebasestorage.googleapis.com/v0/b/" + storage_bucket
        self.credentials = credentials
        self.requests = requests
        self.path = ""
        if credentials:
            client = storage.Client(credentials=credentials, project=storage_bucket)
            self.bucket = client.get_bucket(storage_bucket)

    def child(self, *args):
        new_path = "/".join(args)
        if self.path:
            self.path += "/{}".format(new_path)
        else:
            if new_path.startswith("/"):
                new_path = new_path[1:]
            self.path = new_path
        return self

    def put(self, file, token=None):
        # reset path
        path = self.path
        self.path = None
        if isinstance(file, str):
            file_object = open(file, 'rb')
        else:
            file_object = file
        request_ref = self.storage_bucket + "/o?name={0}".format(path)
        if token:
            headers = {"Authorization": "Firebase " + token}
            request_object = self.requests.post(request_ref, headers=headers, data=file_object)
            raise_detailed_error(request_object)
            return request_object.json()
        elif self.credentials:
            blob = self.bucket.blob(path)
            if isinstance(file, str):
                return blob.upload_from_filename(filename=file)
            else:
                return blob.upload_from_file(file_obj=file)
        else:
            request_object = self.requests.post(request_ref, data=file_object)
            raise_detailed_error(request_object)
            return request_object.json()

    def get_url(self, token=None):
        path = self.path
        self.path = None
        if path.startswith('/'):
            path = path[1:]
        if token:
            return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), token)
        return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPError(e, request_object.text)

if __name__ == "__main__" :
    config = {
  "storageBucket": "jetblueyhack.appspot.com"
}
    firebase = initialize_app(config)
    storage = firebase.storage()
    storage.child("/txt/Bad.txt").put("Bad.txt")
    storage.child("/txt/Good.txt").put("Good.txt")
    storage.child("/txt/Ok.txt").put("Ok.txt")
