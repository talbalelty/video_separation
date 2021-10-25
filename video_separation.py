{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "video_separation.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyM++iUYLPVdeixrkhtkGQ0W",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/talbalelty/Reflection-Removal/blob/main/video_separation.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "XCsb3oZhx-oT"
      },
      "source": [
        "import gc\n",
        "import cv2\n",
        "import numpy as np\n",
        "\n",
        "class Configuration:\n",
        "  def __init__(self):\n",
        "    self.window_size = 10\n",
        "    self.min_val = 2.5\n",
        "    # TAL\n",
        "    self.path_to_video = \"/content/drive/MyDrive/project images/הזזת השתקפות אצל בן.mp4\"\n",
        "    self.path_to_transmission_video = \"/content/drive/MyDrive/project images/transmission video.avi\"\n",
        "    self.path_to_reflection_video = \"/content/drive/MyDrive/project images/reflection video.avi\"\n",
        "\n",
        "def process_video_separation(video, extraction_function, path):\n",
        "  cfg = Configuration()\n",
        "  separated_video = dict()\n",
        "  window = list()\n",
        "  ret = True\n",
        "  separated_frame_index = 0\n",
        "  fps = round(video.get(cv2.CAP_PROP_FPS))\n",
        "  skip_frames = fps // cfg.window_size\n",
        "  for i in range(fps):\n",
        "    ret, frame = video.read()\n",
        "    if ret:\n",
        "      if i % skip_frames == 0:\n",
        "        window.append(frame)\n",
        "\n",
        "    else:\n",
        "      return null\n",
        "  \n",
        "  extraction_function(separated_frame_index, separated_video, window)\n",
        "  separated_frame_index += 1\n",
        "  \n",
        "  # plt.figure(figsize=(5,8))\n",
        "  # plt.imshow(np.rot90(separated_video[0], k=-1, axes=(0,1)))\n",
        "  # plt.show()\n",
        "\n",
        "  i = fps\n",
        "  while (ret):\n",
        "    ret, frame = video.read()\n",
        "    if i % skip_frames == 0:\n",
        "      window = window[1:]\n",
        "      if frame is not None:\n",
        "        window.append(frame)\n",
        "        extraction_function(separated_frame_index, separated_video, window)\n",
        "        separated_frame_index += 1\n",
        "    \n",
        "    i += 1\n",
        "\n",
        "  separated_video = list(dict(sorted(separated_video.items())).values())\n",
        "  separated_video = np.rot90(separated_video, k=-1, axes=(1,2))\n",
        "  save_video(separated_video, path)\n",
        "  return separated_video\n",
        "\n",
        "def extract_transmission_layer(frame_number, separated_video, window):\n",
        "  separated_image = np.median(window, axis=0).astype(np.uint8)\n",
        "  separated_video[frame_number] = separated_image\n",
        "\n",
        "def extract_reflection_layer(frame_number, separated_video, window):\n",
        "  cfg = Configuration()\n",
        "  grey_window = list()\n",
        "\n",
        "  for i, frame in enumerate(window):\n",
        "    grey_window.append(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))\n",
        "\n",
        "  mean = np.mean(grey_window, axis=0)\n",
        "  threshold = cfg.min_val * np.std(grey_window, axis=0)\n",
        "  mask = (grey_window[0] < mean - threshold) | (mean + threshold < grey_window[0])\n",
        "  mask = mask[:, :, np.newaxis]\n",
        "  mask = np.repeat(mask, 3, axis=2)\n",
        "  separated_video[frame_number] = np.where(mask, window[0], 0)\n",
        "\n",
        "def save_video(video, path):\n",
        "  cfg = Configuration()\n",
        "  h, w, _ = video[0].shape\n",
        "  fourcc = cv2.VideoWriter_fourcc(*'XVID')\n",
        "  out = cv2.VideoWriter(path, fourcc, cfg.window_size, (w, h))\n",
        "\n",
        "  for i in range(len(video)):\n",
        "    out.write(video[i])\n",
        "\n",
        "  out.release()\n",
        "  cv2.destroyAllWindows()\n",
        "  print(path + \"\\nVideo made successfully\")\n",
        "\n",
        "def separate_video(path_to_video):\n",
        "  # transmission\n",
        "  gc.collect()\n",
        "  cfg = Configuration()\n",
        "  video = cv2.VideoCapture(cfg.path_to_video)\n",
        "  transmission_video = process_video_separation(video, extract_transmission_layer, cfg.path_to_transmission_video)\n",
        "\n",
        "  # reflection\n",
        "  gc.collect()\n",
        "  video = cv2.VideoCapture(cfg.path_to_video)\n",
        "  reflection_video = process_video_separation(video, extract_reflection_layer, cfg.path_to_reflection_video)\n",
        "\n",
        "  return transmission_video, reflection_video"
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}