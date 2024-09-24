# CG HW1 Test - Video Generation Test Case for EECS 598 Rasterizer

This repository provides a video generation test case for the EECS 598 rasterizer project.

## Setup Instructions

1. **Navigate to your project directory:**

   ```bash
   cd hw1
   ```

2. **Clone the test repository:**

   ```bash
   git clone https://github.com/border-umich/cg-hw1-test.git
   ```

3. **Change into the test directory:**

   ```bash
   cd cg-hw1-test
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the generator:**

   ```bash
   python main.py -t {time} -f {framerate}
   ```

## Convert Output to WebP (Optional)

If you'd like to share your output on Piazza or similar platforms, you can convert your MP4 video to a WebP animation.

1. **Convert using `ffmpeg`:**

   ```bash
   ffmpeg -i output.mp4 -loop 0 loop.webp
   ```

   The `-loop 0` option makes the animation loop indefinitely.
