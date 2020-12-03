# Standard modules
import json

# Open source modules
import librosa
import numpy as np
import torch
import torch.optim as optim

# Project modules
import model_utils

with open('species.json') as json_file: 
    species_data = json.load(json_file) 

# Preprocess audio 
def preprocess(file):
    y, sr = librosa.load(file)
    period = 30
    effective_length = sr * period
    list_y = []
    for i in range(1):
        if len(y) < effective_length:
            new_y = np.zeros(effective_length, dtype=y.dtype)
            start = np.random.randint(effective_length - len(y))
            new_y[start:start + len(y)] = y
            y_snippet = new_y.astype(np.float32)
        elif len(y) > effective_length:
            start = np.random.randint(len(y) - effective_length)
            y_snippet = y[start:start + effective_length].astype(np.float32)
        else:
            y_snippet = y.astype(np.float32) 
        list_y.append(y_snippet)
    x = torch.FloatTensor(list_y).cpu()
    return x

# Load model from checkpoint file
def load_ckp(checkpoint_fpath, model, optimizer):
    checkpoint = torch.load(checkpoint_fpath)
    model.load_state_dict(checkpoint['state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    return model, optimizer, checkpoint['epoch'] 

# Load model
def load_model(path_model):
    model_loaded = model_utils.PANNsDense121Att(sample_rate=32000, window_size=1024, hop_size=320,
                 mel_bins=64, fmin=50, fmax=14000, classes_num=264, apply_aug=True, top_db=None)
    optimizer_loaded = optim.AdamW(model_loaded.parameters(), lr = 0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay = 0.01, amsgrad=True)
    model_loaded, optimizer_loaded, start_epoch = load_ckp(path_model, model_loaded, optimizer_loaded)
    return model_loaded

# Identify bird specie
def predict(file):
    model_loaded = load_model('checkpoint.pt')
    model_loaded.eval()
    x = preprocess(file)
    x = x.expand((1, x.shape[0], x.shape[1]))
    pred = model_loaded(x)["clipwise_output"]
    pred = np.array(pred.permute(1, 0, 2).max(2)[1])[0][0]
    specie = species_data[str(pred)]
    image =  str(pred) + '.jpg'
    return specie, image