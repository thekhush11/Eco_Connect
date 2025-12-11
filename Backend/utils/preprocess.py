# backend/utils/preprocess.py
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as kimage
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np

def load_and_preprocess(path, target=(224,224)):
    img = kimage.load_img(path, target_size=target)
    x = kimage.img_to_array(img)
    x = np.expand_dims(x, 0)
    x = preprocess_input(x)
    return x

def preprocess_image_for_model(image_path, target_size=(224,224)):
    """
    Loads image_path, resizes to target_size, converts to normalized float32 numpy array,
    returns a batch tensor shaped (1, H, W, 3) with values in range [0,1].
    """
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size, Image.BILINEAR)
    arr = np.asarray(img).astype('float32') / 255.0
  
    if arr.ndim == 2:
        arr = np.stack([arr]*3, axis=-1)
    batch = np.expand_dims(arr, axis=0)
    return batch
