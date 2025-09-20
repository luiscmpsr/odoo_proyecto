from odoo import http
from odoo.http import request, Response
import json

class EstudianteAPI(http.Controller):
    @http.route('/api/estudiante_api', type='http', auth='public', methods=['GET'], csrf=False)
    def get_estudiante(self, **kwargs):
        """
        /api/estudiante_api?identificacion=206050682
        /api/estudiante_api?nombre=Luis Campos R
        """
        est_identificacion = kwargs.get('identificacion')
        est_nombre         = kwargs.get('nombre')

        domain = []
        if est_identificacion:
            domain = [('est_identificacion', '=', est_identificacion)]
        elif est_nombre:
            domain = [('est_nombre', '=', est_nombre)]
        else:
            return json.dumps({"error": "Debe enviar la 'Identificacion' o 'Nombre' del estudiante como parámetro"})

        estudiante = request.env['tcu.estudiante'].sudo().search(domain, limit=1)

        if not estudiante:
            return json.dumps({"error": "Estudiante no encontrado"})

        data = {
            "est_nombre":         estudiante.est_nombre,
            "est_identificacion": estudiante.est_identificacion,
            "est_carnet":         estudiante.est_carnet,
            "est_correo":         estudiante.est_correo,
            "est_telefono":       estudiante.est_telefono,
        }

        #return json.dumps(data, ensure_ascii=False)
        return Response(
                    json.dumps(data, ensure_ascii=False),
                    content_type='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
        )