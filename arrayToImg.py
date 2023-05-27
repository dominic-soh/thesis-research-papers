from PIL import Image
import dill

def me(flt_im):
    # Make numpy array into image without allocating any more memory
    p = Image.fromarray(flt_im, mode='L')

    # Create a palette with 256 colours - first 50 are your blueish colour, rest are white
    palette = 5*[100,150,200] + 5*[100,200,150] + 40*[100,200,150] +  206*[255,255,255]

    # Put palette into image and save
    p.putpalette(palette)
    p.save('result.png')

big_boi20131 = dill.load(open("big_boi20131.pickle", "rb"))
me(big_boi20131)