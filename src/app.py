import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.calculator.parser import (
    DivisionByZeroError,
    InvalidExpressionError,
    evaluate_expression,
    format_decimal,
)
from src.db import (
    delete_history,
    init_db,
    insert_history,
    list_history,
)


def create_app():
    app = Flask(__name__)

    allowed_origins = os.environ.get(
        'ALLOWED_ORIGINS',
        '*'
    )

    CORS(app, resources={
        r'/api/*': {
            'origins': allowed_origins
        }
    })

    init_db()

    @app.get('/api/health')
    def health():
        return jsonify({
            'success': True,
            'message': 'Backend is running'
        })

    @app.post('/api/calculate')
    def calculate():
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                'success': False,
                'message': 'Request body must be JSON'
            }), 400

        expression = data.get('expression')

        if not isinstance(expression, str):
            return jsonify({
                'success': False,
                'message': 'Expression must be a string'
            }), 400

        expression = expression.strip()

        if expression == '':
            return jsonify({
                'success': False,
                'message': 'Expression cannot be empty'
            }), 400

        if len(expression) > 200:
            return jsonify({
                'success': False,
                'message': 'Expression is too long'
            }), 400

        try:
            value = evaluate_expression(expression)
            result = format_decimal(value)
        except DivisionByZeroError as error:
            return jsonify({
                'success': False,
                'message': str(error)
            }), 400
        except InvalidExpressionError as error:
            return jsonify({
                'success': False,
                'message': str(error)
            }), 400

        record = insert_history(expression, result)

        return jsonify({
            'success': True,
            'expression': expression,
            'result': result,
            'record': record
        }), 200

    @app.get('/api/history')
    def get_history():
        return jsonify({
            'success': True,
            'history': list_history()
        }), 200

    @app.delete('/api/history/<int:history_id>')
    def remove_history(history_id):
        deleted = delete_history(history_id)

        if not deleted:
            return jsonify({
                'success': False,
                'message': 'History record not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'History record deleted'
        }), 200

    return app


app = create_app()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', '5000')),
        debug=True
    )
