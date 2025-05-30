import openai
from pathlib import Path
import os

def audio_transcribe(input_path, resp_format="text", lang="en"):
    with open(input_path, "rb") as f:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=f,
            response_format=resp_format,
            language=lang
        )
    
    path = Path(input_path)
    if resp_format == "text":
        output_path = f'{path.parent}/{path.stem}.txt'
    else:
        output_path = f'{path.parent}/{path.stem}.srt'

    output_path = Path(output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    return transcript, output_path

audio_file = './data/youtube_download.mp3'

print('- [음성 파일 경로] {audio_file}\n')
r_format = 'srt'

transcript, output_path = audio_transcribe(audio_file, r_format)
print(f"- [텍스트 추출  형식] {r_format}\n")
print(f"- [출력파일] {output_path.name}")
print('-' * 50)
print(f"- [음성 추출 결과(일부 출력)]\n {transcript[:137]}\n")