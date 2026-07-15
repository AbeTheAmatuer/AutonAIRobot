from ultralytics import YOLO

model = YOLO("yolo26n-seg.pt")

results = model.track(source="https://www.youtube.com/watch?v=vqqt5p0q-eU", show=True, tracker="bytetrack.yaml")
