## Pyautogui Drag And Drop

Basic setup for drag and drop with left mouse button hold.

Install with
```
pip install -r requirements.txt
```

### Notes
1.  Two images were taken, one of a closeup of a file in finder, and the other the target cloud icon.
2.  Seems to have a hard time every once in a while with cloud icon, I had to retake the png to get it working again.
3.  For some reason, the scale is off, the mouse coordinates are returned correctly.  My screen is 1920x1080, and the moveto and so forth match.  But when I ask for the center location of an image, I get double the coordinate, thus the SCALE variable in the script to correct for that.


