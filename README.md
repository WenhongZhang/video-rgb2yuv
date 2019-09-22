# video-rgb2yuv
convert video file with RGB format to YUV(YV12) format  
  
北大深圳研究生院 数字媒体技术 作业1:  
将视频转换成YUV格式，并且检查YUV文件的正确性  
要求：分辨率320x240，色度4：2：0  
思路：使用Opencv读取Video文件，对视频进行下采样，对每一帧逐元素RGB转换为YUV，然后存储在字节流中。注意，在字节流中对于每一帧，先存储一帧的Y，再存储U，再存储V，即YV12格式。

# Requirements
opencv>=3.4

# Recommand Install Methods(for Windows10)
1.Install Anaconda3   
2.Install Opencv3 by conda  
3.Install YUView

# Comments
The yuv format is set as YV12.  
  
@2019 PKUSZ DMRD Center, Wenhong Zhang
