"""
Author: Héctor Sánchez
Date: 2018-02-28
Description: Base program that will remove pictures (or frames) that don't contain 
      people walking.
Folders of interest: -180228_01_0945-1100  [YYMMDD_##_hhmm-hhmm]
"""
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

if __name__=='__main__':
  """
  Remove pictures without people
  """
  pdir = '180228_01_0945-1100/100GOPRO/'
  files = os.listdir(pdir)
  files.sort()

  num_im = 200
  sims = []
  with_people = []
  alpha = 0.94 #threshold of similarity

  for i in range(num_im):
    # Loads the image
    im = cv2.imread(pdir+files[i])
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    im = cv2.resize(im,(0,0),fx=0.5,fy=0.5)
    
    if not i:
      im_prev = im
      continue

    s = ssim(im,im_prev)
    print('{0} - SSIM: {1}'.format(i,s))
    
    if s<alpha: with_people.append(files[i])

    
    sims.append(s)

    im_prev = im


  for i,fname in enumerate(with_people): print('{0} - {1}'.format(i,fname))
  
  inds = np.arange(len(sims),dtype=np.int32)
  plt.plot(inds,sims,'o-')
  #plt.xticks(inds)
  plt.show()