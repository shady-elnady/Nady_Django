from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from PIL import Image
#from keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import img_to_array
# from keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.python import ops
import cv2, os
import numpy as np
import re
import base64
from PIL import Image
import io
from django.conf import settings

from .models import Digit
from .forms import DigitForm


app_name = "Digit"


def to_internal_value(data):
    _format, str_img = data.split(";base64")
    decoded_file = base64.b64decode(str_img)
    data = ContentFile(decoded_file, name= "any.png")
    return data

def aiDigit(image):
    print(image)
    img = Image.open(image)
    img_array = img_to_array(img)
    # img_array = tf.keras.preprocessing.image.array_to_img(img)
    print(img_array)
    print(img_array.shape)
    new_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    dim = (28, 28)
    resized = cv2.resize(new_img, dim, interpolation= cv2.INTER_AREA)
    print(resized.shape)
    ready = np.expand_dims(resized, axis=2)
    ready = np.expand_dims(ready, axis=0)
    print(ready.shape)
    try:
      file_model = os.path.join(settings.BASE_DIR, 'Digit/Model/CNN_model.h5')
      # graph = ops.get_default_graph()
      graph = tf.compat.v1.get_default_graph()
      with graph.as_default():
        model = load_model(file_model)
        pred = np.argmax(model.predict(ready))
        result = str(pred)
        print("image:",image)
        print(f'Classified as {pred}')
        return result
    except:
      print('Failed to Classify')
      result = 'Er'
    return result

def home_view(request):
    return render(request, f"{app_name}/home.html")


# Create your views here.
def digit_image_view(request):
  
    if request.method == "POST":
        form = DigitForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = DigitForm()
    return render(request, f"{app_name}/digit_image_form.html", {"form" : form})
  
  
def success(request):
    return HttpResponse("successfully uploaded")
  
  
def display_digit_images(request):
  
  if request.method == "GET":

    # getting all the objects of hotel.
    digits = Digit.objects.all() 
    return render(request, f"{app_name}/display_digit_images.html", {"digit_images" : digits})


# for Django Templates
def canvas_image(request):
    if request.method=="POST":
        # print("-------",request.POST)
        if request.POST.get("captured_image"):
            captured_image = request.POST.get("captured_image")
            # imgstr = captured_image.decode("base64")
            # print("image 1: --------------------------------------", captured_image)
            # imgstr = re.search("base64,(.*)", captured_image).group(1)
            # print("image 2: --------------------------------------", imgstr)
            # imgstr = base64.b64decode(imgstr)
            # print("image 3: --------------------------------------", imgstr)
            # tempimg = io.BytesIO(imgstr)
            # im = Image.open(tempimg)
            # im.show()
            captured_image = to_internal_value(captured_image)
            img = Digit()
            img.name = aiDigit(captured_image)
            img.image = captured_image
            img.save()
            return render(request, f"{app_name}/canvas.html", {"result" : img.name})
            
    return render(request, f"{app_name}/canvas.html", {"title" : "Digit Classify"})


# for Upload Files
def upload(request):
    if request.method == "POST" and request.FILES["upload"]:
        upload = request.FILES["upload"]
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, "main/upload.html", {"file_url": file_url})
    return render(request, "main/upload.html")
