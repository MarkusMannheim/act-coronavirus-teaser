puppeteer = require("puppeteer"),
fs = require("fs");

async function scrape() {
  console.log("scrape()");
  browser = await puppeteer.launch({headless: true}),
  page = await browser.newPage();
  return new Promise(async function(resolve, reject) {
    console.log("begin promise()");
    try {
      console.log("load ACT page");
      await page.goto("https://www.covid19.act.gov.au/updates/confirmed-case-information");
      await page.waitForSelector("#table42313");
      console.log("scrape ACT page");
      let actData = await page.evaluate(function() {
        let cells = document.querySelectorAll("#table42313 td");
        return { actConfirmedCases: cells[0].innerText,
                 actNegativeTests: cells[1].innerText,
                 actRecovered: cells[2].innerText,
                 actDead: cells[3].innerText
               };
      });
      console.log(actData);
      browser.close();
      return resolve(actData);
    } catch (error) {
      return reject(error);
    }
  });
}

scrape()
  .then(function(data) {
    fs.writeFile("./latestCount.json", JSON.stringify(data), function(error) {
      console.log("latestCount.json written");
    });
  })
  .catch(console.error);
