import puppeteer from "puppeteer";

const sleep = async (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const ext = '/app/extension/';
const PORT = process.env.PORT ?? "1337";
const FLAG = process.env.FLAG ?? "fwectf{fake_flag}";

export const visit = async (url) => {
  console.log(`Start visiting: ${url}`);
  
  const browser = await puppeteer.launch({
    headless: "new",
    pipe: true,
    executablePath: "/usr/bin/chromium",
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      '--js-flags="--noexpose_wasm"',
      `--disable-extensions-except=${ext}`,
      `--load-extension=${ext}`
    ],
    dumpio: true
  });
  
  try {
    const page1 = await browser.newPage();
    await page1.goto(`http://localhost:1337/`, { timeout: 3000 });
    await page1.waitForSelector('meta[memopad-extensionId]', { timeout: 3000 });
    await page1.evaluate((flag) => {
      window.postMessage({type: "create", payload: flag});
    }, FLAG);
    const extensionId = await page1.evaluate('document.querySelector("meta[memopad-extensionId]").getAttribute("memopad-extensionId")')

    await page1.goto(url, { timeout: 5000 });
    await sleep(5000);

    await page1.goto(`chrome-extension://${extensionId}/popup.html`, { timeout: 5000 });
    await page1.waitForSelector('.memo-url', { timeout: 3000 });
    const els = await page1.$$('.memo-url');
    await els[els.length - 1].click();
    await sleep(5000);
    await page1.close();
    
    
  } catch (e) {
    console.error(e);
  }
  
  await browser.close();
  
  console.log(`End visiting: ${url}`);
};
