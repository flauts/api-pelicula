import boto3
import uuid
import os

def lambda_handler(event, context):
    # Entrada (json)
    print(event) # Log json en CloudWatch
    try:
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
    except KeyError as e:
        error = { 
            "tipo" : "ERROR",
            "log_datos": event["body"]
        }
        print(error)
        return {
            'statusCode': 400,
            'error': f"Error: {str(e)}",
            'message': "tenant_id y pelicula_datos son requeridos"
        }
    # Proceso
    uuidv4 = str(uuid.uuid4())
    pelicula = {
        'tenant_id': tenant_id,
        'uuid': uuidv4,
        'pelicula_datos': pelicula_datos
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=pelicula)
    # Salida (json)
    info = {
        "tipo" : "INFO",
        "log_datos": pelicula
    }
    print(info)
    # print(pelicula) # Log json en CloudWatch
    return {
        'statusCode': 200,
        'pelicula': pelicula,
        'response': response
    }
