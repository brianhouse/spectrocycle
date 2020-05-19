ffmpeg -loop 1 -i charts/1589916686.png -i 200519.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -vf scale=1080:1080 -shortest 200519.mp4
