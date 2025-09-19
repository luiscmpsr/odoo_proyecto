from odoo import fields,models,api
from datetime import datetime
from odoo.exceptions import ValidationError

class TCUSolicitud(models.Model):
    _name = "tcu.solicitud"
    _description = "TCU Solicitud"
    
    sol_estudiante    = fields.Char(string="Nombre del Estudiante",    required=True)
    sol_periodo       = fields.Char(string="Periodo del TCU",          required=True)
    sol_lugar         = fields.Char(string="Lugar del TCU",            required=True)
    sol_encargado     = fields.Char(string="Encargado del Estudiante", required=True)
    sol_fecha         = fields.Date(string="Fecha de Solicitud",       required=True)
    sol_estado        = fields.Selection([
                                            ('pendiente', 'Pendiente'),
                                            ('revision',  'En Revisión'),
                                            ('aprobado',  'Aprobado'),
                                            ('rechazado', 'Rechazado'),
                                        ], string="Estado",            required=True)
    sol_observaciones = fields.Text(string="Observaciones",            required=True)
    sol_documentos    = fields.Many2many(
                                            'ir.attachment',
                                            'tcu_documento_rel',
                                            'doc_id', 'attach_id', 
                                            string="Documentos",       required=True)
    
    # Valido que el nombre del estudiante exista
    @api.constrains('sol_estudiante')
    def _check_estudiante_existente(self):
        for record in self:
            if record.sol_estudiante:
                # Busco en el modelo de estudiantes
                estudiante = self.env['tcu.estudiante'].search([('est_nombre', '=', record.sol_estudiante)], limit=1)
                if not estudiante:
                    raise ValidationError(
                        f"El estudiante '{record.sol_estudiante}' no existe en el registro de estudiantes."
                    )

    # Valido que el periodo exista
    @api.constrains('sol_periodo')
    def _check_estudiante_existente(self):
        for record in self:
            if record.sol_periodo:
                # Busco en el modelo de estudiantes
                periodo = self.env['tcu.periodo'].search([('per_nombre', '=', record.sol_periodo)], limit=1)
                if not periodo:
                    raise ValidationError(
                        f"El periodo '{record.sol_periodo}' no existe en el registro de periodos."
                    )
    
    # Valido que se haya subido al menos 1 documento
    @api.constrains('sol_documentos')
    def _check_al_menos_un_archivo(self):
        for record in self:
            if not record.sol_documentos:
                raise ValidationError("Se debe subir al menos un archivo para la solicitud.")
    
    # Se sobreescribe el write
    def write(self, vals):
        #raise ValidationError("Entre write")
        res = super(TCUSolicitud, self).write(vals)
        if 'sol_estado' in vals:
            #raise ValidationError("Entre IF")
            for record in self:
                nuevo_estado = vals['sol_estado']
                # Enviar correo
                record._send_estado_change_mail(nuevo_estado)
                
                # Hacer append al campo observaciones
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
                nuevo_texto = f"\n[{timestamp}] Estado cambiado a: {dict(record._fields['sol_estado'].selection).get(nuevo_estado)}"
                record.sol_observaciones = (record.sol_observaciones or "") + nuevo_texto
        #raise ValidationError("NO Entre IF")
        return res
    
    # Función que envía el correo
    def _send_estado_change_mail(self, nuevo_estado):
        template = self.env.ref('tcu_management.mail_template_estado', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)
        else:
            # fallback: correo rápido sin template
            mail_values = {
                'subject': f"Cambio de estado en la solicitud de {self.sol_estudiante}",
                'body_html': f"<p>El estado del registro cambió a <b>{nuevo_estado}</b></p>",
                'email_to': "luiscmpsr@gmail.com",
            }
            self.env['mail.mail'].create(mail_values).send()
