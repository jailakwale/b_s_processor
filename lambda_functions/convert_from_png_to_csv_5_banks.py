import os
import json
import shutil

import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import glob2
import requests
import base64
from zipfile import ZipFile
from tqdm import tqdm


def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if (".zip" in el)][0]
    os.makedirs('/tmp', exist_ok=True)
    
    # open a file to dump the stream in
    print(r)
    print(file_name)
    
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    print(os.stat(f'/tmp/{file_name}').st_size)
    
    with ZipFile(f'/tmp/{file_name}', 'r') as zip:
        # extracting all the files
        print(zip.namelist())
        os.makedirs(f'/tmp/all_png/{file_name}', exist_ok=True)
        os.chdir('/tmp/all_png')

        for file_zip in zip.namelist():
            zip.extract(file_zip, '/tmp/all_png')
            print('Extracting all the files now...')
        print("double nested :\n")
        print(glob2.glob('/tmp/all_png/*/*.png'))
        
    return '/tmp/all_png'

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text


def get_table_csv_results(file_name):
 
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    # process using image bytes
    # get the results
    client = boto3.client('textract',region_name="eu-west-1")

    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])

    # Get the text blocks
    blocks=response['Blocks']
    #pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv_list = []
    for index, table in enumerate(table_blocks):
        csv_list.append(generate_table_csv(table, blocks_map, index +1))
    return csv_list

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = ''

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'
    return csv

def png_2_csv(file_name, out):
    table_csv_list = get_table_csv_results(file_name)

    # replace content
    for idx, table_csv in enumerate(table_csv_list):
        print(idx)
        new_file_name = file_name.replace(".png", f"sub_{str(idx)}.csv")
        
        with open(new_file_name, "wt") as fout:
            fout.write(table_csv)
    
        s3_client = boto3.client('s3', region_name='eu-west-1')
        
        try:
            
            radical_name = file_name.split("/")[-1].replace(".","_")
            suffix = new_file_name.split("/")[-1]
            object_name = f"job_{radical_name}/{suffix}"
            bucket = out
            response = s3_client.upload_file(new_file_name, bucket, object_name)
            zipObj = ZipFile('/tmp/sample.zip', 'a')
            zipObj.write(new_file_name)
            zipObj.close()
            result = object_name

        except Exception as e:
            response = None
            result = "failed transaction"
            print(str(e))
            pass
    return result
            
def parse(f_path,out):
    all_files = glob2.glob(os.path.join(f_path, "*/*.png"))
    paths = []
    for file_name in tqdm(all_files):
        paths.append(png_2_csv(file_name,out))
        
    return paths

def png2csv_liberta_leasing_convert_handler(event, context):
    
    if "body" in event.keys():
        event = json.loads(event["body"])
        
    input_file_url = event["url"]
    output_format = event["format"]
    output_bucket= event["output_bucket"]
    f_path = download_url(input_file_url)

    try:
        # when no error :process and returns json
        s3_client = boto3.client('s3', region_name='eu-west-1')
        try:
            s3_client.create_bucket(Bucket=output_bucket)
        except:
            pass
        
        dest_file = parse(f_path, out=output_bucket)
        
        s3_client = boto3.client('s3', region_name='eu-west-1')
        response = s3_client.upload_file("/tmp/sample.zip", output_bucket, "compressed_csv.zip")
        
        
        return {'headers': {'Content-Type':'application/json'}, 
        'statusCode': 200,
        'body': json.dumps(str(dest_file))}

    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
        'statusCode': 400,
        'body': json.dumps(str(e))}
