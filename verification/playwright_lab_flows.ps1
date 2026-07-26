$ErrorActionPreference = "Stop"

$session = "topic04-verification"
$cli = @("--yes", "--package", "@playwright/cli", "playwright-cli", "-s=$session")
$code = @'
async page => {
  const errors = [];
  page.on('console', message => {
    if (message.type() === 'error' && !message.text().toLowerCase().includes('favicon')) {
      errors.push(message.text());
    }
  });
  const targets = [
    ['Lab01', 'http://127.0.0.1:5000/'],
    ['Lab02', 'http://127.0.0.1:5002/'],
    ['Lab03', 'http://127.0.0.1:5003/login'],
    ['Lab04 victim', 'http://127.0.0.1:5004/'],
    ['Lab04 attacker', 'http://127.0.0.1:9004/'],
    ['Lab05', 'http://127.0.0.1:5005/'],
    ['Lab06', 'http://127.0.0.1:5006/']
  ];
  for (const [name, url] of targets) {
    const response = await page.goto(url, {waitUntil: 'domcontentloaded'});
    if (!response || !response.ok()) throw new Error(`${name} returned ${response && response.status()}`);
    await page.locator('body').waitFor({state: 'visible'});
    if ((await page.locator('body').innerText()).trim().length < 20) throw new Error(`${name} body is empty`);
  }

  await page.goto('http://127.0.0.1:5003/login', {waitUntil: 'domcontentloaded'});
  await page.locator('input[name="username"]').fill('user_a');
  await page.locator('input[name="password"]').fill('UserA123!');
  await Promise.all([
    page.waitForURL('**/products'),
    page.locator('button[type="submit"]').click()
  ]);
  await page.locator('form[action="/cart/add"] button[type="submit"]').first().click();
  await page.waitForURL('**/cart');
  if (errors.length) throw new Error(`Browser console errors: ${errors.join(' | ')}`);
  console.log(`PLAYWRIGHT_TOPIC04_PASS pages=${targets.length} lab03_login_and_cart=pass console_errors=0`);
}
'@

try {
    $openOutput = & npx @cli open about:blank 2>&1 | Out-String
    Write-Output $openOutput.TrimEnd()
    if ($LASTEXITCODE -ne 0 -or $openOutput -match "### Error") {
        throw "Unable to start Playwright CLI session."
    }
    $flowOutput = & npx @cli run-code $code 2>&1 | Out-String
    Write-Output $flowOutput.TrimEnd()
    if ($LASTEXITCODE -ne 0 -or $flowOutput -match "### Error" -or $flowOutput -notmatch "PLAYWRIGHT_TOPIC04_PASS") {
        throw "Playwright flow failed."
    }
}
finally {
    & npx @cli close 2>$null
}
