import glfw

class Controller:
    def __init__(self):
        self.rotate = [0.0, 0.0]     # yaw, pitch
        self.zoom = 3.0              # distance from camera target
        self.last_mouse = None
        self.should_exit = False

    def install_callbacks(self, window):
        glfw.set_key_callback(window, self.on_key)
        glfw.set_cursor_pos_callback(window, self.on_mouse_move)
        glfw.set_scroll_callback(window, self.on_scroll)

    def on_key(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.should_exit = True

    def on_mouse_move(self, window, xpos, ypos):
        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) != glfw.PRESS:
            self.last_mouse = None
            return

        if self.last_mouse is None:
            self.last_mouse = (xpos, ypos)
            return

        dx = self.last_mouse[0] - xpos
        dy = self.last_mouse[1] - ypos
        self.rotate[0] += dx * 0.005
        self.rotate[1] -= dy * 0.005
        self.last_mouse = (xpos, ypos)

    def on_scroll(self, window, xoffset, yoffset):
        self.zoom *= 0.9 if yoffset > 0 else 1.1
        self.zoom = max(0.1, min(self.zoom, 20.0))

