# sketch

Sketch started from a very bad webcam that I use to record musical ideas (sound pops and high pitch noise).
It takes the raw files from my webcam folder, encodes them into .mp4 format, applies audio fades and applies
sound filtering (filters out the very low rumbling frequencies and the super annoying high noise frequencies).

After it's done with the video/audio processing, it starts extracting the pitch for each musical sketch using a pre-trained
neural network (it basically takes a sample every 10 milliseconds and estimates the frequency for that segment).

The main goal of this tool is to fix very specific video and audio problems, inform me on the pitch of the musical idea and to
give me a logical management system of these ideas, thus hoping to increase productivity.


General dependencies:
- mysql-server
- redis-server
- ffmpeg
- ffmpeg-normalize
- tensorflow
- crepe

VIDEO FOCUS: for each sketch, we get the main five musical notes and a management system that makes it so much easier to organise them.

![](https://github.com/plantroots/sketch/blob/master/docs/images/1.png)

ALBUM FOCUS: for each song, we get the estimated tempo, the duration and the estimated fundamental frequency (computed into musical notation).

![](https://github.com/plantroots/sketch/blob/master/docs/images/2.png)
