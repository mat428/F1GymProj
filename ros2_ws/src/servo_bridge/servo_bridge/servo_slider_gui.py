import tkinter as tk

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32


class ServoSliderGUI(Node):

    def __init__(self):

        super().__init__("servo_slider_gui")

        self.publisher = self.create_publisher(
            Int32,
            "/servo_angle",
            10,
        )

        self.window = tk.Tk()
        self.window.title("Servo Controller")
        self.window.geometry("400x160")

        self.label = tk.Label(
            self.window,
            text="90°",
            font=("Arial", 18),
        )

        self.label.pack(pady=10)

        self.slider = tk.Scale(
            self.window,
            from_=0,
            to=180,
            orient=tk.HORIZONTAL,
            length=320,
            command=self.slider_changed,
        )

        self.slider.set(90)
        self.slider.pack()

    def slider_changed(self, value):

        angle = int(value)

        self.label.config(text=f"{angle}°")

        msg = Int32()
        msg.data = angle

        self.publisher.publish(msg)

    def run(self):

        while rclpy.ok():

            rclpy.spin_once(self, timeout_sec=0.01)

            self.window.update()


def main():

    rclpy.init()

    node = ServoSliderGUI()

    try:
        node.run()

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
    