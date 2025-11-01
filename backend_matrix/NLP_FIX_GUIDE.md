# NLP Endpoint Fix - Complete Setup Guide

## Issue Fixed
The NLP endpoint was failing due to incompatible versions of `transformers` and `huggingface_hub`.

### Error Message
```
cannot import name 'split_torch_state_dict_into_shards' from 'huggingface_hub'
```

## Solution Applied

### 1. Upgraded Dependencies
Updated the following packages to compatible versions:
- `torch`: 2.1.1 → 2.9.0
- `transformers`: 4.35.2 → 4.57.1
- `huggingface_hub`: 0.19.4 → 0.36.0
- `tokenizers`: 0.15.2 → 0.22.1
- `torchvision`: 0.16.1 → 0.24.0
- `torchaudio`: 2.5.1 → 2.9.0

### 2. Installed Missing Dependencies
- `typer-slim`: Required by newer huggingface_hub
- `hf-xet`: Required by newer huggingface_hub

### 3. Install spaCy Model (Required)
The NLP endpoint also requires the spaCy English model.

## Complete Setup Instructions

### Step 1: Upgrade Dependencies (Already Done)
The dependencies have been upgraded. If you need to do this again:

```powershell
pip install --upgrade torch torchvision torchaudio
pip install --upgrade huggingface_hub transformers
pip install typer-slim hf-xet
```

### Step 2: Install spaCy Model (REQUIRED)
```powershell
python -m spacy download en_core_web_sm
```

Or use the automated script:
```powershell
python install_nlp_models.py
```

Or use the PowerShell script:
```powershell
.\install_spacy_model.ps1
```

### Step 3: Restart the Backend Server
After upgrading packages, restart your backend:

```powershell
# Stop the current server (CTRL+C)
# Then restart it
.\start.ps1
```

Or:
```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Testing the Fix

### Quick Test
```powershell
python test_nlp.py
```

### Manual Test via API
```powershell
# Test health
curl http://127.0.0.1:8000/nlp/health

# Test analysis
curl -X POST http://127.0.0.1:8000/nlp/analyze -H "Content-Type: application/json" -d "{\"text\":\"Test news\"}"
```

## What Should Happen Now

1. ✅ The transformers library will load without import errors
2. ✅ The NLP models will initialize properly
3. ✅ The `/nlp/analyze` endpoint will work correctly
4. ✅ First request may take longer as models load into memory
5. ✅ Subsequent requests will be faster

## Important Notes

### First Request Timing
- **First request**: 10-30 seconds (loading models into memory)
- **Subsequent requests**: 2-5 seconds

### Model Loading
Models are loaded lazily (on first request) to improve startup time. This is normal behavior.

### Memory Usage
The NLP endpoint loads several large models:
- DeBERTa tokenizer and model (~500MB)
- spaCy model (~12MB)
- Knowledge graph

Make sure you have sufficient RAM (recommend at least 4GB free).

## Troubleshooting

### Issue: "spaCy model not found"
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: "Model checkpoint not found"
**Solution**: Ensure the `nlp_model/checkpoint-753` directory exists with model files

### Issue: Still getting import errors
**Solution**: 
1. Check installed versions: `pip show transformers huggingface_hub`
2. Should be: transformers >= 4.57.0, huggingface_hub >= 0.36.0
3. Reinstall if needed: `pip install --upgrade --force-reinstall transformers huggingface_hub`

### Issue: Out of memory
**Solution**: 
- Close other applications
- The models are loaded once and reused
- Consider increasing system memory if persistent

## Updated Requirements

The `requirements.txt` has been updated with correct versions:
- `torch>=2.9.0`
- `transformers>=4.57.0`
- `huggingface_hub>=0.36.0`

For fresh installations, run:
```powershell
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Success Indicators

When everything is working:
1. Server starts without errors
2. `/nlp/health` returns status with `spacy_model_available: true`
3. `/nlp/analyze` processes text and returns predictions
4. No import errors in logs

## Next Steps

1. ✅ Restart the backend server
2. ✅ Run `python test_nlp.py` to verify
3. ✅ Test from frontend
4. ✅ Monitor first request (may be slow)
5. ✅ Verify subsequent requests are faster
