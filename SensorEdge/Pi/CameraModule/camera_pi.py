import io
import time
import picamera
from base_camera import BaseCamera

#Base Generator Idea found from Guide: https://blog.miguelgrinberg.com/post/video-streaming-with-flask. Modified for use with SHS

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            camera.rotation = 180
            camera.resolution = (640,480)
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()