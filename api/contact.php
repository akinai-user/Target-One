<?php
declare(strict_types=1);
header('Content-Type: application/json; charset=UTF-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
ini_set('session.use_strict_mode', '1');
session_set_cookie_params([
    'httponly' => true,
    'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
    'samesite' => 'Strict',
]);
session_start();
function respond(int $code, array $data): void
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit();
}
$config = require __DIR__ . '/config.php';
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['token'])) {
    $_SESSION['token'] = $_SESSION['token'] ?? bin2hex(random_bytes(32));
    respond(200, ['token' => $_SESSION['token']]);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(405, ['message' => 'POSTで送信してください。']);
}
if (!$config['enabled']) {
    respond(503, ['message' => 'お問い合わせの受付準備中です。お電話でお問い合わせください。']);
}
if (
    !filter_var($config['recipient'], FILTER_VALIDATE_EMAIL) ||
    !filter_var($config['from'], FILTER_VALIDATE_EMAIL)
) {
    respond(503, ['message' => '送信先が設定されていません。']);
}
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin === '' || parse_url($origin, PHP_URL_HOST) !== $config['allowed_host']) {
    respond(403, ['message' => '送信元を確認できません。']);
}
if (
    empty($_SESSION['token']) ||
    !is_string($_POST['token'] ?? null) ||
    !hash_equals($_SESSION['token'], $_POST['token'])
) {
    respond(403, ['message' => '有効期限が切れました。ページを再読み込みしてください。']);
}
if (!empty($_POST['website_check'])) {
    respond(422, ['message' => '送信を受け付けられません。']);
}
if (time() - ($_SESSION['last_submission'] ?? 0) < 60) {
    respond(429, ['message' => 'しばらく時間をおいてから再送信してください。']);
}
if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 40000) {
    respond(413, ['message' => '入力内容が長すぎます。']);
}
function value(string $key): string
{
    $v = $_POST[$key] ?? '';
    return is_string($v) ? trim($v) : '';
}
$type = value('form_type');
if (!in_array($type, ['無料相談', '資料請求'], true)) {
    respond(422, ['message' => 'お問い合わせ種別をご確認ください。']);
}
foreach (['company', 'name', 'email', 'consent'] as $key) {
    if (value($key) === '') {
        respond(422, ['message' => '必須項目をご入力ください。']);
    }
}
if (value('consent') !== '1' || !filter_var(value('email'), FILTER_VALIDATE_EMAIL)) {
    respond(422, ['message' => 'メールアドレスと同意欄をご確認ください。']);
}
$industries = [
    '歯科・クリニック',
    'ジム・フィットネス',
    'エステ・整体',
    '飲食店',
    '不動産・住宅',
    '教育・スクール',
    'その他',
];
$selected = $_POST['industry'] ?? [];
if (!is_array($selected) || !$selected || array_diff($selected, $industries)) {
    respond(422, ['message' => '業種を選択してください。']);
}
if ($type === '無料相談') {
    foreach (['phone', 'url', 'consultation', 'area', 'advertising'] as $key) {
        if (value($key) === '') {
            respond(422, ['message' => '相談内容の必須項目をご確認ください。']);
        }
    }
    if (
        !filter_var(value('url'), FILTER_VALIDATE_URL) ||
        !in_array(parse_url(value('url'), PHP_URL_SCHEME), ['http', 'https'], true)
    ) {
        respond(422, ['message' => 'HPのURLをご確認ください。']);
    }
    if (
        !in_array(value('consultation'), ['無料オンライン相談希望', '無料電話相談希望'], true) ||
        !in_array(value('area'), ['店舗半径', 'エリア限定', '相談したい'], true) ||
        !in_array(value('advertising'), ['あり', 'なし'], true)
    ) {
        respond(422, ['message' => '選択内容をご確認ください。']);
    }
    $holidays = json_decode(file_get_contents(__DIR__ . '/holidays.json'), true);
    $minimum = new DateTimeImmutable('today', new DateTimeZone('Asia/Tokyo'));
    $count = 0;
    while ($count < 3) {
        $minimum = $minimum->modify('+1 day');
        if (
            (int) $minimum->format('N') < 6 &&
            !in_array($minimum->format('Y-m-d'), $holidays, true)
        ) {
            $count++;
        }
    }
    for ($i = 1; $i <= 5; $i++) {
        $day = value('date' . $i);
        $time = value('time' . $i);
        if ($i > 3 && $day === '' && $time === '') {
            continue;
        }
        $date = DateTimeImmutable::createFromFormat('!Y-m-d', $day, new DateTimeZone('Asia/Tokyo'));
        if (
            !$date ||
            $date->format('Y-m-d') !== $day ||
            $date < $minimum ||
            (int) $date->format('N') > 5 ||
            in_array($day, $holidays, true) ||
            !in_array($time, ['10:00', '11:00', '13:00', '14:00', '15:00', '16:00', '17:00'], true)
        ) {
            respond(422, [
                'message' => '希望日は3営業日以降の平日と、選択肢にある時間をご指定ください。',
            ]);
        }
    }
}
$labels = [
    'form_type' => 'お問い合わせ種別',
    'company' => '会社名',
    'name' => 'お名前',
    'url' => 'HP',
    'email' => 'メールアドレス',
    'phone' => '電話番号',
    'industry' => '業種',
    'consultation' => 'ご相談方法',
    'area' => '配信エリア',
    'advertising' => 'WEB広告',
    'message' => 'ご質問',
    'position' => '役職',
    'source' => 'きっかけ',
];
for ($i = 1; $i <= 5; $i++) {
    $labels['date' . $i] = '第' . $i . '希望日';
    $labels['time' . $i] = '第' . $i . '希望時間';
}
$body = 'Target-One サイトからの' . $type . "\n\n";
foreach ($labels as $key => $label) {
    $text = $key === 'industry' ? implode('、', $selected) : value($key);
    if (strlen($text) > 12000) {
        respond(422, ['message' => '入力内容が長すぎます。']);
    }
    $body .= $label . '：' . $text . "\n\n";
}
$headers = [
    'From' => $config['from'],
    'Reply-To' => value('email'),
    'Content-Type' => 'text/plain; charset=UTF-8',
];
if (preg_match('/[\r\n]/', value('email'))) {
    respond(422, ['message' => 'メールアドレスをご確認ください。']);
}
$subject = '=?UTF-8?B?' . base64_encode('【Target-One】' . $type) . '?=';
if (!mail($config['recipient'], $subject, $body, $headers)) {
    respond(502, ['message' => 'メールを送信できませんでした。お電話にてお問い合わせください。']);
}
$_SESSION['last_submission'] = time();
unset($_SESSION['token']);
respond(200, ['success' => true]);
