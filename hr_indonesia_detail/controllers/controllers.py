# -*- coding: utf-8 -*-
from openerp import http

# class HrDetail(http.Controller):
#     @http.route('/hr_indonesia_detail/hr_indonesia_detail/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_indonesia_detail/hr_indonesia_detail/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_detail.listing', {
#             'root': '/hr_indonesia_detail/hr_indonesia_detail',
#             'objects': http.request.env['hr_indonesia_detail.hr_indonesia_detail'].search([]),
#         })

#     @http.route('/hr_indonesia_detail/hr_indonesia_detail/objects/<model("hr_indonesia_detail.hr_indonesia_detail"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_detail.object', {
#             'object': obj
#         })