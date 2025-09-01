
<br>

## 大会ルール(日本語)

* 各チャレンジに、「フラグ」と呼ばれる特定の文字列が隠されています。提示された要件をクリアしたり、脆弱性を突いたりすることによって、このフラグを入手しましょう。
* 正しいフラグを提出すると、そのチームに点数が与えられます。
* 特に問題説明文にて言及されない限り、フラグは次の形式で記述されます: `fwectf{Th1s_is_a_sample_Flag}` (正規表現`fwectf\{[0-9a-zA-Z_!?]+\}`)
* 開催時間: 2025.8.29 19:00 ~ 2025.8.31 19:00 (JST)
* 一部を除くチャレンジの点数は、解いたプレイヤーの数に応じて変動します。最終的な総得点は、終了時のチャレンジの点数の合計となります。

### Discordサーバーについて

[Discordサーバー](https://discord.com/invite/gRX4HHPpvg)

CTFに関するアナウンスはDiscordサーバーにて行われます。

CTFに関する質問や報告がありましたら`#ask-for-admin` チャンネルでチケットを作成してください。

Discordでは`#rules`をよく読み、それに従ってください

### 禁止事項

* CTF終了前に問題の解法・フラグ・ヒントを公にすること
* 異なるチーム同士で問題の解法・フラグ・ヒントを共有すること。また、情報交換の提案を持ちかけること
* 総当りによるフラグの送信
* 当CTFで覚えた知識を自分以外が管理する外部のサイトで悪用すること
* スコアサイトへ意図的な攻撃
* 問題サーバーに負荷がかかるような自動探索ツールの利用(例: dirbuster, sqlmap)
* 他チーム及びCTF運営チームに迷惑をかける一切の行為

### 備考
* 1チームあたりの参加人数に上限はありません
* 問題の説明・アナウンス等は日本語と英語で行われます。
* 一部日本語話者に若干有利な問題があります。このディスアドバンテージに対する補償は行いません。
* インフラの問題等の理由により、開始・終了時間が前後する可能性があります。これらのアナウンスはCTFプラットフォーム上とDiscordで行われます
* ルールに関する最終的な決定権はCTF運営チームが持ちます
* 優勝商品はありません！ごめんね！

*****

## Rules(English)

### Competition Rules
* Each challenge contains a specific string called a "flag". Obtain this flag by fulfilling the given requirements or exploiting a vulnerability.
* Submitting a correct flag awards points to your team.
* Unless otherwise noted in the problem statement, flags follow this format: `fwectf{Th1s_is_a_sample_Flag}` (regex: `fwectf\{[0-9a-zA-Z_!?]+\}`)
* Event duration: 2025.8.29 10:00 ~ 2025.8.31 10:00 (UTC)
* Except for a few challenges, points are adjusted based on the number of solves. Your final score is the sum of all challenge points at the end.

### About the Discord Server
[Discord Server](https://discord.com/invite/gRX4HHPpvg)

All the announcements will be made on the Discord server.

If you have questions or reports about the CTF, please open a ticket in the `#ask-for-admin` channel.

Please read and follow the rules in `#rules` channel on Discord.

### Prohibited Actions
* Publicly sharing solutions, flags, or hints before the CTF ends
* Sharing solutions, flags, or hints between different teams, or asking other competitors for those information
* Brute forcing flags on CTF platform
* Misusing knowledge gained in this CTF on any external site not managed by you
* Intentional attacks on the CTF platform
* Using automated enumeration tools that overload the challenge servers (including, but not limited to dirbuster, sqlmap)
* Any behavior that disturbs other teams or the CTF organizers

### Notes
* There is no limit on the size of your team.
* Problem statements and announcements will be provided in both Japanese and English.
* Some challenges may slightly favor Japanese speakers; no compensation will be provided for this disadvantage.
* Start and end times may shift due to infrastructure issues. Announcements will be made on the CTF platform and Discord.
* The CTF organizers reserve the final right to interpret the rules.
* There is no prize for the winner. Sorry!


<style>
.wave-tables table{
  min-width: 420px;
  border-collapse: separate;
  border-spacing: 0;
  border: 1px solid var(--bs-info-border-subtle);
  box-shadow: 0 2px 8px rgba(0,0,0,.04);
}

.wave-tables table th,
.wave-tables table td{
  padding: 4px 16px;
  border-bottom: 1px solid var(--bs-info-border-subtle);
  vertical-align: middle;
  text-align: left;
  white-space: nowrap;
}

.wave-tables table tbody tr:last-child td{
  border-bottom: none;
}

.wave-tables table tbody tr:nth-child(odd){
  background: var(--bs-secondary-bg);
}
.wave-tables table tbody tr:hover{
  background: var(--bs-tertiary-bg);
}

.wave-tables table th:first-child,
.wave-tables table td:first-child{
  width: 50%;
}
</style>


## 出題スケジュール(Schedule)

このCTFでは問題が3段階に分けて出題されます。出題される時間帯と、問題のジャンル・想定難易度は以下のとおりです。

In this CTF, the challenges are released in three stages. The release schedule, along with the category and expected difficulty of each challenge, is as follows.

<br>

<div class="wave-tables">
  
### Wave 1 (29th 7:00PM JST, 29th 10:00AM UTC) 

| Category       | Difficulty |
| -------------- | ---------- |
| Misc           | Beginner   |
| Misc           | Medium     |
| Misc           | Medium     |
| Misc           | Hard       |
| Forensic/OSINT | Beginner   |
| Forensic/OSINT | Beginner   |
| Forensic/OSINT | Beginner   |
| Forensic/OSINT | Easy       |
| Forensic/OSINT | Medium     |
| Forensic/OSINT | Medium     |
| Crypto         | Beginner   |
| Crypto         | Easy       |
| Crypto         | Medium     |
| Crypto         | Hard       |
| Rev            | Beginner   |
| Rev            | Medium     |
| Rev            | Medium     |
| Rev            | Hard       |
| Pwn            | Beginner   |
| Pwn            | Easy       |
| Pwn            | Easy       |
| Pwn            | Hard       |
| Web            | Beginner   |
| Web            | Easy       |
| Web            | Medium     |
| Web            | Hard       |

<br>

### Wave 2 (30th 7:00AM JST, 29th 10:00PM UTC) 

| Category       | Difficulty |
| -------------- | ---------- |
| Misc           | Easy       |
| Misc           | Medium     |
| Forensic/OSINT | Easy       |
| Forensic/OSINT | Easy       |
| Forensic/OSINT | Hard       |
| Crypto         | Medium     |
| Crypto         | Medium     |
| Rev            | Easy       |
| Rev            | Hard       |
| Pwn            | Medium     |
| Pwn            | Hard       |
| Web            | Medium     |
| Web            | Hard       |

<br>

### Wave 3 (30th 7:00PM JST, 30th 10:00AM UTC) 

| Category       | Difficulty |
| -------------- | ---------- |
| Misc           | Medium     |
| Forensic/OSINT | Medium     |
| Forensic/OSINT | Medium     |
| Forensic/OSINT | Medium     |
| Crypto         | Easy       |
| Crypto         | Easy       |
| Rev            | Easy       |
| Rev            | Medium     |
| Pwn            | Medium     |
| Web            | Medium     |
| Web            | Medium     |

</div>


