"""Modelos do banco de dados (SQLAlchemy)."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil     = db.Column(db.String(20), default="luthier")
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email,
                "perfil": self.perfil,
                "criado_em": self.criado_em.isoformat() if self.criado_em else None}


class Madeira(db.Model):
    __tablename__ = "madeiras"
    id              = db.Column(db.Integer, primary_key=True)
    codigo_qr       = db.Column(db.String(120), unique=True, nullable=False)
    especie         = db.Column(db.String(120), nullable=False)
    descricao       = db.Column(db.Text)
    fornecedor      = db.Column(db.String(120))
    procedencia     = db.Column(db.String(120))
    certificacao    = db.Column(db.String(120))
    data_extracao   = db.Column(db.Date)
    data_entrada    = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    massa_inicial_g = db.Column(db.Float)
    massa_atual_g   = db.Column(db.Float)
    status          = db.Column(db.String(20), default="em_estoque")
    criado_em       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "codigo_qr": self.codigo_qr,
                "especie": self.especie, "descricao": self.descricao,
                "fornecedor": self.fornecedor, "procedencia": self.procedencia,
                "certificacao": self.certificacao,
                "data_extracao": self.data_extracao.isoformat() if self.data_extracao else None,
                "data_entrada": self.data_entrada.isoformat() if self.data_entrada else None,
                "massa_inicial_g": self.massa_inicial_g,
                "massa_atual_g": self.massa_atual_g,
                "status": self.status,
                "criado_em": self.criado_em.isoformat() if self.criado_em else None}


class Leitura(db.Model):
    __tablename__ = "leituras"
    id            = db.Column(db.Integer, primary_key=True)
    madeira_id    = db.Column(db.Integer, db.ForeignKey("madeiras.id"), nullable=True)
    temperatura_c = db.Column(db.Float, nullable=False)
    umidade_pct   = db.Column(db.Float, nullable=False)
    origem        = db.Column(db.String(20), default="esp32")
    lida_em       = db.Column(db.DateTime, default=datetime.utcnow)
    sincronizada  = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {"id": self.id, "madeira_id": self.madeira_id,
                "temperatura_c": self.temperatura_c,
                "umidade_pct": self.umidade_pct,
                "origem": self.origem,
                "lida_em": self.lida_em.isoformat() if self.lida_em else None,
                "sincronizada": bool(self.sincronizada)}


class Alerta(db.Model):
    __tablename__ = "alertas"
    id           = db.Column(db.Integer, primary_key=True)
    leitura_id   = db.Column(db.Integer, db.ForeignKey("leituras.id"), nullable=False)
    tipo         = db.Column(db.String(20), nullable=False)
    severidade   = db.Column(db.String(20), default="aviso")
    mensagem     = db.Column(db.Text, nullable=False)
    resolvido    = db.Column(db.Integer, default=0)
    criado_em    = db.Column(db.DateTime, default=datetime.utcnow)
    resolvido_em = db.Column(db.DateTime)

    def to_dict(self):
        return {"id": self.id, "leitura_id": self.leitura_id,
                "tipo": self.tipo, "severidade": self.severidade,
                "mensagem": self.mensagem,
                "resolvido": bool(self.resolvido),
                "criado_em": self.criado_em.isoformat() if self.criado_em else None,
                "resolvido_em": self.resolvido_em.isoformat() if self.resolvido_em else None}
