import wol
import json
from flask import request
from app_factory import create_app

app = create_app(__name__)


@app.route('/help', methods=['GET'])
def help():
    return json.dumps({'help message': wol.help_message().strip()})


@app.route('/ports', methods=['GET'])
def get_wol_ports():
    return json.dumps({"ports": wol.get_wol_ports()})


@app.route('/wake/<string:mac_address>', methods=['GET'])
def wake(mac_address):
    try:
        args = request.args.to_dict()
        ip = args['ip'] if 'ip' in args else '192.168.1.255'
        port = args['port'] if 'port' in args else wol.get_wol_ports()[2]
        payload = wol.build_payload(mac_address)
        if app.config['DEBUG']:
            print 'Mac  :', mac_address
            print 'Ip   :', ip
            print 'Port :', port
        else:
            app.logger.info({
                'Mac': mac_address,
                'Ip': ip,
                'Port': port
            })
        wol.send(payload, ip, port)
        return json.dumps({"success": True})
    except Exception as e:
        app.logger.error(e.message)
        return json.dumps({"error": e.message})


if __name__ == "__main__":
    app.run()
