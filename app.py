import os
from flask import (
    Flask,
    request,
    jsonify,
    abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Nutritionist, Client, Subscription, Article, db
from datetime import datetime
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def get_initial():
        return jsonify({
            'val': 'Halos'
        })
        
        

    '''
    ROUTES FOR NUTRITIONISTS
    Create, View, and Edit Nutritonist
    '''

    # View all nutritionist
    @app.route('/nutritionists', methods=['GET'])
    @requires_auth('view:nutritionist')
    def get_all_nutritionist(jwt):
        try:
            qr = Nutritionist.query.with_entities(
                Nutritionist.id, Nutritionist.name).all()
            nutritionists = [{'id': user.id, 'name': user.name}
                                 for user in qr] if qr else []
            return jsonify({
                'success': True,
                'data': nutritionists
            })
        except Exception as e:
            abort(404)
            return jsonify({
                'success': False,
                'message': 'users not found'
            }), 404
            

    # Create nutritionist
    @app.route('/nutritionists', methods=['POST'])
    @requires_auth('create:nutritionist')
    def create_nutritionist(jwt):
        data = request.get_json()
        try:
            name = data.get('name')
            specialization = data.get('specialization')
            email = data.get('email')

            if not name or not specialization or not email:
                abort(412)
                return jsonify({
                    'success': False,
                    'message': 'required fields expected'
                }), 412
            else:
                nutritionist = Nutritionist(
                    name=name, specialization=specialization, email=email, rating=0)
                nutritionist.insert()
                return jsonify({
                    'success': True,
                    'email': email,
                    'message': 'Nutritionist Created',
                })
        except Exception:
            abort(422)
            
        
    # Update nutritionist
    @app.route('/nutritionists', methods=['PATCH'])
    @requires_auth('edit:nutritionist')
    def update_nutritionist(jwt):
        data = request.get_json()
        id = data.get('id')
        try:
            nutritionist = Nutritionist.query.get(id)

            if nutritionist:
                if data.get('rating'):
                    nutritionist.rating = data.get('rating') if data.get(
                        'rating') else nutritionist.rating
                else:
                    nutritionist.name = data.get('name') if data.get(
                        'name') else nutritionist.name
                    nutritionist.specialization = data.get('specialization') if data.get(
                        'specialization') else nutritionist.name
                    nutritionist.email = data.get('email') if data.get(
                        'email') else nutritionist.email

                nutritionist.update()
                return jsonify({
                    'success': True,
                    'id': id,
                    'message': 'user data updated'
                })
            else:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'user not found'
                })
        except Exception:
            abort(422)
     
            
    # Get specific nutritionist
    @app.route('/nutritionists/<int:id>')
    @requires_auth('view:nutritionist')
    def get_nutritionist(jwt, id):
        try:
            qr = Nutritionist.query.get(id)
            if qr:
                return jsonify({
                    'success': True,
                    'data': qr.format()
                })
            else:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'user not found.'
                })
        except:
            abort(404)

    
    
    '''
    ROUTES FOR CLIENTS
    Create, View, and Edit Clients
    '''

    # Get all clients
    @app.route('/clients', methods=['GET'])
    @requires_auth('view:client')
    def get_all_client(jwt):
        try:
            qr = Client.query.with_entities(Client.id, Client.name).all()
            clients = [{'id': user.id, 'name': user.name}
                        for user in qr] if qr else []
            return jsonify({
                'success': True,
                'data': clients
            })

        except Exception as e:
            print(e)
            abort(404)
            
            
    # Create client    
    @app.route('/clients', methods=['POST'])
    @requires_auth('create:client')
    def create_client(jwt):
        data = request.get_json()
        name = data.get('name')
        country = data.get('country')
        email = data.get('email')

        if not name or not country or not email:
            abort(412)
            return jsonify({
                'success': False,
                'message': 'required fields expected'
            }), 412
        else:
            try:
                client = Client(name=name, country=country, email=email)
                client.insert()
                return jsonify({
                    'success': True,
                    'email': email,
                    'message': 'client created'
                })
            except Exception as e:
                abort(422)
                
                
    
    # Update Client    
    @app.route('/clients', methods=['PATCH'])
    @requires_auth('edit:client')
    def edit_client(jwt):
        data = request.get_json()
        id = data.get('id')
        try:
            client = Client.query.get(id)
            if client:
                client.name = data.get('name') if data.get(
                    'name') else client.name
                client.country = data.get('country') if data.get(
                    'country') else client.country
                client.email = data.get('email') if data.get(
                    'email') else client.email

                client.update()
                return jsonify({
                    'success': True,
                    'id': id,
                    'message': 'User data updated'
                })
            else:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'user not found'
                })
        except Exception:
            abort(422)
            

    # Get specific client
    @app.route('/clients/<int:id>')
    @requires_auth('view:client')
    def get_client(jwt, id):
        try:
            qr = Client.query.get(id)
            if qr:
                return jsonify({
                    'success': True,
                    'data': qr.format()
                })
            else:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'user not found.'
                }), 404
        except Exception:
            abort(404)



    '''
    ROUTES FOR ARTICLES
    Create, Update, Edit, Delete articles
    '''

    '''
        View articles created by nutritionist by passing nutritionist_id as params
        View articles subscribed by clients by passing client_id as params
    '''
    @app.route('/articles')
    @requires_auth('read:article')
    def get_articles(jwt):
        client_id = request.args.get('client_id')
        nutritionist_id = request.args.get('nutritionist_id')
        if client_id:
            try:
                qr = Article.query.join(Nutritionist).join(Subscription).join(Client).filter(
                    Article.nutritionist_id == Subscription.nutritionist_id,
                    Client.id == Subscription.client_id,
                    Subscription.client_id == client_id
                ).all()
                result = [article.format() for article in qr] if qr else []
                return jsonify({
                    'success': True,
                    'data': result
                })
            except Exception:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'data not found'
                }), 404

        if nutritionist_id:
            try:
                qr = Article.query.join(Nutritionist).filter(
                    Article.nutritionist_id == Nutritionist.id,
                    Nutritionist.id == nutritionist_id
                ).all()

                result = [article.format() for article in qr] if qr else []
                return jsonify({
                    'success': True,
                    'data': result
                })
            except Exception as e:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'data not found'
                }), 404

        else:
            try:
                qr = Article.query.all()
                formated_data = [article.format()
                                for article in qr] if qr else []
                return jsonify({
                    'success': True,
                    'data': formated_data
                })
            except Exception as e:
                abort(404)
                return jsonify({
                    'success': False,
                    'message': 'data not found'
                }), 404
                
                
    # Create articles
    @app.route('/articles', methods=['POST'])
    @requires_auth('create:article')
    def create_articles(jwt):
        data = request.get_json()
        title = data.get('title')
        date_created = datetime.now()
        content = data.get('content')
        nutritionist_id = data.get('nutritionist')

        if not title or not content or not nutritionist_id:
            abort(412)
            return jsonify({
                'success': False,
                'message': 'required fields expected'
            }), 412
        else:
            try:
                author = Nutritionist.query.get(nutritionist_id)
                if author:
                    article = Article(
                        title=title, date_created=date_created, content=content, nutritionist_id=author.id)
                    print(article)
                    article.insert()
                    return jsonify({
                        'success': True,
                        'message': 'Article created'
                    })
                else:
                    abort(404)
                    return jsonify({
                        'success': False,
                        'message': 'Nutritionist selected not found.'
                    }), 404
            except Exception as e:
                abort(422)
                
                
    # Update articles
    @app.route('/articles', methods=['PATCH'])
    @requires_auth('edit:article')
    def edit_articles(jwt):
        data = request.get_json()
        article_id = data.get('id')
        print(article_id)
        try:
            article = Article.query.get(article_id)
            if article:
                article.title = data.get(
                    'title') if data.get('title') else article.title
                article.date_created = datetime.now()
                article.content = data.get('content') if data.get(
                    'content') else article.content
                article.nutritionist_id = data.get('nutritionist') if data.get(
                    'nutritionist') else article.nutritionist_id

                article.update()
                return jsonify({
                    'success': True,
                    'id': article_id,
                    'message': 'Article Updated.'
                })
            else:
                abort(422)
                return jsonify({
                    'success': False,
                    'message': 'Article not found.'
                }), 422
        except Exception as e:
            abort(422)
            

    # Delete Article
    @app.route('/articles/<int:article_id>', methods=['DELETE'])
    @requires_auth('delete:article')
    def delete_article(jwt, article_id):
        try:
            article = Article.query.get(article_id)
            if article:
                article.delete()
                return jsonify({
                    'success': True,
                    'id': article_id
                })
            else:
                abort(422)
                return jsonify({
                    'success': False,
                    'message': 'Article not found'
                })
        except Exception:
            abort(422)

    
    '''
    Subscribe Client to nutritionist
    Post with client_id and nutritionist_id
    '''

    # Subscribe Client to Nutritionist
    @app.route('/subscriptions', methods=['POST'])
    @requires_auth('subscribe:client')
    def subscription(jwt):
        data = request.get_json()
        method = request.method

        if method == 'POST':
            nutritionist_id = data.get('nutritionist_id')
            client_id = data.get('client_id')
            subscription_status = True
            
            check_nutritionist = Nutritionist.query.get(nutritionist_id)
            check_client = Client.query.get(client_id)
            
            subscription_check = Subscription.query.filter(
                Subscription.client_id == client_id, Subscription.nutritionist_id == nutritionist_id).all()

            if not check_nutritionist or not check_client or not subscription_status:
                abort(412)
                return jsonify({
                    'success': False,
                    'message': 'provide accurate data for required fields'
                }), 412
            elif subscription_check:
                abort(422)
                return jsonify({
                    'success': False,
                    'message': 'Client already subscribed to this nutritionist'
                }), 422
            else:
                try:
                    subscription = Subscription(
                        nutritionist_id=nutritionist_id, client_id=client_id, subscription_status=subscription_status)
                    subscription.insert()

                    return jsonify({
                        'success': True,
                        'message': 'Client subscription added'
                    })

                except Exception:
                    abort(422)
                    
    '''
        HANDLE APP ERRORS
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(412)
    def precondition_failed(error):
        return jsonify({
            'success': False,
            'error': 412,
            'message': 'precondition failed'
        }), 412

    @app.errorhandler(422)
    def unprocessed_request(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessed request'
        }), 422
        
    @app.errorhandler(405)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

        
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
