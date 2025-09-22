from odoo import http
from odoo.http import request
import base64

class TCUSolicitudController(http.Controller):

    @http.route('/api/create_solicitud_api', type='http', auth='public', methods=['POST'], csrf=False)
    def create_solicitud(self, **kwargs):
        try:
            sol_estudiante    = kwargs.get('sol_estudiante')
            sol_periodo       = kwargs.get('sol_periodo')
            sol_lugar         = kwargs.get('sol_lugar')
            sol_encargado     = kwargs.get('sol_encargado')
            sol_fecha         = kwargs.get('sol_fecha')
            sol_estado        = kwargs.get('sol_estado')
            sol_observaciones = kwargs.get('sol_observaciones')

            # Validar campos requeridos
            if not all([sol_estudiante, sol_periodo, sol_lugar, sol_encargado, sol_fecha, sol_estado, sol_observaciones]):
                # Construir mensaje con cada valor recibido
                detalle = (
                    f"sol_estudiante=   '{sol_estudiante}', "
                    f"sol_periodo=      '{sol_periodo}', "
                    f"sol_lugar=        '{sol_lugar}', "
                    f"sol_encargado=    '{sol_encargado}', "
                    f"sol_fecha=        '{sol_fecha}', "
                    f"sol_estado=       '{sol_estado}', "
                    f"sol_observaciones='{sol_observaciones}'"
                )
                return request.make_json_response(
                    {"error": "Faltan campos requeridos.", "detalle": detalle},
                    status=400
                )

            # Procesar los archivos que se van a adjuntar a la solicitud
            #archivos_ids = []
            #for key, file in request.httprequest.files.items():
            #    file_content = file.read()
            #    attachment = request.env['ir.attachment'].sudo().create({
            #        'name': file.filename,
            #        'datas': base64.b64encode(file_content),
            #        'res_model': 'tcu.solicitud',
            #        'type': 'binary',
            #        'mimetype': file.mimetype,
            #    })
            #    archivos_ids.append(attachment.id)

            # Crear la solicitud
            solicitud = request.env['tcu.solicitud'].sudo().create({
                'sol_estudiante'   : sol_estudiante,
                'sol_periodo'      : sol_periodo,
                'sol_lugar'        : sol_lugar,
                'sol_encargado'    : sol_encargado,
                'sol_fecha'        : sol_fecha,
                'sol_estado'       : sol_estado,
                'sol_observaciones': sol_observaciones,
                #'sol_documentos'   : [(6, 0, archivos_ids)] if archivos_ids else False
            })

            return request.make_json_response({
                "success": True,
                "id": solicitud.id,
                "message": "Solicitud creada correctamente"
            })

        except Exception as e:
            return request.make_json_response({"error": str(e)}, status=500)
