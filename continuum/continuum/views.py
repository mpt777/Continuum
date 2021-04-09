from django.shortcuts import render
import os
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
import matplotlib.pyplot as plt

from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
import subprocess

import continuum
import sys

import shutil
# insert at 1, 0 is the script path (or '' in REPL)

@csrf_protect

def home(request):
    response = {}
    if(request.method == "POST"):
        
        for f in os.listdir("media/uploadedfiles"):
            os.remove(os.path.join("media/uploadedfiles", f))
            
        for f in os.listdir("media/outputfiles"):
            os.remove(os.path.join("media/outputfiles", f))
  
        for f in os.listdir("media/json-data"):
            os.remove(os.path.join("media/json-data", f))
        
        if ('filename' in request.FILES): # User Form
            f=request.FILES['filename'] # here you get the files needed
            f_name = request.FILES['filename'].name
            model=request.POST.get('models')
            
            if '.zip' in f_name:
                file_name = "pic.zip"
                file_name_2 = default_storage.save("uploadedfiles/"+file_name, f)
                file_url = default_storage.url(file_name_2)
                shutil.unpack_archive('media/uploadedfiles/pic.zip') 
                
            else:
                file_name = f_name
                file_name_2 = default_storage.save("uploadedfiles/"+file_name, f)
                file_url = default_storage.url(file_name_2)
                
            command_string = 'python yolov5/detect_continuum.py --source media/uploadedfiles/ --weights media/yolov5-models/{}/best.pt --project media/outputfiles --name outputfiles'.format(model)
            
            if(request.POST.get('conf')):
                command_string += " --conf-thres {}".format(request.POST.get('conf'))
            
            if(request.POST.get('iou')):
                command_string += " --iou-thres {}".format(request.POST.get('iou'))
                
            subprocess.call(command_string, shell=True)
            response['image'] = file_name
            response['json'] = 'true'
            response['image_name'] = os.path.splitext(f_name)[0]
            
            if '.zip' in f_name:
                shutil.make_archive('media/outputfiles/'+model+'_images', 'zip', 'media/outputfiles')
                shutil.make_archive('media/json-data/'+model+'_annotations', 'zip', 'media/json-data')
                response['zip'] = True
                response['model'] = model
            
            
            
        if (request.POST.get('modelname') and 'modelbest' in request.FILES): #Admin Form
            
            model_name=request.POST.get('modelname')
            model_best=request.FILES['modelbest']
            
            os.mkdir("media/yolov5-models/{}".format(model_name))
            file_name = "best.pt"
            x = "yolov5-models/{}/".format(model_name)
            file_name_models = default_storage.save(x+file_name, model_best)
            file_url = default_storage.url(file_name_models)
            response['modelname'] = model_name
        
        
        
        response['anchor'] = 'model-results'
        response['models'] = os.listdir('media/yolov5-models/')
        
        return render(request, 'continuum.html', response)
    else:
        response['models'] = os.listdir('media/yolov5-models/')
        return render(request, 'continuum.html', response)