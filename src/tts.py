import os
import requests
import playsound

"""
Speaker: 四国めたん, ノーマル id: 2
Speaker: 四国めたん, あまあま id: 0
Speaker: 四国めたん, ツンツン id: 6
Speaker: 四国めたん, セクシー id: 4
Speaker: 四国めたん, ささやき id: 36
Speaker: 四国めたん, ヒソヒソ id: 37
Speaker: ずんだもん, ノーマル id: 3
Speaker: ずんだもん, あまあま id: 1
Speaker: ずんだもん, ツンツン id: 7
Speaker: ずんだもん, セクシー id: 5
Speaker: ずんだもん, ささやき id: 22
Speaker: ずんだもん, ヒソヒソ id: 38
Speaker: ずんだもん, ヘロヘロ id: 75
Speaker: ずんだもん, なみだめ id: 76
Speaker: 春日部つむぎ, ノーマル id: 8
Speaker: 雨晴はう, ノーマル id: 10
Speaker: 波音リツ, ノーマル id: 9
Speaker: 波音リツ, クイーン id: 65
Speaker: 玄野武宏, ノーマル id: 11
Speaker: 玄野武宏, 喜び id: 39
Speaker: 玄野武宏, ツンギレ id: 40
Speaker: 玄野武宏, 悲しみ id: 41
Speaker: 白上虎太郎, ふつう id: 12
Speaker: 白上虎太郎, わーい id: 32
Speaker: 白上虎太郎, びくびく id: 33
Speaker: 白上虎太郎, おこ id: 34
Speaker: 白上虎太郎, びえーん id: 35
Speaker: 青山龍星, ノーマル id: 13
Speaker: 青山龍星, 熱血 id: 81
Speaker: 青山龍星, 不機嫌 id: 82
Speaker: 青山龍星, 喜び id: 83
Speaker: 青山龍星, しっとり id: 84
Speaker: 青山龍星, かなしみ id: 85
Speaker: 青山龍星, 囁き id: 86
Speaker: 冥鳴ひまり, ノーマル id: 14
Speaker: 九州そら, ノーマル id: 16
Speaker: 九州そら, あまあま id: 15
Speaker: 九州そら, ツンツン id: 18
Speaker: 九州そら, セクシー id: 17
Speaker: 九州そら, ささやき id: 19
Speaker: もち子さん, ノーマル id: 20
Speaker: もち子さん, セクシー／あん子 id: 66
Speaker: もち子さん, 泣き id: 77
Speaker: もち子さん, 怒り id: 78
Speaker: もち子さん, 喜び id: 79
Speaker: もち子さん, のんびり id: 80
Speaker: 剣崎雌雄, ノーマル id: 21
Speaker: WhiteCUL, ノーマル id: 23
Speaker: WhiteCUL, たのしい id: 24
Speaker: WhiteCUL, かなしい id: 25
Speaker: WhiteCUL, びえーん id: 26
Speaker: 後鬼, 人間ver. id: 27
Speaker: 後鬼, ぬいぐるみver. id: 28
Speaker: 後鬼, 人間（怒り）ver. id: 87
Speaker: 後鬼, 鬼ver. id: 88
Speaker: No.7, ノーマル id: 29
Speaker: No.7, アナウンス id: 30
Speaker: No.7, 読み聞かせ id: 31
Speaker: ちび式じい, ノーマル id: 42
Speaker: 櫻歌ミコ, ノーマル id: 43
Speaker: 櫻歌ミコ, 第二形態 id: 44
Speaker: 櫻歌ミコ, ロリ id: 45
Speaker: 小夜/SAYO, ノーマル id: 46
Speaker: ナースロボ＿タイプＴ, ノーマル id: 47
Speaker: ナースロボ＿タイプＴ, 楽々 id: 48
Speaker: ナースロボ＿タイプＴ, 恐怖 id: 49
Speaker: ナースロボ＿タイプＴ, 内緒話 id: 50
Speaker: †聖騎士 紅桜†, ノーマル id: 51
Speaker: 雀松朱司, ノーマル id: 52
Speaker: 麒ヶ島宗麟, ノーマル id: 53
Speaker: 春歌ナナ, ノーマル id: 54
Speaker: 猫使アル, ノーマル id: 55
Speaker: 猫使アル, おちつき id: 56
Speaker: 猫使アル, うきうき id: 57
Speaker: 猫使ビィ, ノーマル id: 58
Speaker: 猫使ビィ, おちつき id: 59
Speaker: 猫使ビィ, 人見知り id: 60
Speaker: 中国うさぎ, ノーマル id: 61
Speaker: 中国うさぎ, おどろき id: 62
Speaker: 中国うさぎ, こわがり id: 63
Speaker: 中国うさぎ, へろへろ id: 64
Speaker: 栗田まろん, ノーマル id: 67
Speaker: あいえるたん, ノーマル id: 68
Speaker: 満別花丸, ノーマル id: 69
Speaker: 満別花丸, 元気 id: 70
Speaker: 満別花丸, ささやき id: 71
Speaker: 満別花丸, ぶりっ子 id: 72
Speaker: 満別花丸, ボーイ id: 73
Speaker: 琴詠ニア, ノーマル id: 74
Speaker: Voidoll, ノーマル id: 89
Speaker: ぞん子, ノーマル id: 90
Speaker: ぞん子, 低血圧 id: 91
Speaker: ぞん子, 覚醒 id: 92
Speaker: ぞん子, 実況風 id: 93
Speaker: 中部つるぎ, ノーマル id: 94
Speaker: 中部つるぎ, 怒り id: 95
Speaker: 中部つるぎ, ヒソヒソ id: 96
Speaker: 中部つるぎ, おどおど id: 97
Speaker: 中部つるぎ, 絶望と敗北 id: 98
"""


def synthesize_voice(text, speaker=1, filename="./data/output.wav"):
    query_payload = {"text": text, "speaker": speaker}
    query_response = requests.post(
        f"http://localhost:50021/audio_query", params=query_payload
    )

    if query_response.status_code != 200:
        print(f"Error in audio_query: {query_response.text}")
        return

    query = query_response.json()

    synthesis_payload = {"speaker": speaker}
    synthesis_response = requests.post(
        f"http://localhost:50021/synthesis", params=synthesis_payload, json=query
    )

    if synthesis_response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(synthesis_response.content)
    else:
        print(f"Error in synthesis: {synthesis_response.text}")


def text_to_speech(text, speaker=1):
    filename = f"./tmp/voicevox_output_{speaker}.wav"
    synthesize_voice(text, speaker=speaker, filename=filename)
    playsound.playsound(filename)
    os.remove(filename)


if __name__ == "__main__":
    text = "ぽぽぽぽーん"
    text_to_speech(text)
