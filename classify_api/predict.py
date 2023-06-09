import torch
from utils.helpers import *
import warnings
from PIL import Image
from torchvision import transforms
import timm
#from torchsummary import summary
from imagenet import imagenet_arr
def image_transform(imagepath):
    test_transforms = transforms.Compose([transforms.Resize((224,224)),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])
    image = Image.open(imagepath)
    imagetensor = test_transforms(image)
    return imagetensor


def predict(imagepath, verbose=False):
    if not verbose:
        warnings.filterwarnings('ignore')
    model_path = './models/catvdog.pth'
    try:
        checks_if_model_is_loaded = type(model)
    except:
        #model = load_model(model_path)
        model = timm.create_model('coatnet_1_rw_224',pretrained=True)
    model.eval()
    #summary(model, input_size=(3,244,244))
    if verbose:
        print("Model Loaded..")
    image = image_transform(imagepath)
    image1 = image[None,:,:,:]
    ps=torch.exp(model(image1))
    topconf, topclass = ps.topk(1, dim=1)
    return {'class':imagenet_arr[topclass.item()],'confidence':str(topconf.item())}


#print(predict('data/dog1.jpeg'))
#print(predict('data/cat1.jpeg'))
#print(predict('data/dog2.jpeg'))
#print(predict('data/cat2.jpeg'))
