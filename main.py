import cv2
import numpy as np

AIM_FPS = 15
AIM_WIDTH = 320
AIM_HEIGHT = 240


def video_rgb2yuv(video_path, yuv='420'):
    video = video_path
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        raise ValueError('cap is not opened !')
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps < AIM_FPS:
            raise RuntimeError('fps of video is lower than 15 !')

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print("current video is {:.0f}*{:.0f}, {:.0f} fps, frame_num = {:.0f}\n".format(width, height, fps, frame_num))

        # down sample the video to 15 fps
        sample_step = int(fps/AIM_FPS)+1
        aim_frame_num = int(frame_num * float(AIM_FPS)/fps)
        srcframe_idx = 0  # the src video frame index
        dstframe_idx = 0  # the dst (15 fps) video frame index
        buffer_bytes = np.zeros(int(AIM_WIDTH * AIM_HEIGHT * 1.5 * aim_frame_num), dtype='uint8')

        retval, frame = cap.read()
        while retval:
            if srcframe_idx % sample_step == 0:
                print('processing {}th frame'.format(dstframe_idx))
                # retval, frame = cap.read()

                # frame = np.transpose(frame, (1, 0, 2))
                resize_frame = cv2.resize(frame, (AIM_WIDTH, AIM_HEIGHT), interpolation=cv2.INTER_LINEAR)
                resize_frame = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2RGB)

                # tmp = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2YUV_IYUV)
                # cv2.namedWindow('test', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
                # cv2.imshow('test', resize_frame)
                # cv2.waitKey(0)
                buffer_bytes = pixel_rgb2yuv(resize_frame, buffer_bytes, dstframe_idx)
                srcframe_idx += 1
                dstframe_idx += 1
                retval, frame = cap.read()
            else:
                retval, frame = cap.read()
                srcframe_idx += 1

        cap.release()
        return buffer_bytes.astype(dtype='uint8').tobytes()


def pixel_rgb2yuv(frame, buffer_bytes, dstframe_idx):
    y_pos = dstframe_idx * (AIM_WIDTH * AIM_HEIGHT)
    u_pos = dstframe_idx * (AIM_WIDTH * AIM_HEIGHT) + (AIM_WIDTH * AIM_HEIGHT)
    v_pos = dstframe_idx * (AIM_WIDTH * AIM_HEIGHT) + (AIM_WIDTH * AIM_HEIGHT)*5.0/4
    v_pos = int(v_pos)

    for height in range(0, AIM_HEIGHT):
        for width in range(0, AIM_WIDTH):
            buffer_bytes[y_pos] = 0.299*frame[height, width, 0] + 0.587*frame[height, width, 1] \
                                  + 0.114*frame[height, width, 2]
            y_pos += 1
            if height % 2 == 0:
                if width % 2 == 0:
                    buffer_bytes[u_pos] = -0.169 * frame[height, width, 0] + -0.332 * \
                                          frame[height, width, 1] + 0.500 * frame[height, width, 2] + 128
                    buffer_bytes[v_pos] = 0.500 * frame[height, width, 0] + -0.419 *\
                                          frame[height, width, 1] + -0.0813 * frame[height, width, 2] + 128
                    u_pos += 1
                    v_pos += 1

    buffer_bytes = np.clip(buffer_bytes, 0, 255)
    # t = int(AIM_HEIGHT*AIM_WIDTH/4)
    # print(np.max(buffer_bytes[u_pos-t: u_pos]), np.min(buffer_bytes[u_pos-t: u_pos]))
    # cv2.imshow('y', cv2.resize(buffer_bytes[u_pos-t: u_pos].reshape(120, 160), (240,320)))
    # cv2.waitKey(0)

    return buffer_bytes


if __name__ == '__main__':
    buffer = video_rgb2yuv('./test_video.mp4')
    with open('result.yuv', 'wb') as f:
        f.write(buffer)
        f.close()
