# sizer_image.py code resizes the image is as per user input and and organizes them in separate folders. Features include: 
# Developed by Beautifulbird, March 2017.

from PIL import Image
import glob
import os,sys,time
import shutil
codepath = os.path.dirname(os.path.realpath(__file__)) + "/"

class initial_config():
    # initial configuration
    def __init__(self):
        self.sdir = "images/"
        self.extensions = [".png",".jpg"]
        self.cdir = {   "images1x/" : 72    ,
                        "images2x/" : 144   ,
                        "images3x/" : 288   , 
                        "images4x/" : 576   
                    }
        return

def main():
    g1 = initial_config()
    datafolder = codepath + g1.sdir
    for dirs in sorted(g1.cdir):
        # scan through each category folder
        print("==================")
        create_directory(codepath + dirs)
        # prompt for width
        try:
            print("Specify desired width for {} folder".format(dirs))
            bwidth = int(input("(0 is default to maintian original width): "))
        except ValueError:
            bwidth = 0

        for root, subdirs, files in sorted(os.walk(datafolder)):
            # scan through nested folders within the images folder and get path for eac of image file
            rootrelative = os.path.relpath(root, codepath) + "/"
            if os.listdir(root) != []: 
                os.chdir(root)
                for exts in g1.extensions:
                    # scan through extensions
                    for filename in glob.glob("*"+exts):
                        tmpfile = "tmptmp"+exts
                        delete_file(tmpfile)

                        # get image details. populate the class
                        im1 = image_data(filename)

                        print("------------------")
                        print("""Image name: "{}"  """.format(im1.filename))
                        print("""Image location: "{}"  """.format(rootrelative))
                        print("Orig Dims: W x H = {} x {} = {}".format(im1.width,im1.height,im1.numpix))
                        prefix = "@"+dirs[-3:-1]
                        # clean uo the file name
                        fname = clean_filename(im1.filename,prefix)

                        # rescale the file as per the user specified width and dpi and save as temp file
                        save_image(im1.filename,dpi=g1.cdir[dirs],basewidth=bwidth,outfile=tmpfile)

                        # copy the file to corresponding category folder 
                        copy_file(tmpfile,dirs,fname)

                        delete_file(tmpfile)

    os.chdir(codepath)
    print("Done")
    print("==================")
    return
    
class image_data:
    # get image details. populate the class
    def __init__(self, filename):
        with Image.open(filename) as im:
            self.width,self.height = im.size
            self.numpix = self.width*self.height
            self.filename = filename

def create_directory(dname):
    if not os.path.exists(dname):
        os.makedirs(dname)
    return

def delete_file(tmpfile):
    if os.path.isfile(tmpfile):
        os.remove(tmpfile)
    return

def svg_to_png(fname):
    return

def save_image(infile,dpi=72,basewidth=0,outfile = "tmptmp"):
    # rescale the file as per the user specified width and dpi and save as temp file
    with Image.open(infile) as im:
        # assign cutom dpi to image as attribute
        im.info["dpi"] = dpi
        basewidth = int(basewidth)
        if basewidth != 0:
            # preserve aspect ratio, calculate new dimensions
            orig_width  = im.size[0]
            orig_height = im.size[1]
            aspect_ratio = float(orig_height)/float(orig_width)
            new_width = basewidth
            new_height = int( float(basewidth)*aspect_ratio )
            im.thumbnail((new_width,new_height), Image.ANTIALIAS)
            print("New  Dims: W x H = {} x {} = {}".format(im.size[0],im.size[1],im.size[0]*im.size[1]))
        im.save(outfile,dpi=(dpi,dpi))
    return

def copy_file(srcfile,folder,desfile):
    # copy the file to corresponding category folder 
    shutil.copy2(srcfile,codepath+folder+desfile)
    print("""Saved --> {}{} """.format(folder,desfile))
    
def clean_filename(fname,prefix):
    # clean uo the file name
    # remove extra white spaces and other characters
    fname = "-".join(fname.split())
    fname = fname.lower()
    parts = fname.split(".")
    fname = "".join(parts[:-1])+ prefix + '.' + parts[-1]
    return fname

if __name__ == '__main__':
    main()
