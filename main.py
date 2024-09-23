import argparse
import math
import subprocess
import yaml
import av
import numpy as np
from PIL import Image

scene_config = {
  "task": "shading",
  "antialias": "SSAA",
  "samples": 16,
  "resolution": {
    "width": 800,
    "height": 800
  },
  "obj": "obj/monkeys",
  "output": "output",
  "camera": {
    "pos": [0.0, 0.0, 5.0],
    "lookAt": [0.0, 0.0, 0.0],
    "up": [0.0, 1.0, 0.0],
    "width": 0.2,
    "height": 0.2,
    "nearClip": 0.1,
    "farClip": 100.0
  },
  "transforms": [
    {
      "translation": [2.0, 0.0, 0.0],
    },
    {
      "translation": [-2.0, 0.0, 0.0],
    }
  ],
  "exponent": 4.0,
  "ambient": [31, 31, 31],
  "lights": [
    {
      "intensity": 50.0,
      "color": [0, 255, 255]
    },
    {
      "intensity": 100.0,
      "color": [255, 0, 0]
    }
  ]
}
width=800
height=800
def main():
  parser = argparse.ArgumentParser(description="Generate video with optional time and fps arguments.")
  parser.add_argument('-t', '--time', type=int, default=5, help="Duration of the video in seconds (default: 5)")
  parser.add_argument('-f', '--fps', type=int, default=30, help="Frames per second (default: 30)")
  args = parser.parse_args()
  
  genVideo(args.time, args.fps)
  

def genVideo(time: float, fps: float):
  container = av.open("output.mp4", mode="w")
  stream = container.add_stream("libx264", rate=fps)
  stream.width = width
  stream.height = height
  stream.pix_fmt = "yuv420p"

  frames = int(time*fps)
  for i in range(frames):
    print(f"Frame {i+1}/{frames}")
    update_config(i/frames)
    subprocess.run(["../rasterizer/rasterizer", "config.yaml"], check=True, stdout=subprocess.DEVNULL)
    frame = Image.open("output.png")
    frame = frame.convert("RGB")
    frame_data = np.asarray(frame)
    av_frame = av.VideoFrame.from_ndarray(frame_data, format='rgb24')
    for packet in stream.encode(av_frame):
      container.mux(packet)
  for packet in stream.encode():
    container.mux(packet)
  container.close()

def update_config(t: float):
  angle=2*math.pi*t
  scene_config["transforms"][0]["rotation"]=[math.cos(angle), math.sin(angle), 0.0, 0.0]
  scene_config["transforms"][1]["rotation"]=[math.cos(-angle), math.sin(-angle), 0.0, 0.0]
  scene_config["transforms"][0]["scale"]=[1.0-abs(t-.5), 1.0-abs(t-.5), 1.0-abs(t-.5)]
  scene_config["transforms"][1]["scale"]=[.5+abs(t-.5), .5+abs(t-.5), .5+abs(t-.5)]
  scene_config["camera"]["pos"]=[5.0*math.sin(-angle), 0.0, 5.0*math.cos(-angle)]
  scene_config["lights"][0]["pos"]=[8.0*math.sin(angle), 0.0, 8.0*math.cos(angle)]
  scene_config["lights"][1]["pos"]=[0.0, 10.0*math.sin(2*angle), 10.0*math.cos(2*angle)]
  with open("config.yaml", 'w') as yamlFile:
    yaml.dump(scene_config, yamlFile, indent=0, default_flow_style=True)

if __name__=="__main__":
    main()