# -*- coding: utf-8 -*-


class VarStackList(object):

    stack = []
    ele_stack = []
    sub_stack = stack

    def add_both(self, var):
        self.add_ele(var)
        self.add_sub(var)

    def drop_both(self):
        self.drop
        self.ele_drop

    def add_ele(self, var):
        self.ele_stack.append(var)

    def add(self, var):
        self.stack.append(var)
    
    @property
    def pop(self):
        if len(self.stack) > 0:
            self.stack.pop(-1)
        else:
            print "stack is empty. cannot pop or lock."

    @property
    def drop_ele(self):
        self.ele_stack.pop(-1)

    @property
    def ele_str(self):
        return '.'.join(self.ele_stack)

    @property
    def string(self):
        return '.'.join(self.stack)
