ffmpeg -loop 1 -i charts/1589344730.png -i 200502.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -vf scale=1080:1080 -shortest 200502.mp4
