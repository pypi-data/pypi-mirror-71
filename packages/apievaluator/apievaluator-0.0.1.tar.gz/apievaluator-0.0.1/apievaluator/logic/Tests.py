import json
import re
from importlib import import_module

import click
import requests


def checkObjectTypes(resp, cond, testDict):
    ret = []
    if isinstance(cond, str):
        testDict['test'] += 1
        if cond == 'int':
            if isinstance(resp, int):
                testDict['success'] = testDict['success']+1
                ret.append((True, 'OK - int'))
            else:
                testDict['failed'] = testDict['failed']+1
                ret.append((False, 'Not OK - expected %s, got %s' % (cond, type(resp).__name__)))
        elif cond == 'string':
            if isinstance(resp, str):

                testDict['success'] = testDict['success']+1
                ret.append((True, 'OK - string'))
            else:
                testDict['failed'] = testDict['failed']+1
                ret.append((False, 'Not OK - expected %s, got %s' % (cond, type(resp).__name__)))
        elif cond == 'array':
            if isinstance(resp, list):

                testDict['success'] = testDict['success']+1
                ret.append((True, 'OK - array'))
            else:
                testDict['failed'] = testDict['failed']+1
                ret.append((False, 'Not OK - expected %s, got %s' % (cond, type(resp).__name__)))

    elif isinstance(cond, (object, dict)):
        for key, dataType in cond.items():
            testDict['test'] = testDict['test']+1
            if dataType == 'int':
                if isinstance(resp.get(key), int):
                    testDict['success'] = testDict['success']+1
                    ret.append((True, 'OK - int'))
                else:
                    testDict['failed'] = testDict['failed']+1
                    ret.append((False, 'Not OK - expected %s, got %s' % (cond, type(resp).__name__)))
            elif dataType == 'string':
                if isinstance(resp.get(key), str):
                    testDict['success'] = testDict['success']+1
                    ret.append((True, 'OK - string'))
                else:
                    testDict['failed'] = testDict['failed']+1
                    ret.append((False, 'Not OK - expected %s, got %s' % (cond, type(resp).__name__)))
            elif dataType == 'array':
                if isinstance(resp.get(key), list):
                    testDict['success'] = testDict['success']+1
                    ret.append((True, 'OK - array'))
                else:
                    testDict['failed'] = testDict['failed']+1
                    ret.append((False, 'Not OK - expected %s, got %s' % (cond, type(resp).__name__)))
            elif isinstance(dataType, object):
                testDict['success'] = testDict['success']+1
                ret.extend(checkObjectTypes(resp.get(key), dataType, testDict))
            else:
                testDict['failed'] = testDict['failed']+1
    return ret


def load_custom_test(name: str, prop: str, arg: str):
    kls = getattr(import_module('ApiEvaluator.CustomTests'), name)
    return kls(prop, arg) if arg else kls(prop)


def CheckIfEndpointsExist(paths, apiurl):
    result = {}
    routes = []
    ret = []
    testDict = {
        'total': 0,
        'success': 0,
        'failed': 0
    }

    for key in paths:
        routes.append(apiurl+key)
    for r in routes:
        TestGet(routes, result, r)

    for key in result:
        testDict['test'] = testDict['test']+1
        if result[key] == True:
            testDict['success'] = testDict['success']+1
            ret.append((True, '%s - Exists' % key))
        elif result[key] == False:
            testDict['failed'] = testDict['failed']+1
            ret.append((False, '%s - Does not exist' % key))

    return (ret, testDict)


def TestGet(routes, result, r):
    res = requests.get(r, verify=False)

    # result[r] = res.status_code >= 200 and res.status_code < 400

    if str(res.status_code)[0] == '2':
        result[r] = True
    elif res.status_code == 404:
        result[r] = False
    elif res.reason != 'Not Found':
        result[r] = True
    else:
        result[r] = True


def EvaluateResponses(apiurl, tests):
    endpoints = tests["endpoints"]
    endpointSpec = {}
    resource = {}
    ret = []
    testDict = {
        'total': 0,
        'success': 0,
        'failed': 0
    }

    for key, endpointSpec in endpoints.items():
        endpointMethods = endpointSpec.get('data')
        for method, condition in endpointMethods.items():
            results = []
            results.append('%s %s' % (method, apiurl + key))

            if method == 'GET':
                expectedType = condition.get('resp').get('type')
                url = apiurl

                if condition.get('req') == None:
                    url = apiurl+key
                elif condition.get('req').get('in') == 'route':
                    a = re.sub(r'\{.*\}', condition.get('req').get('Id'), key)
                    url = apiurl+a

                r = requests.get(url, verify=False)
                resp = json.loads(r.text)
                if expectedType != "object":
                    results.extend(checkObjectTypes(resp, condition.get('resp').get('type'), testDict))
                else:
                    results.extend(checkObjectTypes(resp, condition.get('resp').get('object'), testDict))

                custom = condition.get('custom')
                if custom:
                    for test in custom:
                        t = load_custom_test(test['name'], test['prop'], test.get('arg'), import_module)
                        results.append(t.run(resp))
            elif method == 'POST':
                if condition.get('req').get('in') != "body":
                    results.append((False, f'No body data for POST {key}'))
                else:
                    url = apiurl+key
                    reqData = condition.get('req').get('object')
                    r1 = requests.post(url, json=reqData, verify=False)
                    if r1.status_code == 201:
                        click.secho(str(r1.status_code) + " Created Succesfuly", bg="green", fg="white")
                        results.extend(checkObjectTypes(json.loads(r1.text), condition.get('resp').get('object'), testDict))
                    else:
                        click.secho("Unexpected Error", bg='red', fg='white')
                        testDict['test'] = testDict['test']+1
                        testDict['failed'] = testDict['failed']+1
                        results.append((False, 'Unexpected error, 1st attempt status code %d' % r1.status_code))

                    r2 = requests.post(url, json=reqData, verify=False)
                    if r2.status_code == 400:
                        click.secho(str(r2.status_code)+" Bad request: \"" +
                                    r2.text+"\" Expected", bg="green", fg="white")
                    else:
                        testDict['test'] = testDict['test']+1
                        testDict['failed'] = testDict['failed']+1
                        results.append((False, 'Unexpected error, 2nd attempt status code %d' % r2.status_code))

                    custom = condition.get('custom')
                    if custom:
                        for test in custom:
                            t = load_custom_test(test['name'], test['prop'], test.get('arg'), import_module)
                            results.append(t.run(r1.json()))
            elif method == 'PUT':
                if condition.get('req').get('in') != "both":
                    results.append((False, f'No body data for POST {key}'))
                else:
                    a = re.sub(r'\{.*\}', condition.get('req').get('Id'), key)
                    url = apiurl+a
                    reqData = condition.get('req').get('object')
                    r1 = requests.put(url, json=reqData, verify=False)
                    if r1.status_code == 200:
                        results.extend(checkObjectTypes(json.loads(r1.text), condition.get('resp').get('object'), testDict))
                    else:
                        results.append((False, f'Bad status code for PUT {key} -> {r1.status_code}'))
                    r2 = requests.put(url, json=reqData, verify=False)
                    if r2.status_code == 400:
                        click.secho(str(r2.status_code)+" Bad request: \"" + r2.text+"\" Expected", bg="green", fg="white")
                    else:
                        testDict['test'] = testDict['test']+1
                        testDict['failed'] = testDict['failed']+1

            ret.append((True, results))

    return (ret, testDict)


def merge(A: dict, B: dict, f: lambda x, y: (x, y)):
    merged = {k: A.get(k, B.get(k)) for k in A.keys() ^ B.keys()}
    merged.update({k: f(A[k], B[k]) for k in A.keys() & B.keys()})
    return merged


def eval_all(paths, apiurl, tests):
    [exist, count1] = CheckIfEndpointsExist(paths, apiurl)
    [tests, count2] = EvaluateResponses(apiurl, tests)
    return (exist, tests, merge(count1, count2, lambda x, y: x+y))
