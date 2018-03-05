"""
Author: Héctor Sánchez
Date: 2018-02-28
Description: The program will remove frames that don't contain people walking.
Folders of interest: -180228_01_0945-1100  [YYMMDD_##_hhmm-hhmm]
"""
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
from shutil import copy2
import numpy as np
import cv2
import sys
import os

def efold(edir):
  """
  Checks the end of the directory
  """
  if edir[-1]!='/':
    edir += '/'
  return(edir)

def fname(i,lzeros=5):
  """
  Returns the name of a frame to be saved
  """

  it = str(i)

  zeros = lzeros-len(it)

  name = 'Frame_'
  for j in range(zeros):
    name += '0'
  name += it+'.JPG'
  return(name)



class FindPeopleVid:
  def __init__(self,mdir,folder,video):
    """
    mdir: main directory where the folder with images is
    folder: folder containing the images to be analyzed
    """
    self.dir = mdir
    self.folder = folder
    self.video = video
    self.pdir = self.dir + self.folder
    self.pdir = efold(self.pdir)
    self.out_dir = self.dir + self.folder + video[:-4] + '_PPL/'
    self.sims = [] # Similarities
    self.wppl = [] # With people

  def runme(self,alpha=0.94):
    """
    Main program. Find all the images with people
    """
    if not os.path.isfile(self.pdir+self.video):
      print('File not found: {}'.format(self.pdir+self.video))
      sys.exit()
    else:
      print(self.pdir+self.video)

    if not os.path.exists(self.out_dir):
      os.mkdir(self.out_dir)

    vid = cv2.VideoCapture(self.pdir+self.video)
    nframes = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    self.alpha = alpha # Similarity threshold

    i = 0
    count = 0
    while(vid.isOpened()):
      ret,im = vid.read()
      
      if not ret:
        count += 1
        if count>1000:
          print('Frames not detected. Ending Search.')
          break
        continue
      
      count = 0
      
      # To Speed up the process, skip some frames
      skips = 2
      for _ in range(skips):
        _ = vid.read()
      #####

      im_rgb = im
      im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
      im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)

      if not i:
        im_p = im
        i += 1
        continue

      s = ssim(im,im_p)
      pflag = ''
      # In case the SSIM indicates that two pictures are very different...
      # Saves in a list and copies all photos with people to a new folder    
      if s<self.alpha:
        pflag = '***'
        name = fname(i)
        self.wppl.append(name)
        cv2.imwrite(self.out_dir+name,im_rgb)

      print('{0}/{1} - {2} SSIM: {3} {4}'.format(i,int(nframes/(skips+1)),self.video,s,pflag))

      self.sims.append(s)

      im_p = im

      i += 1

  def runme2(self,it=800*3,alpha=0.98):
    """
    Run an specific number of iterations
    """
    if not os.path.isfile(self.pdir+self.video):
      print('File not found')
      sys.exit()
    else:
      print(self.pdir+self.video)
    
    
    vid = cv2.VideoCapture(self.pdir+self.video)
    nframes = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    self.alpha = alpha # Similarity threshold

    i = 0
    while(vid.isOpened()):
      if i>it:
        break
      ret,im = vid.read()

      if not ret:
        continue
      im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
      im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)

      if not i:
        im_p = im
        i += 1
        continue
      
      s = ssim(im,im_p)
      save_fold = 'tmp2/'
      print('{0}/{1} [{2}] - {3} SSIM: {4}'.format(i,it,nframes,self.video,s))
      if not os.path.exists(self.pdir+save_fold):
        os.mkdir(self.pdir+save_fold)

      # In case the SSIM indicates that two pictures are very different...
      # Saves in a list and copies all photos with people to a new folder    
      if s<self.alpha:
        name = fname(i)
        self.wppl.append(name)
        cv2.imwrite(self.pdir+save_fold+str(i)+'.jpg',im)

      self.sims.append(s)

      im_p = im

      i += 1

  def im_names(self):
    """
    Print the names of all files qith images
    """
    for i,fname in enumerate(self.wppl): 
      print('{0} - {1}'.format(i,fname))

  def graph(self):
    """
    Print Structural Similarities Index Graph
    """
    inds = np.arange(len(self.sims),dtype=np.int32)
    plt.plot(inds,self.sims,'o-')
    #plt.xticks(inds)
    plt.show()


if __name__=='__main__':
  """
  Remove pictures without people
  """
  record = '/media/hector-cic/DATA/MTA/Research_Project/Database/CICATA18_People_Walking/180305_01/'
  folder = '100GOPRO/'
  videos = ['GOPR7868.MP4','GP017868.MP4','GP027868.MP4','GP037868.MP4',
            'GP047868.MP4','GP057868.MP4','GP067868.MP4','GP077868.MP4']

  for video in videos:
    fppl = FindPeopleVid(mdir=record,folder=folder,video=video)
    fppl.runme(alpha=0.97)
    #fppl.im_names()
    #fppl.graph()