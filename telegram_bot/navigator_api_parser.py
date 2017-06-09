# coding: utf-8
import contextlib
import json
import ssl
import urllib2


def _load_poster(info_dict):
    poster = ''
    files = info_dict.get('files')
    if files and isinstance(files, list) and len(files) > 0:
        poster = files[0].get('url')

    if poster.find('127.0.0.1') > -1:
        poster = ''

    if not poster:
        files = info_dict.get('new_files')
        if files and isinstance(files, list) and len(files) > 0:
            poster = files[0].get('src')
    return poster


def _load_description(info_dict):
    description = info_dict.get('sms_description', '')
    if not description:
        description = info_dict.get(
            'web_description', 'К сожалению, нет описания'
        )
    return description


def _load_crm_id(info_dict):
    return info_dict.get('crm_id')


def _load_address(info_dict):
    address = info_dict.get('address')
    if address:
        country = address.get('country').encode('utf-8')
        city = address.get('place').encode('utf-8')
        street = address.get('street').encode('utf-8')
        house = address.get('house', '')
        if house:
            house = house.encode('utf-8')
        else:
            house = ''

        return '{}, {}, {} {}'.format(
            country, city, street, house
        ) if house not in street else '{}, {}, {}'.format(
            country, city, street
         )


def _load_location(info_dict):
    location = info_dict.get('location')
    return location


def _load_web_site(info_dict):
    return info_dict['web_site']


def _load_info(info_dict):

    info = {}
    info['description'] = _load_description(info_dict)
    info['poster'] = _load_poster(info_dict)
    info['crm_id'] = _load_crm_id(info_dict)
    info['address'] = _load_address(info_dict)
    info['location'] = _load_location(info_dict)
    info['web_site'] = _load_web_site(info_dict)
    return info


def load_navigator_api(api_link):
    context = ssl._create_unverified_context()
    request = urllib2.Request(
        api_link
    )
    with contextlib.closing(
            urllib2.urlopen(request, context=context)) as jf:

        l = json.loads(jf.read())
        my_dict = {}
        for d in l:
            name = d.get('name', '').strip()
            if not name:
                continue

            return _load_info(d)
