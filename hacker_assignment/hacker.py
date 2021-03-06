# -*- coding: utf-8 -*-
"""hacker

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E0SzfKbx96HDRStCX9s_N28OHVSsUZ1H
"""

!wget https://raw.githubusercontent.com/iamandeepsandhu/CS753/main/hacker_assignment/requirements
!pip install -r requirements
!pip install --upgrade youtube-dl
!pip install moviepy

import os
import urllib.request
import subprocess
import re
import acoustid
import chromaprint
import youtube_dl
import moviepy.editor as mp
import librosa
import matplotlib.pyplot as plt
import librosa.display
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

URLS = ['https://www.youtube.com/watch?v=-7UzQEUyrQA','https://www.youtube.com/watch?v=C-hzP3mOBGY',
        'https://www.youtube.com/watch?v=sNFjR2w_bsw','https://www.youtube.com/watch?v=hJs68D04Ypw',
        'https://www.youtube.com/watch?v=32Bxe2Nr81E','https://www.youtube.com/watch?v=2c8vTDgXULg']

# the following code was taken from 
# https://stackoverflow.com/questions/40713268/download-youtube-video-using-python-to-a-certain-directory

ydl_opts = { 'outtmpl': 'content/videos/%(title)s'+'.mp4'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)

path = "/content/content/videos/"
i=1
for filename in os.scandir(path):
    if filename.is_file():
      clip = mp.VideoFileClip(filename.path)
      print(filename.path)
      clip.audio.write_audiofile(str(i) + ".wav")
      i=i+1

"""# Helper functions for audio fingerprint comparison"""

#converting audio files into fingerprint
def fingerprint_conversion(input):
    time, raw = acoustid.fingerprint_file(input)
    fingerprint, _version = chromaprint.decode_fingerprint(raw)
    return (fingerprint, time)

#similarity index between two files
def check_audio_similarity(input1, input2):
    file1, _duration1 = fingerprint_conversion(input1)
    file2, _duration2 = fingerprint_conversion(input2)
    return correlation(file1, file2)

#correlation helper function    
def correlation(arr1, arr2):
    if len(arr1) > len(arr2):
      arr1 = arr1[:len(arr2)]
    elif len(arr1) < len(arr2):
      arr2 = arr2[:len(arr1)]
    covariance = 0
    for i in range(len(arr1)):
        covariance = covariance + 32 - bin(arr1[i] ^ arr2[i]).count("1")
    covariance = covariance / float(len(arr1))
    return covariance/32

"""# Helper function for MFCC matrix making and comparison"""

#converting audio file into mfcc matrix
def mfcc_compare(file1,file2):
  y1, s1 = librosa.load(file1) 
  y2, s2 = librosa.load(file2) 
  mfcc1 = librosa.feature.mfcc(y1,s1)
  mfcc2 = librosa.feature.mfcc(y2, s2)
  distance, path = fastdtw(mfcc1.T, mfcc2.T, dist=euclidean)
  return distance

"""# Results using audio fingerprint"""

number_of_files = len(URLS)
for i in range(1,number_of_files+1):
  base = i
  dic = dict()
  for j in range(1,number_of_files+1):
    if i!=j:
      dic[check_audio_similarity(str(base) + ".wav", str(j) + ".wav")] = j
  print("most similar to ", str(base) + ".wav :")
  for z in sorted (dic, reverse=True) :
    print (str(dic[z]) + ".wav", z)
  print("--------------------------")

"""# Results using mfcc"""

for i in range(1,number_of_files+1):
  base = i
  dic = dict()
  for j in range(1,number_of_files+1):
    if i!=j:
      dic[mfcc_compare(str(base) + ".wav", str(j) + ".wav")] = j
  print("most similar to ", str(base) + ".wav :")
  for z in sorted (dic) :
    print (str(dic[z]) + ".wav", z)
  print("--------------------------")

