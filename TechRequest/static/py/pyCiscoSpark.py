# This file come from: https://github.com/brbester/pyCiscoSpark/blob/master/pyCiscoSpark.py
# Thanks to brbester who is the creator.
# I just completed the missing feature that I need.

import requests
import json
import ntpath
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re

# COMMENTED SECTION BELOW FOR DEBUGGING

#import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
#try:
#    import http.client as http_client
#except ImportError:
    # Python 2
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger('requests.packages.urllib3')
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True


# Helpers
def _url(path):
    return 'https://api.ciscospark.com/v1' + path

def _fix_at(at):
    at_prefix = 'Bearer '
    if not re.match(at_prefix, at):
        return 'Bearer ' + at
    else:
        return at

# Search functions
def findroomidbyname(at, roomname):
    room_dict = get_rooms(_fix_at(at))
    for room in room_dict['items']:
        if room['title'] == roomname:
            return room['id']
        else:
            return

def searchroomsbyname(at, roomname):
    result = []
    room_dict = get_rooms(_fix_at(at))
    for room in room_dict['items']:
        if roomname in room["title"]:
          result.append(room)
    return result

def findteamidbyname(at, teamname):
    team_dict = get_teams(_fix_at(at))
    for team in team_dict['items']:
        if team['title'] == teamname:
            return team['id']
        else:
            return

def searchteamsbyname(at, teamname):
    result = []
    team_dict = get_teams(_fix_at(at))
    for team in team_dict['items']:
        if teamname in team["name"]:
          result.append(team)
    return result

def findmsgidbyname(at, msgtxt):
    msg_dict = get_message(_fix_at(at))
    for msg in msg_dict['items']:
        if msg['text'] == msgtxt:
            return msg['id']
        else:
            return

def searchmsgsbyname(at, msgtxt, roomid):
    result = []
    msg_dict = get_messages(_fix_at(at),roomid)
    for msg in msg_dict['items']:
        if msgtxt in msg["text"]:
          result.append(msg)
    return result


def code(resp):
  if resp.status_code == requests.codes.ok:
    res = "OK"
  else:
    res = "KO"

  try:
    dict = json.loads(resp.text)
    dict['statuscode'] = str(resp.status_code)
    dict['status'] = res
    return dict
  except (ValueError, KeyError, TypeError) as error:
    return resp.text

# GET Requests
def get_authorize( response_type, scope, state, client_id, redirect_uri):
    headers = {'content-type': 'application/json'}
    payload = {'response_type': response_type, 'scope': scope, 'state': state, 'client_id': client_id, 'redirect_uri': redirect_uri}
    resp = requests.get(url=_url('/authorize'), json=payload, headers=headers)
    return code(resp)

def get_peoples(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/people'), headers=headers)
    return code(resp)

def get_people(at, email='', displayname='', max=10):
    headers = {'Authorization': _fix_at(at)}
    payload = {'max': max}
    if email:
        payload['email'] = email
    if displayname:
        payload['displayName'] = displayname
    resp = requests.get(_url('/people'), params=payload, headers=headers)
    return code(resp)

def get_me(at):
    headers = {'Authorization': _fix_at(at)}
    payload = {}
    resp = requests.get(_url('/people/me'), params=payload, headers=headers)
    return code(resp)

def get_persondetails(at, personId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/people/{:s}/'.format(personId)), headers=headers)
    return code(resp)

def get_me(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/people/me'), headers=headers)
    return code(resp)

def get_rooms(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/rooms'), headers=headers)
    return code(resp)

def get_room(at, roomId):
    headers = {'Authorization': _fix_at(at)}
    payload = {'showSipAddress': 'true'}
    resp = requests.get(_url('/rooms/{:s}'.format(roomId)), params=payload, headers=headers)
    return code(resp)

def get_teams(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/teams'), headers=headers)
    return code(resp)

def get_team(at, teamId):
    headers = {'Authorization': _fix_at(at)}
    payload = {'showSipAddress': 'true'}
    resp = requests.get(_url('/teams/{:s}'.format(teamId)), params=payload, headers=headers)
    return code(resp)

def get_memberships(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/memberships'), headers=headers)
    return code(resp)

def get_membership(at, membershipId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/memberships/{:s}'.format(membershipId)), headers=headers)
    return code(resp)

def get_messages(at, roomId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId}
    resp = requests.get(_url('/messages'), params=payload, headers=headers)
    return code(resp)

def get_message(at, messageId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/messages/{:s}'.format(messageId)), headers=headers)
    return code(resp)

def get_webhooks(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/webhooks'), headers=headers)
    return code(resp)

def get_webhook(at, webhookId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/webhooks/{:s}'.format(webhookId)), headers=headers)
    return code(resp)

# POST Requests
def post_room(at, title):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'title': title}
    resp = requests.post(url=_url('/rooms'), json=payload, headers=headers)
    return code(resp)

def post_team(at, name):
    print 'at: '+at
    print 'name: '+name

    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'name': name}
    resp = requests.post(url=_url('/teams'), json=payload, headers=headers)

    print 'resp: '+str(resp)
    return code(resp)

def post_people(at, emails, displayName, firstName, lastName, avatar, orgId, roles, licenses):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'emails': emails, 'displayName':displayName, 'firstName':firstName, 'lastName':lastName, 'avatar':avatar, 'orgId':orgId, 'roles':roles, 'licenses':licenses }
    resp = requests.post(url=_url('/people'), json=payload, headers=headers)
    return code(resp)

def post_message(at, roomId, text, toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'text': text}
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), json=payload, headers=headers)
    return code(resp)

def post_file(at, roomId, url, text='', toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'files': [url]}
    if text:
        payload['text'] = text
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), json=payload, headers=headers)
    return code(resp)

def post_localfile(at, roomId, filename, text='', toPersonId='', toPersonEmail=''):
    openfile = open(filename, 'rb')
    filename = ntpath.basename(filename)
    payload = {'roomId': roomId, 'files': (filename, openfile, 'image/jpg')}
    if text:
        payload['text'] = text
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    m = MultipartEncoder(fields=payload)
    headers = {'Authorization': _fix_at(at), 'Content-Type': m.content_type}
    resp = requests.request("POST",url=_url('/messages'), data=m, headers=headers)
    return code(resp)

def post_roommembership(at, roomId, personEmail, isModerator=True):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'personEmail': personEmail, 'isModerator': isModerator}
    resp = requests.post(url=_url('/memberships'), json=payload, headers=headers)
    return code(resp)

def post_teammembership(at, teamId, personEmail, isModerator=True):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'teamId': teamId, 'personEmail': personEmail, 'isModerator': isModerator}
    resp = requests.post(url=_url('/room/memberships'), json=payload, headers=headers)
    return code(resp)

def post_webhook(at, name, targetUrl, resource, event, filter):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'name': name, 'targetUrl': targetUrl, 'resource': resource, 'event': event, 'filter': filter}
    resp = requests.post(url=_url('/webhooks'), json=payload, headers=headers)
    return code(resp)

# PUTS
def put_room(at, roomId, title='title'):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'title': title}
    resp = requests.put(url=_url('/rooms/{:s}'.format(roomId)), json=payload, headers=headers)
    return code(resp)

def put_team(at, teamId, name='name'):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'name': name}
    resp = requests.put(url=_url('/teams/{:s}'.format(teamId)), json=payload, headers=headers)
    return code(resp)

def put_people(at, emails, displayName, firstName, lastName, avatar, orgId, roles, licenses):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'emails': emails, 'displayName':displayName, 'firstName':firstName, 'lastName':lastName, 'avatar':avatar, 'orgId':orgId, 'roles':roles, 'licenses':licenses }
    resp = requests.put(url=_url('/people'), json=payload, headers=headers)
    return code(resp)

def put_membership(at, membershipId, isModerator):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'isModerator': isModerator}
    resp = requests.put(url=_url('/memberships/{:s}'.format(membershipId)), json=payload, headers=headers)
    return code(resp)

def put_webhook(at, webhookId, name, targetUrl):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'name': name, 'targetUrl': targetUrl}
    resp = requests.put(url=_url('/webhooks/{:s}'.format(webhookId)),json=payload, headers=headers)
    return code(resp)

# DELETES
def del_room(at, roomId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/rooms/{:s}'.format(roomId)), headers=headers)
    return code(resp)

def del_team(at, teamId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/teams/{:s}'.format(teamId)), headers=headers)
    return code(resp)

def del_people(at, peopleId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/people/{:s}'.format(peopleId)), headers=headers)
    return code(resp)

def del_membership(at, membershipId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/memberships/{:s}'.format(membershipId)), headers=headers)
    return code(resp)

def del_message(at, messageId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/messages/{:s}'.format(messageId)), headers=headers)
    return code(resp)

def del_webhook(at, webhookId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/webhooks/{:s}'.format(webhookId)), headers=headers)
    return code(resp)

