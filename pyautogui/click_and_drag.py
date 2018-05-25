"""
    Given to small png images, click at center of first, and drag with left
    moust button down to center of second image.
"""
import pyautogui as pyag
import sys

SCALE = 0.5  # Don't understand why, but the return from locate is off by factor of 2

def locateCenter(path_image):
    """Wrapper around pyautogui locate center, adds except catch, and info printout"""
    try:
        x, y = pyag.locateCenterOnScreen(path_image)
    except:
        print("!! Could not find image center for {}".format(path_image))
        sys.exit(1)

    x_scaled, y_scaled = x*SCALE, y*SCALE
    print("{} Found at {}, {}".format(path_image, x_scaled, y_scaled))
    return x_scaled, y_scaled


def dragAndDrop(path_image_from, path_image_to):
    """Find center of first image, left mouse click and drag to center of second iamge"""
    xf, yf = locateCenter(path_image_to)
    xi, yi = locateCenter(path_image_from)

    pyag.moveTo(xi,yi)
    pyag.dragTo(xf, yf, 2, button='left')



if __name__ == "__main__":
    print("===== ===== =====")
    print("Screen size: ", pyag.size())
    print("Cursor start: ", pyag.position())


    dragAndDrop('allstate_python_test.png', 'cloud_up_icon.png')
