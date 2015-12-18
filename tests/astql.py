#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import ast
import copy

class BaseConstructorMixin(object):
    def setUp(self):
        pass

class KwConstructorMixin(BaseConstructorMixin):
    def __init__(self,**kwargs):
        for k in kwargs:
            setattr(self,k,kwargs[k])
        self.setUp()
class ArgsConstructorMixin(BaseConstructorMixin):
    def __init__(self,*args):
        self.args=[]
        for a in args:
            self.args.append(a)
        self.setUp()

class Query(KwConstructorMixin):
    def get_results(self):
        self.result_dict={}
        for root,dirs,files in os.walk(self.start):
            for f in files:
                if f.endswith('.py'):
                    for result in self.process_python_file(root,f):
                        yield result
        return
        yield
    
    def process_python_file(self,relative_dir,file_name):
        file_content=open(os.path.join(relative_dir,file_name),'r').read()
        for result in self.pattern.node_enter('python_file',self.result_dict,
                                              file_content=file_content,
                                              name=file_name,
                                              relative_dir=relative_dir):
            yield result
        tree=ast.parse(file_content)
        
        self.pattern.node_exit('python_file',self.result_dict,file_content=file_content)
        return
        yield
        
        
class PyFile(KwConstructorMixin):
    def node_enter(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_file':
            result_dict[self.var]={'name':kwargs['name'],
                                   'relative_dir':kwargs['relative_dir'],
                                   'num_lines':len(kwargs['file_content'].split('\n'))
                                  }
            yield copy.copy(result_dict)
        return
        yield
    def node_exit(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_file':
            del result_dict[self.var]

class PyClass(KwConstructorMixin):
    pass

class PyMethod(KwConstructorMixin):
    pass

class And(ArgsConstructorMixin):
    pass

class PyString(KwConstructorMixin):
    pass

class Stack(ArgsConstructorMixin):
    def setUp(self):
        self.level=0
    def node_enter(self,pattern_type,result_dict,*args,**kwargs):
        yielded=False
        if self.level<len(self.args):
            for result in self.args[self.level].node_enter(pattern_type,result_dict,*args,**kwargs):
                yielded=True
                yield result
            if yielded:
                self.level+=1
        return 
        yield
    def node_exit(self,pattern_type,result_dict,*args,**kwargs):
        pass