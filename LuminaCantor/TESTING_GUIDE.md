# Alchemical Cantor - Testing Guide

## Quick Start (Command Line)

### 1. Test the Core Pipeline
```bash
cd "c:\LUMINA RED PILL"
python -m LuminaCantor.main
```

This will:
- Load Shakespeare's Sonnet 18 from `LuminaCantor/input_texts/sonnet_18.txt`
- Parse the text into an emotional vector
- Generate a MIDI file: `LuminaCantor/input_texts/transmutation.mid`

### 2. Listen to the Generated Music
- Open `LuminaCantor/input_texts/transmutation.mid` in any MIDI player
- Windows Media Player, VLC, or online MIDI players work

## Test with Your Own Text

### 1. Add Your Text File
Place your `.txt` file in: `LuminaCantor/input_texts/your_file.txt`

### 2. Run with Custom Text
```bash
cd "c:\LUMINA RED PILL"
python -c "from LuminaCantor import main; main.transmute_text_to_music('LuminaCantor/input_texts/your_file.txt')"
```

## GUI Testing (Current - Basic)

### 1. Launch the GUI
```bash
cd "c:\LUMINA RED PILL"
python Lumina/gui.py
```

### 2. Use the Alchemical Cantor Mode
- Select "ALCHEMICAL CANTOR" from the dropdown
- Click "SELECT TEXT FILE" and choose your text file
- Click "EXECUTE MISSION"
- Check the terminal output for progress
- Find the generated MIDI file in the same folder as your input text

## What to Expect

- **Input**: Any text file (.txt)
- **Output**: A MIDI file (.mid) in the same directory as input
- **Processing Time**: 1-2 seconds for typical texts
- **Musical Style**: Melodic line based on word patterns, rhythm, and emotional weight

## Troubleshooting

### "No module named 'titan_forge'"
- This is expected - the Rust backend is optional for basic functionality
- The system works without it using direct emotional mapping

### MIDI file won't play
- Ensure you have a MIDI player installed
- Try online MIDI players if local players don't work

### GUI looks outdated
- A modern web interface is being developed
- Current GUI is functional but uses basic tkinter styling
