from openai import OpenAI

# 인스턴스 생성
client = OpenAI()

# Fine-tuning job 목록 가져오기
fine_tunes = client.fine_tuning.jobs.list()

# 실패한 fine-tuning job 출력
for fine_tune in fine_tunes.data:
    if fine_tune.status == 'failed':
        print(f'Failed fine-tuning job: {fine_tune.id}')
