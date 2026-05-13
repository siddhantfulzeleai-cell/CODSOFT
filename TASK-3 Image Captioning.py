import torch
import torch.nn as nn
import torchvision.models as models

# --- 1. TEST PRINT ---
print("--- SCRIPT IS STARTING ---")

class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(weights='DEFAULT')
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.embed = nn.Linear(resnet.fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)

    def forward(self, images):
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.bn(self.embed(features))
        return features

class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size):
        super(DecoderRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, features, captions):
        embeddings = self.embed(captions[:, :-1])
        inputs = torch.cat((features.unsqueeze(1), embeddings), dim=1)
        hiddens, _ = self.lstm(inputs)
        return self.linear(hiddens)

    def sample(self, features, max_len=20):
        sampled_ids = []
        inputs = features.unsqueeze(1)
        states = None
        for i in range(max_len):
            hiddens, states = self.lstm(inputs, states)
            outputs = self.linear(hiddens.squeeze(1))
            _ , predicted = outputs.max(1)
            sampled_ids.append(predicted.item())
            inputs = self.embed(predicted).unsqueeze(1)
        return sampled_ids

# --- 2. EXECUTION BLOCK (This runs the code) ---
if __name__ == "__main__":
    print("Initializing models...")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    encoder = EncoderCNN(256).to(device)
    decoder = DecoderRNN(256, 512, 1000).to(device)

    # --- ADD THESE TWO LINES ---
    encoder.eval()
    decoder.eval()
    # ---------------------------

    print("Processing dummy image...")
    dummy_img = torch.randn(1, 3, 224, 224).to(device)
    
    # Wrap in 'with torch.no_grad()' to save memory/speed during inference
    with torch.no_grad():
        features = encoder(dummy_img)
        caption_indices = decoder.sample(features)
    
    print("SUCCESS!")
    print(f"Generated Token IDs: {caption_indices}")