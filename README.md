A utilization of the rpi-rgb-led-matrix and tbapy libraries for python. 

With this repo, a 64x32 rgb led matrix can display data pulled from The Blue Alliance! Simply run the command
```
sudo python3 main.py frc[teamNum] [comp]
```

Example:
```
sudo python3 main.py frc7211 2024miwmi
```

It's as easy as that! This should work with most competitions and possibly even currently running ones! 

Note: This is still just me messing around with the libraries, support for displays is hard coded in the main.py file, you'd have to change that if you have a different display and there is ZERO garuntee that this will work on any displays larger/smaller than 64x32 (actually it is NOT supported on smaller displays, I can hardly show data)


If you have any issues, please file an issue. The code isn't great as it's my first time messing with Python, but I hope it works well enough!


Made by Noah/PGtheVRguy (who's on FRC 7211 >:3)



This was NOT made on behalf/affiliated of/with First Robotics or The Blue Alliance, all trademarks belong to them and other legal stuff similar to that. I just wanna have a cool way to view matches :3
