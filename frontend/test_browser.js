import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
  page.on('requestfailed', request => console.log('REQUEST FAILED:', request.url(), request.failure().errorText));

  try {
    const url = process.argv[2] || 'http://localhost:5173';
    console.log("Navigating to", url);
    const response = await page.goto(url, {waitUntil: 'networkidle0'});
    console.log("Status:", response.status());
    const html = await page.content();
    console.log("HTML length:", html.length);
    const rootHtml = await page.evaluate(() => {
      const el = document.getElementById('root');
      return el ? el.innerHTML : 'NO ROOT ELEMENT';
    });
    console.log("Root innerHTML length:", rootHtml.length);
    if (rootHtml.length > 0) {
        console.log("Root innerHTML:", rootHtml.substring(0, 100) + '...');
    }
  } catch (e) {
    console.error("Test error:", e);
  }
  
  await browser.close();
})();
