"""
TCC Grupo 6 - 2026S2
Backend Flask para o Sistema de Controle de Estoque de Madeiras
"""
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify
from flask_cors import CORS

from config import Config
from models import db, Madeira, Leitura, Alerta, Usuario


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)


def requer_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token != Config.API_TOKEN:
            return jsonify({"erro": "Token inválido ou ausente"}), 401
        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "servico": "TCC Grupo 6 - Controle de Estoque de Madeiras",
        "status": "online",
        "versao": "0.1.0",
    })


@app.route("/api/leituras", methods=["POST"])
@requer_token
def criar_leitura():
    dados = request.get_json(silent=True) or {}

    temperatura = dados.get("temperatura_c")
    umidade = dados.get("umidade_pct")

    if temperatura is None or umidade is None:
        return jsonify({"erro": "Campos 'temperatura_c' e 'umidade_pct' são obrigatórios"}), 400

    madeira_id = dados.get("madeira_id")
    if not madeira_id and dados.get("codigo_qr"):
        madeira = Madeira.query.filter_by(codigo_qr=dados["codigo_qr"]).first()
        if madeira:
            madeira_id = madeira.id

    leitura = Leitura(
        madeira_id=madeira_id,
        temperatura_c=float(temperatura),
        umidade_pct=float(umidade),
        origem=dados.get("origem", "esp32"),
        sincronizada=0 if dados.get("offline") else 1,
    )
    db.session.add(leitura)
    db.session.flush()

    alertas_gerados = _verificar_alertas(leitura)
    db.session.commit()

    return jsonify({
        "leitura": leitura.to_dict(),
        "alertas_gerados": [a.to_dict() for a in alertas_gerados],
    }), 201


def _verificar_alertas(leitura):
    alertas = []

    if leitura.temperatura_c < Config.TEMP_MIN:
        alertas.append(_criar_alerta(
            leitura, "temperatura", "aviso",
            f"Temperatura abaixo do mínimo: {leitura.temperatura_c}°C (mín: {Config.TEMP_MIN}°C)"
        ))
    elif leitura.temperatura_c > Config.TEMP_MAX:
        severidade = "critico" if leitura.temperatura_c > Config.TEMP_MAX + 5 else "aviso"
        alertas.append(_criar_alerta(
            leitura, "temperatura", severidade,
            f"Temperatura acima do máximo: {leitura.temperatura_c}°C (máx: {Config.TEMP_MAX}°C)"
        ))

    if leitura.umidade_pct < Config.UMIDADE_MIN:
        alertas.append(_criar_alerta(
            leitura, "umidade", "aviso",
            f"Umidade abaixo do mínimo: {leitura.umidade_pct}% (mín: {Config.UMIDADE_MIN}%)"
        ))
    elif leitura.umidade_pct > Config.UMIDADE_MAX:
        severidade = "critico" if leitura.umidade_pct > Config.UMIDADE_MAX + 10 else "aviso"
        alertas.append(_criar_alerta(
            leitura, "umidade", severidade,
            f"Umidade acima do máximo: {leitura.umidade_pct}% (máx: {Config.UMIDADE_MAX}%)"
        ))

    return alertas


def _criar_alerta(leitura, tipo, severidade, mensagem):
    alerta = Alerta(
        leitura_id=leitura.id,
        tipo=tipo,
        severidade=severidade,
        mensagem=mensagem,
    )
    db.session.add(alerta)
    return alerta


@app.route("/api/leituras", methods=["GET"])
def listar_leituras():
    query = Leitura.query

    madeira_id = request.args.get("madeira_id")
    if madeira_id:
        query = query.filter_by(madeira_id=int(madeira_id))

    desde = request.args.get("desde")
    if desde:
        try:
            dt = datetime.fromisoformat(desde)
            query = query.filter(Leitura.lida_em >= dt)
        except ValueError:
            return jsonify({"erro": "Formato de 'desde' inválido. Use ISO 8601"}), 400

    limite = min(int(request.args.get("limite", 100)), 1000)
    leituras = query.order_by(Leitura.lida_em.desc()).limit(limite).all()
    return jsonify([l.to_dict() for l in leituras])


@app.route("/api/leituras/ultima", methods=["GET"])
def ultima_leitura():
    leitura = Leitura.query.order_by(Leitura.lida_em.desc()).first()
    if not leitura:
        return jsonify({"mensagem": "Nenhuma leitura registrada ainda"}), 404
    return jsonify(leitura.to_dict())


@app.route("/api/madeiras", methods=["GET"])
def listar_madeiras():
    madeiras = Madeira.query.order_by(Madeira.criado_em.desc()).all()
    return jsonify([m.to_dict() for m in madeiras])


@app.route("/api/madeiras/<int:madeira_id>", methods=["GET"])
def obter_madeira(madeira_id):
    madeira = Madeira.query.get_or_404(madeira_id)
    return jsonify(madeira.to_dict())


@app.route("/api/madeiras", methods=["POST"])
def criar_madeira():
    dados = request.get_json(silent=True) or {}

    if not dados.get("codigo_qr") or not dados.get("especie"):
        return jsonify({"erro": "Campos 'codigo_qr' e 'especie' são obrigatórios"}), 400

    if Madeira.query.filter_by(codigo_qr=dados["codigo_qr"]).first():
        return jsonify({"erro": "Já existe uma madeira com esse código_qr"}), 409

    madeira = Madeira(
        codigo_qr=dados["codigo_qr"],
        especie=dados["especie"],
        descricao=dados.get("descricao"),
        fornecedor=dados.get("fornecedor"),
        procedencia=dados.get("procedencia"),
        certificacao=dados.get("certificacao"),
        data_extracao=_parse_data(dados.get("data_extracao")),
        data_entrada=_parse_data(dados.get("data_entrada")) or datetime.utcnow().date(),
        massa_inicial_g=dados.get("massa_inicial_g"),
        massa_atual_g=dados.get("massa_inicial_g"),
        status=dados.get("status", "em_estoque"),
    )
    db.session.add(madeira)
    db.session.commit()
    return jsonify(madeira.to_dict()), 201


def _parse_data(valor):
    if not valor:
        return None
    try:
        return datetime.fromisoformat(valor).date()
    except ValueError:
        return None


@app.route("/api/alertas", methods=["GET"])
def listar_alertas():
    apenas_ativos = request.args.get("ativos", "true").lower() == "true"
    query = Alerta.query
    if apenas_ativos:
        query = query.filter_by(resolvido=0)
    alertas = query.order_by(Alerta.criado_em.desc()).limit(200).all()
    return jsonify([a.to_dict() for a in alertas])


@app.route("/api/alertas/<int:alerta_id>/resolver", methods=["PUT"])
def resolver_alerta(alerta_id):
    alerta = Alerta.query.get_or_404(alerta_id)
    alerta.resolvido = 1
    alerta.resolvido_em = datetime.utcnow()
    db.session.commit()
    return jsonify(alerta.to_dict())


@app.route("/api/estatisticas", methods=["GET"])
def estatisticas():
    total_madeiras = Madeira.query.count()
    total_leituras = Leitura.query.count()
    alertas_ativos = Alerta.query.filter_by(resolvido=0).count()
    ultimas_24h = datetime.utcnow() - timedelta(hours=24)
    leituras_24h = Leitura.query.filter(Leitura.lida_em >= ultimas_24h).count()

    return jsonify({
        "total_madeiras": total_madeiras,
        "total_leituras": total_leituras,
        "alertas_ativos": alertas_ativos,
        "leituras_ultimas_24h": leituras_24h,
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Banco de dados inicializado.")
        print(f"Servidor rodando em http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
