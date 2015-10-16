# -*- coding: utf-8 -*-

import urllib2
import json

known_formats = 'pdf doc docx'.split()


def get_attachment_or_description(url):
    f = urllib2.urlopen(url)
    s = f.read()
    f.close()

    try:
        data = json.loads(s, encoding='latin1')
    except ValueError:
        return (None, None)

    returned_url = _get_attachment_url(data)
    if returned_url:
        return (None, returned_url)

    return (_get_description(data), None)


def _get_attachment_url(data):
    # try to find a full announcement attachment
    for attachment in data.get('synopsisAttachments', []):
        if (attachment['attachmentType'].lower() == 'full announcement'
                and attachment['fileExt'].lower() in known_formats):
            url = (
                'http://www.grants.gov/grantsws/AttachmentDownload?attId=' +
                str(attachment['id'])
            )
            return url

    return None


def _get_description(data):
    # As I didn't find a full announcement attachment, I'll compose a text
    # content for loader to work on.

    text = """Due Date: %s

Estimated Total Program Funding: US$ %s
Award Ceiling: US$ %s
Award Floor: US$ %s
Agency Name: %s
Description: %s""" % (
        data.get('originalDueDate', ''),
        data['synopsis'].get('estimatedFundingFormatted', ''),
        data['synopsis'].get('awardCeiling', ''),
        data['synopsis'].get('awardFloor', ''),
        data['synopsis'].get('agencyName', ''),
        data['synopsis'].get('fundingActivityCategoryDesc', ''))

    return text
