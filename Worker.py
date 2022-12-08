import torch
from torchvision import transforms
import cv2


class Worker:

    def __init__(self):
        self.preprocessor = transforms.Compose([
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)
        self.model.eval()
        with open("imagenet_classes.txt", "r") as f:
            self.categories = [s.strip() for s in f.readlines()]

    def recognize(self, image) -> str:
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = torch.from_numpy(image)
        image = image.to(torch.float)
        image = image.permute(2, 0, 1)
        image = image / 256
        input_tensor = self.preprocessor(image)
        input_batch = input_tensor.unsqueeze(0)
        with torch.no_grad():
            output = self.model(input_batch)
        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 1)
        for i in range(top5_prob.size(0)):
            print(self.categories[top5_catid[i]], top5_prob[i].item())
        return self.categories[top5_catid[0]]
