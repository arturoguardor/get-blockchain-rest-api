from flask import Flask, jsonify
import requests
import re
import numpy as np
import pandas as pd

app = Flask(__name__)

# Compilar una expresión regular para validar los símbolos de la API
rex = re.compile("^[a-zA-Z]{3,8}-[a-zA-Z]{3,8}$")


@app.errorhandler(400)
def bad_request(error):
    """Manejar errores de solicitud"""
    return jsonify({
        "code": 400,
        "status": "bad request"
        })


@app.errorhandler(404)
def not_found(error: int):
    """Manejar errores de solicitud"""
    return jsonify({
        "code": 404,
        "status": "not found"
        })


@app.errorhandler(405)
def method_not_allowed(error):
    """Manejar errores de solicitud"""
    return jsonify({
        "code": 405,
        "status": "method not allowed"
        })


@app.errorhandler(500)
def server_error(error):
    """Manejar errores de servidor"""
    return jsonify({
        "code": 500,
        "status": "internal server error"
        })


@app.route('/', methods=['GET'])
def welcome():
    """Mensaje de bienvenida de la API"""
    return jsonify({'message': 'Welcome to my Blockchain API where you find'
                    ' information about crypto coins and/or real coins.'})


@app.route('/l3/', methods=['GET'])
def l3():
    """Obtener estadísticas del libro de órdenes L3 para todos los símbolos
    disponibles"""

    try:
        # Obtener los datos de la API de Blockchain.com
        url = 'https://api.blockchain.com/v3/exchange/symbols'
        response_symbols = requests.get(url).json()

        # Extraer todos los símbolos de la respuesta de la API
        symbols = list(response_symbols.keys())

        # Obtener los datos de cada símbolo individualmente
        urls = [f'https://api.blockchain.com/v3/exchange/l3/{symbol}'
                for symbol in symbols]
        responses = (requests.get(url).json() for url in urls)

        # Convertir los datos de la API en un DataFrame de Pandas
        df = pd.DataFrame(responses)

        # Calcular las estadísticas necesarias utilizando NumPy y Pandas
        stats = {}
        for symbol in df['symbol'].unique():
            symbol_df = df[df['symbol'] == symbol]
            bids_qty = np.sum([x['qty'] for x in symbol_df['bids'].sum()])
            bids_px = np.sum([x['px'] for x in symbol_df['bids'].sum()])
            asks_qty = np.sum([x['qty'] for x in symbol_df['asks'].sum()])
            asks_px = np.sum([x['px'] for x in symbol_df['asks'].sum()])
            stats[symbol] = {
                'bids': {
                    'count': len(symbol_df['bids'].max()),
                    'qty': bids_qty,
                    'value': bids_qty * bids_px
                },
                'asks': {
                    'count': len(symbol_df['asks'].max()),
                    'qty': asks_qty,
                    'value': asks_qty * asks_px
                }
            }

        # Devolver los resultados como un objeto JSON
        return jsonify(stats)

    except requests.exceptions.RequestException:
        # Manejar cualquier excepción relacionada con la solicitud HTTP
        return server_error(500)


@app.route('/l3/<symbol>/', methods=['GET'])
def get_symbol(symbol):
    """Obtener estadísticas del libro de órdenes L3 para el símbolo indicado"""
    try:
        # Verificar que el símbolo esté en el formato correcto
        if not rex.match(symbol):
            return bad_request(400)

        url = (f"https://api.blockchain.com/v3/exchange/l3/{symbol.upper()}"
               )
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return response.json()

        return not_found(404)

    except requests.exceptions.RequestException:
        # Manejar cualquier excepción relacionada con la solicitud HTTP
        return server_error(500)


@app.route('/l3/<symbol>/bids/', methods=['GET'])
def get_symbol_bids(symbol):
    """Obtener estadísticas del libro de órdenes L3 para el símbolo indicado,
    solo para las ofertas (bids)"""
    try:

        # Verificar que el símbolo esté en el formato correcto
        if not rex.match(symbol):
            return bad_request(400)

        # print(str(symbol))
        url = (f"https://api.blockchain.com/v3/exchange/l3/{symbol.upper()}"
               )
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            return not_found(404)

        # Convertir los datos de las órdenes en un DataFrame de Pandas
        bids_df = pd.DataFrame(response.json()['bids'])

        # Calcular las estadísticas necesarias utilizando NumPy y Pandas
        total_qty = np.sum(bids_df['qty'])
        total_px = np.sum(bids_df['px'] * bids_df['qty'])
        average_value = total_px / total_qty
        greater_value = bids_df.loc[
            (bids_df['px'] * bids_df['qty']).idxmax()]
        lesser_value = bids_df.loc[
            (bids_df['px'] * bids_df['qty']).idxmin()]

        # Devolver los resultados como un objeto JSON
        return {
            "bids": {
                "average_value": average_value,
                "greater_value": {
                    "px": float(greater_value['px']),
                    "qty": float(greater_value['qty']),
                    "num": int(greater_value['num']),
                    "value":
                    float(greater_value['px'])
                    * float(greater_value['qty'])
                },
                "lesser_value": {
                    "px": float(lesser_value['px']),
                    "qty": float(lesser_value['qty']),
                    "num": int(lesser_value['num']),
                    "value":
                    float(lesser_value['px'])
                    * float(lesser_value['qty'])
                },
                "total_qty": total_qty,
                "total_px": total_px
            }
        }
    except requests.exceptions.RequestException:
        # Manejar cualquier excepción relacionada con la solicitud HTTP
        return server_error(500)


@app.route('/l3/<symbol>/asks/', methods=['GET'])
def get_symbol_asks(symbol):
    """Obtener estadísticas del libro de órdenes L3 para el símbolo indicado,
    solo para las ofertas (asks)"""

    try:
        # Verificar que el símbolo esté en el formato correcto
        if not rex.match(symbol):
            return bad_request(400)

        url = (f"https://api.blockchain.com/v3/exchange/l3/{symbol.upper()}"
               )
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            return not_found(404)

        # Convertir los datos de las órdenes en un DataFrame de Pandas
        asks_df = pd.DataFrame(response.json()['asks'])

        # Calcular las estadísticas necesarias utilizando NumPy y Pandas
        total_qty = np.sum(asks_df['qty'])
        total_px = np.sum(asks_df['px'] * asks_df['qty'])
        average_value = total_px / total_qty
        greater_value = asks_df.loc[
            (asks_df['px'] * asks_df['qty']).idxmax()]
        lesser_value = asks_df.loc[
            (asks_df['px'] * asks_df['qty']).idxmin()]

        # Devolver los resultados como un objeto JSON
        return {
            "asks": {
                "average_value": average_value,
                "greater_value": {
                    "px": float(greater_value['px']),
                    "qty": float(greater_value['qty']),
                    "num": int(greater_value['num']),
                    "value":
                    float(greater_value['px'])
                    * float(greater_value['qty'])
                },
                "lesser_value": {
                    "px": float(lesser_value['px']),
                    "qty": float(lesser_value['qty']),
                    "num": int(lesser_value['num']),
                    "value":
                    float(lesser_value['px'])
                    * float(lesser_value['qty'])
                },
                "total_qty": total_qty,
                "total_px": total_px
            }
        }
    except requests.exceptions.RequestException:
        # Manejar cualquier excepción relacionada con la solicitud HTTP
        return server_error(500)


if __name__ == '__main__':
    app.run()
