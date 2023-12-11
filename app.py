from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://arielangelm:Ariel447021@arielangelm.mysql.pythonanywhere-services.com/arielangelm$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(100))
    genero = db.Column(db.String(100))
    publicacion = db.Column(db.String(50))
    paginas = db.Column(db.Integer)

    def __init__(self, titulo, autor, genero, publicacion, paginas):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.publicacion = publicacion
        self.paginas = paginas


with app.app_context():
    db.create_all()


class LibroSchema(ma.Schema):
    class Meta:
        fields = ('id', 'titulo', 'autor', 'genero', 'publicacion', 'paginas')


libro_schema = LibroSchema()
libros_schema = LibroSchema(many=True)


@app.route('/libros', methods=['GET'])
def get_libros():
    all_libros = Libro.query.all()
    result = libros_schema.dump(all_libros)
    return jsonify(result)


@app.route('/libros/<id>', methods=['GET'])
def get_libro(id):
    libro = Libro.query.get(id)
    return libro_schema.jsonify(libro)


@app.route('/libros/<id>', methods=['DELETE'])
def delete_libro(id):
    libro = Libro.query.get(id)
    db.session.delete(libro)
    db.session.commit()
    return libro_schema.jsonify(libro)


@app.route('/libros', methods=['POST'])
def create_libro():
    titulo = request.json['titulo']
    autor = request.json['autor']
    genero = request.json['genero']
    publicacion = request.json['publicacion']
    paginas = request.json['paginas']
    new_libro = Libro(titulo, autor, genero, publicacion, paginas)
    db.session.add(new_libro)
    db.session.commit()
    return libro_schema.jsonify(new_libro)


@app.route('/libros/<id>', methods=['PUT'])
def update_libro(id):
    libro = Libro.query.get(id)

    titulo = request.json['titulo']
    autor = request.json['autor']
    genero = request.json['genero']
    publicacion = request.json['publicacion']
    paginas = request.json['paginas']

    libro.titulo = titulo
    libro.autor = autor
    libro.genero = genero
    libro.publicacion = publicacion
    libro.paginas = paginas

    db.session.commit()
    return libro_schema.jsonify(libro)

