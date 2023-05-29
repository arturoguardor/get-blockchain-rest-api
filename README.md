# get-blockchain-rest-api
Aplicación que lee los datos de la API de Blockchain.com y expone información sobre estos datos a través de una API REST.

Vamos a leer los datos de la API de Blockchain.com cuya documentación está disponible aquí:
https://api.blockchain.com/v3/

Concretamente leeremos los datos de la llamada GET /l3/{symbol}.

Todas las llamadas REST devolverán los datos en formato JSON.

## Funcionalidades

1. GET:/

    Mensaje de bienvenida de la API

2. GET:/l3

    El usuario puede obtener las siguientes estadísticas del libro de órdenes L3 para todos los símbolos disponibles:

    - Número de órdenes de compra.
    - Número de órdenes de venta.
    - Valor total de las órdenes de compra.
    - Valor total de las órdenes de venta.
    - El total de monedas de las órdenes de compra.
    - El total de monedas de las órdenes de venta.

    Un ejemplo de la salida:
      ```json
      {
        "BTC-USD": {
          "bids": {
            "count": 500,
            "qty": 45,
            "value": 150000.00
          },
          "asks": {
            "count": 500,
            "qty": 500,
            "value": 450000
          }
        }
      }
      ```

3. GET:/l3/symbol

    El usuario puede obtener los datos del libro de órdenes L3 para un símbolo, indicando un símbolo compuesto de una criptomoneda y una moneda real (e.g. "BTC-USD").

4. GET:/l3/symbol/bids/

    El usuario puede obtener las siguientes estadísticas de las órdenes de compra (bids) del libro de órdenes L3 para el símbolo indicado:

    - El valor medio de las órdenes, donde el valor es la cantidad de la orden multiplicado por su precio.
    - La orden de compra con mayor valor.
    - La orden de compra con menor valor.
    - El total de monedas en órdenes.
    - El precio total de las órdenes.

    Un ejemplo de la salida:
      ```json
      {
        "bids": {
          "average_value": 10.25,
          "greater_value": {
            "px": 31790.42,
            "qty": 1.25824063,
            "num": 16484191171,
            "value": 40000.00
          },
          "lesser_value": {
            "px": 31777,
            "qty": 0.05,
            "num": 16484191502,
            "value": 1588.85
          },
          "total_qty": 40.12,
          "total_px": 154600
        }
      }
      ```

3. GET:/l3/symbol/asks/

   El usuario puede obtener las mismas estadísticas anteriores pero de las órdenes de venta (asks) del libro de órdenes L3 para el símbolo indicado.
  
