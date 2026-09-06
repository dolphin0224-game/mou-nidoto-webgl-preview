"""Discord report starter. Python 3.10+, standard library only."""
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def public_url(value):
    p = urllib.parse.urlsplit(value)
    if p.scheme not in ("http", "https") or not p.hostname or p.username or p.password:
        raise ValueError("公開ゲームURLの形式を確認してください")
    host = p.hostname.lower()
    if host == "localhost" or "." not in host or host.endswith((".localhost", ".local", ".internal")):
        raise ValueError("他のPCから開ける公開URLが必要です")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError("ローカルIPを公開URLには使えません")
    if any(c.isspace() for c in value) or "discord.com/api/webhooks/" in value:
        raise ValueError("ゲームURLを確認してください")
    return value


def build(config, report):
    for key in ("id", "completed_at"):
        if not isinstance(report.get(key), str) or not report[key].strip():
            raise ValueError("idとcompleted_atは必須です")
    for key in ("changes", "verification", "unresolved"):
        if not isinstance(report.get(key), list) or any(not isinstance(x, str) or not x.strip() for x in report[key]):
            raise ValueError("changes/verification/unresolvedは文字列の配列です")
    if not report["changes"]:
        return None
    status = report.get("deployment_status")
    if status not in ("published", "pending", "failed"):
        raise ValueError("deployment_statusはpublished/pending/failedです")
    url = ""
    if status == "published":
        url = public_url(report.get("game_url") or config.get("game_url") or "")
    title = "修正・公開完了" if status == "published" else "変更済み・公開" + ("失敗" if status == "failed" else "待ち")
    lines = [title, "プレイURL: " + url if url else "確認リンク未用意", "プロジェクト: " + str(config.get("project", "")),
             "作業者: " + str(config.get("author", "")), "日時: " + report["completed_at"], "報告ID: " + report["id"]]
    for label, key in (("変更項目", "changes"), ("確認結果", "verification"), ("未解決事項", "unresolved")):
        lines += ["", label] + ["・" + x for x in (report[key] or (["未確認"] if key == "verification" else ["記載なし"]))]
    if status != "published":
        lines += ["", "公開状況: " + str(report.get("deployment_note", "未確認"))]
    content = "\n".join(lines)
    if re.search(r"https?://[^\s]*discord(?:app)?\.com/api/webhooks/", content, re.I):
        raise ValueError("報告にWebhook URLを含めることはできません")
    return content


def wire(content):
    payload = {"content": content, "allowed_mentions": {"parse": []}}
    if len(content.encode("utf-16-le")) // 2 <= 2000:
        return json.dumps(payload, ensure_ascii=False).encode(), "application/json"
    # Keep the play URL first and preserve the entire report in an attachment.
    first = content.splitlines()[:2]
    summary = "\n".join(first)
    if len(summary.encode("utf-16-le")) // 2 > 1800:
        raise ValueError("リンクが長すぎます。共有URLを確認してください")
    payload["content"] = summary + "\n詳細は添付のchanges.txtを参照してください。"
    boundary = "report-" + uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"payload_json\"\r\nContent-Type: application/json\r\n\r\n".encode()
            + json.dumps(payload, ensure_ascii=False).encode()
            + f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"files[0]\"; filename=\"changes.txt\"\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n".encode()
            + content.encode() + f"\r\n--{boundary}--\r\n".encode())
    return body, "multipart/form-data; boundary=" + boundary


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def transmit(url, data, content_type, thread_id=""):
    query = {"wait": "true"}
    if thread_id:
        if not re.fullmatch(r"[0-9]{15,22}", thread_id):
            raise ValueError("DISCORD_THREAD_IDの形式を確認してください")
        query["thread_id"] = thread_id
    endpoint = url + "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(endpoint, data=data, headers={"Content-Type": content_type, "User-Agent": "GameDiscordReporter/0.2"})
    with urllib.request.build_opener(NoRedirect).open(request, timeout=20) as response:
        result = json.load(response)
    if not isinstance(result.get("id"), str):
        raise ValueError("送信結果を確認できません")
    return result["id"]


def deliver(config, report, content, state_dir, url, thread_id="", sender=transmit):
    if not re.fullmatch(r"https://discord\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+", url):
        raise ValueError("DISCORD_WEBHOOK_URLを設定してください（値は表示しません）")
    body, content_type = wire(content)
    key = hashlib.sha256((url + "\n" + thread_id + "\n" + report["id"]).encode()).hexdigest()
    digest = hashlib.sha256(content.encode()).hexdigest()
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / (key + ".json")
    lock = state_dir / (key + ".lock")
    try:
        lock.mkdir()
    except FileExistsError:
        print("処理中または前回中断。状態を確認してください。")
        return 3
    try:
        old = read(path) if path.exists() else {}
        if old and old.get("digest") != digest:
            raise ValueError("同じ報告IDで内容が変わっています。意図した新規報告には新しいIDを使用してください")
        if old.get("status") == "sent":
            print("送信済み。重複投稿を省略しました。")
            return 0
        if old.get("status") in ("unknown", "sending"):
            print("前回の結果が不明です。Discordを確認してから再送してください。")
            return 3
        state = {"status": "sending", "digest": digest, "report": report, "content": content}
        save(path, state)
        try:
            message_id = sender(url, body, content_type, thread_id)
        except urllib.error.HTTPError as e:
            state["status"] = "pending" if 400 <= e.code < 500 else "unknown"
            state["http_status"] = e.code
            if e.code == 429:
                try:
                    delay = float(json.loads(e.read()).get("retry_after", 0))
                    state["retry_after_seconds"] = delay
                    print("送信制限。再試行までの秒数:", delay)
                except (ValueError, TypeError):
                    pass
            save(path, state)
            print("未送信または結果不明。保存した状態を確認してください。HTTP", e.code)
            return 3
        except Exception:
            state["status"] = "unknown"
            save(path, state)
            print("送信結果不明。報告を保存しました。自動再送は停止します。")
            return 3
        state.update(status="sent", message_id=message_id)
        save(path, state)
        print("Discord投稿成功。メッセージID:", message_id)
        return 0
    finally:
        lock.rmdir()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        config, report = read(args.config), read(args.report)
        content = build(config, report)
        if content is None:
            print("変更なし。投稿しません。")
            return 0
        if args.dry_run:
            wire(content)
            print(content)
            return 0
        if config.get("enabled") is not True:
            print("自動投稿は無効です。")
            return 0
        state = Path(config["state_dir"])
        if not state.is_absolute():
            state = Path(args.config).resolve().parent / state
        thread_id = os.environ.get("DISCORD_THREAD_ID", "") or str(config.get("thread_id", ""))
        return deliver(config, report, content, state, os.environ.get("DISCORD_WEBHOOK_URL", ""), thread_id)
    except Exception:
        # Do not print arbitrary exceptions, which may contain tokens or config contents.
        print("入力・設定または状態保存のエラー。設定と報告の形式、保存先を確認してください。", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
