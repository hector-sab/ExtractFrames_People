"""
Author: Héctor Sánchez
Date: 2018-02-28
Description: The program will remove pictures that don't contain people walking.
Folders of interest: -180228_01_0945-1100  [YYMMDD_##_hhmm-hhmm]
"""
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
from shutil import copy2
import numpy as np
import cv2
import os

def efold(edir):
  """
  Checks the end of the directory
  """
  if edir[-1]!='/':
    edir += '/'
  return(edir)


class FindPeopleIms:
  def __init__(self,mdir,folder):
    """
    mdir: main directory where the folder with images is
    folder: folder containing the images to be analyzed
    """
    self.dir = mdir
    self.folder = folder
    self.pdir = self.dir + self.folder
    self.pdir = efold(self.pdir)
    self.out_dir = self.dir + self.folder + '_PPL/'
    self.sims = [] # Similarities
    self.wppl = [] # With people

  def runme(self,alpha=0.94):
    """
    Main program. Find all the images with people
    """
    if not os.path.exists(self.out_dir):
      os.mkdir(self.out_dir)

    self.files = os.listdir(self.pdir)
    self.files.sort()

    self.alpha = alpha # Similarity threshold

    for i in range(len(self.files)):
      im = cv2.imread(self.pdir+self.files[i])
      im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
      im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)

      if not i:
        im_p = im
        continue

      s = ssim(im,im_p)
      print('{0}/{1} - {2} SSIM: {3}'.format(i,len(self.files),self.files[i],s))

      # In case the SSIM indicates that two pictures are very different...
      # Saves in a list and copies all photos with people to a new folder    
      if s<self.alpha: 
        self.wppl.append(self.files[i])
        copy2(self.pdir+self.files[i],self.out_dir)

      self.sims.append(s)

      im_p = im

  def runme2(self,it=100,alpha=0.94):
    """
    Run an specific number of iterations
    """
    self.files = os.listdir(self.pdir)
    self.files.sort()

    self.alpha = alpha # Similarity threshold

    for i in range(it):
      im = cv2.imread(self.pdir+self.files[i])
      im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
      im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)

      if not i:
        im_p = im
        continue

      s = ssim(im,im_p)
      print('{0}/{1} - {2} SSIM: {3}'.format(i,it,self.files[i],s))

      # In case the SSIM indicates that two pictures are very different...
      # Saves in a list and copies all photos with people to a new folder    
      if s<self.alpha: 
        self.wppl.append(self.files[i])

      self.sims.append(s)

      im_p = im

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
  record = '180228_02_1300-1500/People/'
  folder = '116GOPRO_PPL'

  fppl = FindPeopleIms(mdir=record,folder=folder)
  fppl.runme2(alpha=0.905)
  fppl.im_names()
  fppl.graph()

  """
  folders = os.listdir(record)
  folders.sort()
  #t = 6 # 0,2,4,6,8
  #t1 = 0 + t
  #t2 = 2 + t
  #folders = folders[t1:]

  for i in range(len(folders)):
    #if i>0: break
    print('Running on {0} {1}'.format(record,folders[i]))
    fppl = FindPeopleIms(mdir=record,folder=folders[i])

    fppl.runme(alpha=0.925)
    fppl.im_names()
    #fppl.graph()
  """