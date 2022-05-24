import PyPDF2
import tqdm
from pdf2image import convert_from_path, convert_from_bytes
from zipfile import ZipFile
import os
import glob2
import requests
import json
import boto3

def download_url(url):
    '''
    utility funcction which downloads pdf to local environment
    '''
    # data is going to be read as stream
    chunk_size=2000
    r = requests.get(url, stream=True)
    # the pdf filename is extracted from the presigned url
    file_name = [el for el in url.split("/") if ".pdf" in el][0]
    # open a file to dump the stream in
    with open(f'/tmp/{file_name}', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
    return f'/tmp/{file_name}'

def parse(my_pdf):
    reader = PyPDF2.PdfFileReader(my_pdf)
    n_pages = len(reader.pages)
    for i in tqdm.tqdm(range(n_pages)):
        writer = PyPDF2.PdfFileWriter()
        my_page = reader.getPage(i)
        writer.addPage(my_page)
        output_filename = my_pdf.replace('.pdf', f'_{str(i)}.pdf')
        new_dir = '/tmp'
        os.makedirs(new_dir, exist_ok=True)
        new_path = os.path.join(new_dir, output_filename)
        with open(new_path, 'wb') as output:
            writer.write(output)
        png_path = new_path.replace("pdf","png")
        img_test = convert_from_path(new_path)[0].save(png_path)
        
        os.chdir(new_dir)    
    all_png = glob2.glob(f"{new_dir}/*.png")
    
    for png_path in all_png :
        with ZipFile('my_bank_statement_png.zip','a') as zip:
            # writing each file one by one for file in png paths:
            zip.write(png_path)
            
    print(os.path.getsize('my_bank_statement_png.zip'))
    
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    
    LL_BUCKET = os.environ["BUCKET_DEST"]
    PREFIX = os.environ["PREFIX_DEST"]
    
    s3_client.upload_file('my_bank_statement_png.zip',LL_BUCKET ,f'{PREFIX}/my_bank_statement_png.zip')
    
    return 'my_bank_statement_png.zip'
          
          
def convert_from_pdf_2_csv_handler(event, context):
    event = json.loads(event["body"])
    
    input_file_url = event["url"]
    output_format = event["format"]
    f_path = download_url(input_file_url)
    
    try:
        # when no error :process and returns json
        dest_file = parse(f_path)
        # dest_file = str(event["url"])
        return {'headers': {'Content-Type':'application/json'}, 
        'statusCode': 200,
        'body': json.dumps(dest_file)}

    except Exception as e :
        # in case of errors return a json with the error description
        return {'headers': {'Content-Type':'application/json'}, 
        'statusCode': 400,
        'body': json.dumps(str(e))}
