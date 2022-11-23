from django.db import models
from django.conf import settings

from GraphQL.models import BaseModel, BaseModelImage
# import tensorflow as tf
# from PIL import Image
#from keras.preprocessing.image import img_to_array
# from tensorflow.keras.utils import img_to_array
# from keras.preprocessing import image
# from tensorflow.keras.models import load_model
# from tensorflow.python import ops
# import cv2, os
# import numpy as np


# Create your models here.


class Digit(BaseModelImage, BaseModel):
  
  def __str__(self) -> str:
    return str(self.id)
  
  # def save(self, *arg, **kwargs):
  #   print(self.image)
  #   img = Image.open(self.image)
  #   img_array = img_to_array(img)
  #   # img_array = tf.keras.preprocessing.image.array_to_img(img)
  #   print(img_array)
  #   print(img_array.shape)
  #   new_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
  #   dim = (28, 28)
  #   resized = cv2.resize(new_img, dim, interpolation= cv2.INTER_AREA)
  #   print(resized.shape)
  #   ready = np.expand_dims(resized, axis=2)
  #   ready = np.expand_dims(ready, axis=0)
  #   print(ready.shape)
  #   try:
  #     file_model = os.path.join(settings.BASE_DIR, 'Model/CNN_model.h5')
  #     # graph = ops.get_default_graph()
  #     graph = tf.compat.v1.get_default_graph()
  #     with graph.as_default():
  #       model = load_model(file_model)
  #       pred = np.argmax(model.predict(ready))
  #       self.result = str(pred)
  #       print("image:",self.image)
  #       print(f'Classified as {pred}')
  #       # return self.result
  #   except:
  #     print('Failed to Classify')
  #     self.result = 'Failed Classify'
  #   return super(Digit, self).save(*arg, **kwargs)