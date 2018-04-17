#!/usr/bin/env python

#=================================
# Imports           
#=================================
import sys
import os
import logging
import numpy as np
import _thread
from PIL import Image, ImageTk

# For testing
from thinice import *

if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk

#=================================
# Item representations
#=================================
EMPTY   =   np.array([0,0,0,0])
GOAL    =   np.array([1,0,0,0])
PIT     =   np.array([0,1,0,0])
WALL    =   np.array([0,0,1,0])
PLAYER  =   np.array([0,0,0,1])
WIN     =   np.array([1,0,0,1])
LOSE    =   np.array([0,1,0,1])

#=================================
# Asset location 
#=================================
ASSET_DIR   =   os.path.join(os.path.dirname(os.path.realpath(__file__)), "Assets")

class GUIApplication(tk.Frame):
    DEFAULT_WIDTH       =   800
    DEFAULT_HEIGHT      =   800
    DEFAULT_NUM_ROWS    =   4
    DEFAULT_NUM_COLS    =   4
    # In pixels
    EXPECTED_IMG_WIDTH  =   200
    EXPECTED_IMG_HEIGHT =   200
    
    logger = None

    def __init__(self, master=None, logging=True):
        tk.Frame.__init__(self, master)

        if logging:
            self.enable_logging()

        self.master.title("ThinIce")
        self.validate_defaults()
        self.grid()
        self.set_geometry()
        self.set_icon()

        # Close program with esc
        self.master.bind('<Escape>', self.close)

    def validate_defaults(self):
        # Assuming using default values, checks that they make sense
        # (width and height fit)
        assert(self.EXPECTED_IMG_WIDTH * self.DEFAULT_NUM_COLS == self.DEFAULT_WIDTH)
        assert(self.EXPECTED_IMG_HEIGHT * self.DEFAULT_NUM_ROWS == self.DEFAULT_HEIGHT)

    def set_geometry(self, width=None, height=None, resizable=False):
        if width is None:
            width = self.DEFAULT_WIDTH 
        if height is None:
            height = self.DEFAULT_HEIGHT

        # Center window in screen
        s_width = self.master.winfo_screenwidth()
        s_height = self.master.winfo_screenheight()
        x = (s_width/2) - (width/2)
        y = (s_height/2) - (height/2)
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

        if not resizable:
            self.master.resizable(width=False, height=False)

    def set_icon(self):
        icon_path = os.path.join(ASSET_DIR, "icon.ico")
        icon_img = ImageTk.PhotoImage(Image.open(icon_path))
        self.tk.call('wm', 'iconphoto', self.master._w, icon_img)

    def draw_grid(self, state):
        # Verify type and dimensions of state
        if type(state) != np.ndarray:
            err_msg = "Expected np.ndarray, instead got " + str(type(state)) 
            raise TypeError(err_msg)

        if len(state.shape) != 3:
            err_msg = "Expected 3 dimensions array, instead got " + str(len(state.shape)) + " dimensions"
            raise ValueError(err_msg)
        
        # Log state
        if self.logger is not None:
            self.logger.debug("draw_grid()\n" + 
                              "state            = \n" + str(dispGrid(state))) 
            self.logger.debug("state.shape      = " + str(state.shape))
            self.logger.debug("len(state.shape) = " + str(len(state.shape)))
            self.logger.debug("type(state)      = " + str(type(state)))

        # Draw grid
        for row in range(state.shape[0]):
            self.rowconfigure(row, minsize = self.EXPECTED_IMG_HEIGHT)
            for col in range(state.shape[1]):
                self.logger.debug("state[{}][{}] = {}".format(row,col, state[row][col]))
                self.columnconfigure(col, minsize = self.EXPECTED_IMG_WIDTH)

                # Select image for given position state
                pos_state = state[row][col]
                if np.array_equal(pos_state, EMPTY):
                    image_path = os.path.join(ASSET_DIR, "empty.jpg")
                elif np.array_equal(pos_state, GOAL):
                    image_path = os.path.join(ASSET_DIR, "goal.jpg")
                elif np.array_equal(pos_state, PIT):
                    image_path = os.path.join(ASSET_DIR, "pit.jpg")
                elif np.array_equal(pos_state, WALL):
                    image_path = os.path.join(ASSET_DIR, "wall.jpg")
                elif np.array_equal(pos_state, PLAYER):
                    image_path = os.path.join(ASSET_DIR, "player.jpg")
                elif np.array_equal(pos_state, LOSE):
                    image_path = os.path.join(ASSET_DIR, "lose.jpg")
                elif np.array_equal(pos_state, WIN):
                    image_path = os.path.join(ASSET_DIR, "win.jpg")
                else:
                    err_msg = "Unexpected position state {}, at [{}][{}]".format(pos_state, row, col)
                    raise ValueError(err_msg)
                # Validate image size
                img = Image.open(image_path)
                img_w, img_h = img.size

                assert(img_w == self.EXPECTED_IMG_WIDTH)
                assert(img_h == self.EXPECTED_IMG_HEIGHT)

                tk_image = ImageTk.PhotoImage(img)

                panel = tk.Label(self, image = tk_image)
                panel.image = tk_image
                panel.grid(column = col, row = row)
     
    def enable_logging(self):
        if self.logger is not None:
            self.logger.warning("Attempting to initialize logger when already initialized.")
            return

        # Get logger
        self.logger = logging.getLogger("ThinIceLogger")

        # Set logging file, appending old log file
        filename = os.path.join(os.getcwd(),"ThinIceGUI.log")
        fh = logging.FileHandler(filename)

        # Set format
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        fh.setFormatter(formatter)

        # Add fh to logger
        self.logger.addHandler(fh)
        self.logger.setLevel(logging.DEBUG)

        self.logger.debug("Logging enabled")

    def log_grid_info(self):
        logger_was_enabled = False if (self.logger is None) else True

        if not logger_was_enabled:
            self.enable_logging() 

        self.logger.debug("log_grid_info()\n" +
                          "grid_info        = " + str(self.grid_info()))
        

        if not logger_was_enabled:
            self.close_logger_handlers()

    def close_logger_handlers(self):
        self.logger.debug("Disabling logging")

        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def close(self, event):
        self.quit()

def update_state(app, iterations):
    for i in range(0, iterations):
        state = initGridRand()
        app.log_grid_info()
        app.draw_grid(state)


if __name__ == "__main__":
    # For testing purposes, should not be calling script directly
    app = GUIApplication()
    
    state = initGridRand()
    app.log_grid_info()
    app.draw_grid(state)

    _thread.start_new_thread(update_state, (app, 100))
    app.mainloop()
