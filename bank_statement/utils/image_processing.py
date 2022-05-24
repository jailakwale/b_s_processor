import pdf2image
#import cv2
import os

def safe_convert(filename, out, folder):
    '''
    converts pdf to image. be careful : out is the filename without extension and without folder info (=basename), 
    folder is the full destination path
    the function saves the generated image to disk.
    '''
    assert os.path.exists(filename)
    my_im = pdf2image.convert_from_path(filename,
                                        output_folder = folder, 
                                        last_page= 1, 
                                        output_file= out, 
                                        paths_only= True, 
                                        fmt='jpg')
    return my_im

def convert_pdf_2_im(folder, basename):
    '''
    image conversion given a basename and destination folder (fully defined)
    '''
    full_filename = os.path.join(folder, basename)
    
    out = full_filename.split(".pdf")[0].split("/")[-1]
    safe_convert(full_filename, out, folder)

def read_image_crop(folder, image_path, crop=250):
    '''
    the function crops the right upper corner of an image
    '''
    my_im = cv2.imread(os.path.join(folder, image_path))
    my_im_RGB = cv2.cvtColor(my_im, cv2.COLOR_BGR2RGB)
    return my_im_RGB[:250,-250:]