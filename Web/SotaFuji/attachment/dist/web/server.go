package main

import (
	"fmt"
	"log"
	"net/http"
  "os"
)

func main() {
  flag := os.Getenv("FLAG")
  if flag == "" {
      flag = "fwectf{fake_flag}"
  }
	fuji := `
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>藤井竜王の現在のタイトル</title>
  <style>
    table {
      border-collapse: collapse;
      width: 100%;
      max-width: 600px;
      margin: 20px auto;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background-color: #f0f0f0;
    }
    h1 {
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>藤井竜王の現在のタイトル (Sota Fuji's current titles)</h1>
  <table>
    <thead>
      <tr>
        <th>タイトル</th>
        <th>期数</th>
        <th>詳細</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>竜王</td>
        <td>4期</td>
        <td>（第34期-2021年度・35・36期・37期）</td>
      </tr>
      <tr>
        <td>名人</td>
        <td>2期</td>
        <td>（第81期-2023年度・82期）</td>
      </tr>
      <tr>
        <td>王位</td>
        <td>5期</td>
        <td>（第61期-2020年度・62～65期）</td>
      </tr>
      <tr>
        <td>叡王</td>
        <td>3期</td>
        <td>（第6期-2021年度・7・8期）</td>
      </tr>
      <tr>
        <td>王座</td>
        <td>2期</td>
        <td>（第71期-2023年度・第72期）</td>
      </tr>
      <tr>
        <td>棋王</td>
        <td>3期</td>
        <td>（第48期-2022年度・49期・50期）</td>
      </tr>
      <tr>
        <td>王将</td>
        <td>3期</td>
        <td>（第71期-2021年度・72・73期）</td>
      </tr>
      <tr>
        <td>棋聖</td>
        <td>5期</td>
        <td>（第91期-2020年度・92～95期）</td>
      </tr>
    </tbody>
  </table>
</body>
</html>
`
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/":
			w.Header().Set("Content-Type", "text/html")
			fmt.Println("/")
			fmt.Fprint(w, fuji)
		case "/flag":
			w.Header().Set("Content-Type", "text/plain")
			fmt.Println("/flag")
			fmt.Fprint(w, flag)
		default:
			http.NotFound(w, r)
		}
	})

	log.Println("Server listening on :4001")
	if err := http.ListenAndServe(":4001", nil); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
