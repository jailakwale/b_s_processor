# Download base image lambda python v.3.9 
FROM amazon/aws-lambda-python:3.9
WORKDIR /home/ubuntu
RUN yum update && yum install poppler-utils make curl wget sudo nano git gcc-c++ libgl1 libgl1-mesa-glx mesa-libGL ffmpeg libsm6 libxext6 -y
RUN pip3 install pandas boto3 tqdm opencv-python Pillow glob2 requests scikit-learn zipfile38 PyPDF2 pdf2image requests zipfile38 openpyxl --target "${LAMBDA_TASK_ROOT}"

# Necessary to put ourselves in the folder ("${LAMBDA_TASK_ROOT}")
# and to copy the python file where the handler function is located
WORKDIR "${LAMBDA_TASK_ROOT}"
RUN git clone https://github.com/assansanogo/b_s_processor.git
RUN ls "${LAMBDA_TASK_ROOT}"/b_s_processor/lambda_functions
RUN cp  "${LAMBDA_TASK_ROOT}"/b_s_processor/lambda_functions/step1_convert_to_png/extraction/convert_from_pdf_to_png_5_banks.py "${LAMBDA_TASK_ROOT}"
RUN ls "${LAMBDA_TASK_ROOT}"

CMD ["convert_from_pdf_to_png_5_banks.convert_from_pdf_2_csv_handler"]
