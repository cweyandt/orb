# -*- coding: utf-8 -*-
"""
This module implements the REST API used to interact with the test case.  
The API is implemented using the ``flask`` package.  

Adapted from https://raw.githubusercontent.com/SenHuang19/BuildingControlEmulator/master/restapi.py
"""

# GENERAL PACKAGE IMPORT
# ----------------------
from flask import Flask
from flask_restful import Resource, Api, reqparse
# ----------------------

# Pre-defined model import
# ----------------
from orb_models import OrbModel
# ----------------

# FLASK REQUIREMENTS
# ------------------
app = Flask(__name__)
api = Api(app)
# ------------------

# Load the default model
# ---------------------
model = OrbModel()
# ---------------------

# DEFINE ARGUMENT PARSERS
# -----------------------
# ``select model`` interface
parser_model = reqparse.RequestParser()
parser_model.add_argument('model')

# ``analyze`` interface
parser_advance=[]
for i in range(len(case.u)):
   temp = reqparse.RequestParser()
   for key in case.u[i].keys():
        temp.add_argument(key)
   parser_advance.append(temp)
# -----------------------

# DEFINE REST REQUESTS
# --------------------

class ModelAPI(Resource):
    '''Interface to pre-trained models.'''
     
    def get(self):

        '''GET request to receive available parameters for loaded model.'''
        name=model.get_name()
        print name
        return name
   
    def put(self):
        '''PUT request to change the model.'''
        # global case_index   
        # args = parser_name.parse_args()
        # print args
        # name=args['name']
        # i=0
        # for fmu_name in case.get_name():
        #         if name == fmu_name:
        #             case_index=i

        #             break
        #         i=i+1
        # print case_index
        # return 'Testcase selected.'
        pass 

        
class Inputs(Resource):
    '''Interface to model inputs.'''
    
    def get(self):
        '''GET request to receive list of available inputs.'''
        u_list = model.get_inputs()
        return u_list
        

class AnalyzeAPI(Resource):
    '''Interface to obtain estimates.'''

    def get(self):
        '''GET request to receive estimates from loaded model.'''
        print model.get_name()
        print model.input_status()
        args = parser_analyze.parse_args()
        print args
        res=mode.analyze()
        return res
        

class ResultsAPI(Resource):
    '''Interface to test case result data.'''
 
    def get(self):
        '''GET request to receive analysis results.'''
        Y = model.get_results()
        return Y


class PingAPI(Resource):
    '''Interface to validate api is online'''

    def get(self):
        return 'Pong.'

# --------------------
        
# ADD REQUESTS TO API WITH URL EXTENSION
# --------------------------------------
api.add_resource(ModelAPI, '/model')
api.add_resource(InputsAPI, '/inputs')
api.add_resource(AnalyzeAPI, '/analyze')
api.add_resource(ResultsAPI, '/results')
api.add_resource(PingAPI, '/ping')

# --------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')