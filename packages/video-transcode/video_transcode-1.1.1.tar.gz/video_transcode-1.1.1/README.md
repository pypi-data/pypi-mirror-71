# video-transcode
=======
Simplified commercial cutting and transcoding for Plex DVR.
 
# Installation
1. Install ffmpeg
2. Install redis 
3. Install comcut
4. Install comskip
3. Clone video-transcode
4. make
5. start service
6. Add video-transcode script path to Plex post processing.

# To Do
- Configurable UID/GID
- Pass additional ffmpeg options
- Port comcut to Python

### For NVENC endocding
1. Install (nvidia-container-toolkit)[https://github.com/NVIDIA/nvidia-docker]
2. 