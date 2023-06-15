from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError


class ProjectDocuments(models.Model):
    _name='project.project'
    _inherit='project.project'

    label_document = fields.Char(string='Use documents as', default=lambda s: _('Documents'), translate=True,
    help="Gives label to documents on project's kanban view.")    
    mom_count = fields.Integer(string="MOM:",compute='_compute_mom_attached_docs_count')
    dd_count = fields.Integer(string="Due Deligence:",compute='_compute_dd_attached_docs_count')
    ca_count = fields.Integer(string="Confidentiality Agreement:",compute='_compute_ca_attached_docs_count')
    ts_count = fields.Integer(string="Term Sheet:",compute='_compute_ts_attached_docs_count')
    im_count = fields.Integer(string="Investment Memo:",compute='_compute_im_attached_docs_count')
    fm_count = fields.Integer(string="Financial Model:",compute='_compute_fm_attached_docs_count')
    ip_count = fields.Integer(string="Investor Presentation:",compute='_compute_ip_attached_docs_count')
    doctypes= fields.One2many('ir.attachment','documenttype_id',string='Document Types')
    
    def _compute_mom_attached_docs_count(self):
        momAttachment = self.env['ir.attachment']
        for project in self:
            project.mom_count = momAttachment.search_count([
                '|',
                '&',
                ('documenttype_id', '=', 'MOM' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)
                
            ])
       
    def _compute_dd_attached_docs_count(self):
        ddAttachment = self.env['ir.attachment']
        for project in self:
            project.dd_count = ddAttachment.search_count([
                '|',
                '&',
                ('documenttype_id.name', '=', 'Due Deligence' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)
                
            ])

    def _compute_ca_attached_docs_count(self):
        caAttachment = self.env['ir.attachment']
        for project in self:
            project.ca_count = caAttachment.search_count([
                '|',
                '&',
               ('documenttype_id.name', '=', 'Confidentiality Agreement' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)  
                ])

    def _compute_ts_attached_docs_count(self):
        tsAttachment = self.env['ir.attachment']
        for project in self:
            project.ts_count = tsAttachment.search_count([ 
            '|',
                '&',
               ('documenttype_id.name', '=', 'Term Sheet' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)  
                ]) 

    def _compute_im_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for project in self:
            project.im_count = Attachment.search_count([
                '|',
                '&',
               ('documenttype_id.name', '=', 'Investment Memo' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)  
                ]) 

    def _compute_fm_attached_docs_count(self):
        fmAttachment = self.env['ir.attachment']
        for project in self:
            project.fm_count = fmAttachment.search_count([
                '|',
                '&',
               ('documenttype_id.name', '=', 'Financial Model' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)  
                ]) 

    def _compute_ip_attached_docs_count(self):
        ipAttachment = self.env['ir.attachment']
        for project in self:
            project.ip_count = ipAttachment.search_count([
                '|',
                '&',
               ('documenttype_id.name', '=', 'Investor Presentation' ),
                '&',
                ('res_model', '=', 'project.project'), ('res_id', '=', project.id),
                '&',
                ('res_model', '=', 'project.task'), ('res_id', 'in', project.task_ids.ids)  
                ])               

class Docs(models.Model):
    _name='ir.attachment'
    _inherit='ir.attachment'
    documenttype_id=fields.Many2one('business.document',string='Document Type')
    doc_date=fields.Date(string='Document Date')
    doc_version=fields.Float(string='Document Version')


class BusinessDocument(models.Model):
    _name = 'business.document'

    name = fields.Char(string='Document Type', required=True, translate=True)
    sequence = fields.Integer()
    documenttype_id = fields.One2many('ir.attachment','documenttype_id', string="Projects")