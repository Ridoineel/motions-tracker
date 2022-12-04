# MotionsTracker

> MotionsTracker is a module that allows you to
> Track the movements of webcam images and save them as images or as a single video


## How do i install MotionsTracker ?

```bash
pip install motionstracker
```

## How do i use it ?

```bash
python -m motionstracker
```

#### Arguments

- Output Directory: --output-dir or -o
		path to an directory

- Motion accuracy: --accuracy or -ac
		value between 0 and 1

- Duration: --duration or -d
		duration format: 1m, 1s, 1h, 10:21 or 11:21:12

- Output format: --format or -f
		value images or video

	**video** is recommanded if the _duration_ is too long

## Example

Track the motions with **accuracy=0.8** during **1 minute** <br>
and save the images as **video** in the **directory output**

```bash
mkdir output
python -m motionstracker -d output -ac 0.8 -d 1m -f video
```
