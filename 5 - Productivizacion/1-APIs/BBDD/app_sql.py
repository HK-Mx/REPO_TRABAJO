from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd

churro = "sqlite:///books.db"
engine = create_engine(churro)


app = Flask(__name__)
app.config["DEBUG"] = True

def suma(a,b):
    return a+b


@app.route('/', methods=['GET'])
def home():
    print("la suma de 2+3 =", suma(2,3))
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros
@app.route('/api/v0/resources/books/all', methods=['GET'])
def get_all():
    query = """
    SELECT * FROM books
    """
    return pd.read_sql(query, con=engine).to_dict(orient="records")

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
@app.route('/api/v0/resources/book', methods=['GET'])
def book_id():
    
    if 'id' in request.args:
        id = int(request.args['id'])
        query = f"""
        SELECT * FROM books
        WHERE id = {id}
        """
        return pd.read_sql(query, con=engine).to_dict(orient="records")


    else:
        return "No id field provided"


# 3.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada de otra forma
@app.route('/api/v0/resources/book/<string:title>', methods=['POST'])
def book_title(title):
    
    if 'title' in request.args:
        title = request.args['title']
        query = f"""
        SELECT * FROM books
        WHERE title = {title}
        """
        return pd.read_sql(query, con=engine).to_dict(orient="records")


    else:
        return "No title field provided"



# 4.Ruta para obtener un libro concreto mediante su título dentro del cuerpo de la llamada
@app.route('/api/v1/resources/book', methods=['GET'])
def book_title_body():
    
    if "title" in request.get_json():

        title = request.get_json()["title"]
        
        query = f"""
        SELECT * FROM books
        WHERE title = {title}
        """
        return pd.read_sql(query, con=engine).to_dict(orient="records")


    else:
        return "No title field provided"


# 5.Ruta para añadir un libro mediante parámetros en la llamada
@app.route('/api/v1/resources/book/add', methods=['POST'])
def add_book():
    new_book = request.get_json()
    books.append(new_book)
    return jsonify(books)



# # 6.Ruta para añadir un libro de otra forma 1
# # @app.route('/api/v1/resources/book/add_parameters', methods=['POST'])
# @app.route('/api/v1/resources/book/add', methods=['POST'])
# def add_book():
#     new_book = request.args
#     books.append(new_book)
#     return jsonify(books)



# 7.Ruta para modificar un libro
@app.route('/api/v1/resources/book/update', methods=['PUT'])
def put_book():

    new_book = request.get_json()
    if "id" in new_book:
        id = int(new_book["id"])
        for idx, book in enumerate(books):
            if book["id"] == id:
                books[idx] = new_book
                return jsonify(books)
        return "no book found"
    else:
        return "no id field found"



# 8.Ruta para eliminar un libro
@app.route('/api/v1/resources/book/delete', methods=['DELETE'])

def delete_book(): 
    payload = request.get_json()
    if "id" in payload:
        id = int(payload["id"])

        query = f"""
                SELECT * FROM books
                """
        books = pd.read_sql(query, con=engine)
            
        mask = books.id == id
        index = books.loc[mask,:].index[0]
        new_df = books.drop(index)

        new_df.to_sql("books", index=None, con= engine, if_exist="replace")

        return new_df.to_dict(orient="records")
            
app.run()