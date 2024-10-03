from ultralytics import YOLO

model = YOLO("yolov8m.pt")

model.train(data="C:\VSCODE\EOL_LINE\Errort\custom1.yaml", epochs=5)