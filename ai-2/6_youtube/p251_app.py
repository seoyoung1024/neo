from email import message
from urllib3 import response
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
import textwrap

def get_video_id(video_url):
    video_id = video_url.split('v=')[1][:11]

    return video_id

video_url = "https://www.youtube.com/watch?v=pSJrML-TTmI"
video_id = get_video_id(video_url)

try:
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

    try:
        transcript_obj = transcript_list.find_transcript(['ko'])
    except:
        transcript_obj = transcript_list.find_generated_transcript(['ko'])
    
    transcript = transcript_obj.fetch()
    text_formatter = TextFormatter().format_transcript(transcript)
    text_info = text_formatterted.replace('\n'," ")

    shorten_text_info = textwrap.shorten(text_info, width=150, placeholder=' [...이하 생략...]')
    print(shorten_text_info, end='\n')

except TranscriptsDisabled:
    print("해당 URL의 자막이 비활성화되어 있습니다.")
except NoTranscriptFound:
    print("이 영상에는 한국어 자막(수동자동 생성 포함)이 없습니다.")
except Exception as e:
    print("예상치 못한 오류가 발생했습니다.", e)


def answer_from_given_info(question_info, prompt):
    user_content = f'{prompt} 다음 내용을 바탕으로 질문으로 답해줘. {question_info}'

    message = [
        {"role": "user", "content": user_content},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=100,
        temperature=0.2,
    )

    return response['choices'][0]['message']['content']

question_info = text_info
prompt = "허준이 교수가 받은 상은 무엇인가요?"
print(prompt)
response = answer_from_given_info(question_info, prompt)
print(response)
print('-' * 50)

question_info = text_info
prompt = "허준이 교수는 어느 대학 교수인가요?"
print(prompt)
response = answer_from_given_info(question_info, prompt)
print(response)
print('-' * 50)