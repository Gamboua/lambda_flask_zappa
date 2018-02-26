from flask import Flask, Response, request
import rds_config
import pymysql
import json

app = Flask(__name__)

@app.route('/')
def index():
    return Response(json.dumps(
        {
            "status": "success"
        }
    ), status=200, mimetype='application/json')


@app.route('/callback/mercadolivre/', methods=['POST'])
def callback_mercadolivre():
    content = request.get_json(force=True)

    conn = pymysql.connect(rds_config.host, user=rds_config.user, passwd=rds_config.pswd, db=rds_config.base)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO notificacao_mercado_livre(user_id, resource, topic, received, sent) VALUES('%s', '%s', '%s', '%s', '%s')" % 
            content.get('user_id'),
            content.get('resource'),
            content.get('topic'),
            content.get('received'),
            content.get('sent')
        ) 
        conn.commit()
        
    return Response(json.dumps(
        content
    ), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()
