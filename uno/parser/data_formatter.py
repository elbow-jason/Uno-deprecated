# -*- coding: utf-8 -*-

class DataFormatter(object):

    def __init__(self, parent_obj):
        self.parent = parent_obj
        self.prep_funcs = {}



    def css(self, info):
        info['data']['stack'] = info['stack']
        return info['data']

    def element(self, info):
        varname = info['data']+'_'+str(info['g_id'])
        stack   = info['stack']
        tag     = info['data']
        return dict(stack=, varname=varname, tag=tag)

    def payload(self, info):
        payload = self.cleanup_payload(info['data'])
        if payload == "":
            return ''
        pname = 'payload_' + str(info['g_id'])
        stack = info['stack']
        return dict(stack=stack, pname=pname, payload=payload)

    
    def run(self, parsed_data):

