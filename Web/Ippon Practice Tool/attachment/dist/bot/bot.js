import { firefox } from "playwright-firefox";
import crypto from "crypto";
const sleep = async (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export const visit = async (url, envs) => {
  console.log(`Start visiting: ${url}`);

  const browser = await firefox.launch({
    headless: true,
    firefoxUserPrefs: {
      "javascript.options.wasm": false,
      "javascript.options.baselinejit": false,
    },
  });
  const context = await browser.newContext();

  try {
    const page1 = await context.newPage();

    await page1.goto(envs.APP_URL + "/register", { timeout: 3000 });
    await page1.waitForSelector("#username", { timeout: 1000 });
    await page1.type("#username", "asusn-" + crypto.randomUUID());
    await page1.type("#password", "password-" + crypto.randomUUID());
    await page1.click("#submit");
    await page1.waitForSelector("#answer", { timeout: 1000 });
    await page1.type("#answer", envs.FLAG);
    await page1.click("#private");
    await page1.click("#submit");
    await sleep(1000);
    await page1.close();

    const page2 = await context.newPage();
    await page2.goto(url, { timeout: 5000 });
    await sleep(15 * 1000);
    await page2.close();
  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();

  console.log(`End visiting: ${url}`);
};
