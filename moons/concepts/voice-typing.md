# Voice Typing and Transcription

AI consumption pattern where two models collaborate in a pipeline. Illustrates fragmented configuration.

## How it works
- On-device speech model (usually Whisper variant) transcribes audio locally
- Language model cleans transcript: grammar, filler words, formatting
- Two-stage pipeline: speech-to-text → text cleanup

## Products
- **SuperWhisper**: fully on-device Whisper, no cloud, one-time purchase — privacy but limited quality
- **Wispr Flow**: on-device Whisper + cloud LLM cleanup, monthly subscription — polished output
- **MacWhisper**: local Whisper, one-time purchase, optional advanced features — no recurring cost

## Cost models
- Subscription (Wispr Flow): recurring monthly for cloud LLM access
- One-time purchase (SuperWhisper, MacWhisper): fixed capabilities, no ongoing cost
- DIY: manually configure local Whisper + separate LLM endpoint

## Relevance to Saturn
- Demonstrates AI consumption fragmentation: each tool handles its own model configuration
- The DIY path requires configuring two separate AI services manually
- Saturn could provide both transcription and LLM cleanup endpoints via network discovery
- Example of how per-user configuration burden multiplies across AI use cases

## Chapters
- Ch 2.3: AI service landscape example
