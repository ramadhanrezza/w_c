from flask_restful import Resource, reqparse
from flask import request
from app.models import company
from app import mysql


class CompanyController(Resource):
    def get(self):
        try:
            if len(request.args) == 0:
                try:
                    companies = company.get_companies()
                    
                    return {
                        'status_code': 200,
                        'message': 'successful',
                        'data': companies
                    }
                except Exception as e:
                    return {
                        'status_code': 400,
                        'message': str(e),
                        'data': list()
                    }
                
            else:
                if request.args.get('company_name'):
                    try:
                        companies = company.get_detail_company(request.args['company_name'])

                        return {
                            'status_code': 200,
                            'message': 'successful',
                            'data': companies
                        }
                    except Exception as e:
                        return {
                            'status_code': 400,
                            'message': str(e),
                            'data': list()
                        }
                elif request.args.get('industry'):
                    try:
                        companies = company.get_company_by_industry(request.args['industry'])

                        return {
                            'status_code': 200,
                            'message': 'successful',
                            'data': companies
                        }
                    except Exception as e:
                        return {
                            'status_code': 400,
                            'message': str(e),
                            'data': list()
                        }
                elif request.args.get('revenue'):
                    try:
                        companies = company.get_company_by_revenue(request.args['revenue'])

                        return {
                            'status_code': 200,
                            'message': 'successful',
                            'data': companies
                        }
                    except Exception as e:
                        return {
                            'status_code': 400,
                            'message': str(e),
                            'data': list()
                        }
                else:
                    return {
                        'status_code': 400,
                        'message': 'Filter not available.',
                        'data': list()
                    }
        except Exception as e:
            return {
                'status_code': 400,
                'message': str(e),
                'data': list()
            }