ffmpeg -loop 1 -i /Users/house/Studio/spectrometer/charts/1592597262.png -i /Users/house/Studio/firefly/micros/200619.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -vf scale=1080:1080 -shortest /Users/house/Studio/firefly/micros/200619.mp4
