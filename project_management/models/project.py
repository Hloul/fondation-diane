from odoo import api, fields, models, tools, SUPERUSER_ID,  _
from odoo.exceptions import UserError, AccessError, ValidationError

class ProjectManagement(models.Model):
    _name='project.project'
    _inherit='project.project'
    
    phase_id=fields.Many2one('project.phase', string='Phase')
    category_id =fields.Many2one('project.category', string='Category')
    status_id=fields.Many2one('project.status', string='Status')
    tag_ids=fields.Many2many('project.tags', string='Tag')
    supervisor_id=fields.Many2one('res.partner', string='Supervisor',track_visibility="onchange")
    leadmanager_id=fields.Many2one('res.partner',string='Lead Manager',track_visibility="onchange")
    Analyst_id=fields.Many2one('res.partner',string='Analyst',track_visibility="onchange")
    start_date=fields.Date(string='Start Date')
    golive_date=fields.Date(string='Go Live Date')

    @api.multi
    def write(self, vals):
        res = super(ProjectManagement, self).write(vals) if vals else True
        if vals.get('supervisor_id') or vals.get('privacy_visibilty') or vals.get('leadmanager_id'):
            for project in self.filtered(lambda project: project.privacy_visibility == 'followers'):
                project.message_subscribe(project.supervisor_id.ids)
                project.message_subscribe(project.leadmanager_id.ids)
                project.message_subscribe(project.Analyst_id.ids)
        return res

class StatusProcess(models.Model):
    _name='project.status'
    _description = "Project Status"
    _order = 'sequence, id'
    
    name = fields.Char(string='Status', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    status_id = fields.One2many('project.project','status_id', string="Status")
    
class ProjectCategory(models.Model):
    _name='project.category'
    _description = "Project Category"
    name = fields.Char(string='Category', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    category_id = fields.One2many('project.project', 'category_id', string="Catergory")

class ProjectPhase(models.Model):
    _name='project.phase'
    _description = "Project Phase"
    name = fields.Char(string='Phase', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    phase_id = fields.One2many('project.project', 'phase_id', string="Phase")


    