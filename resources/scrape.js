puppeteer = require("puppeteer"),
fs = require("fs");

async function scrape() {
  console.log("establish scraper ...");
  browser = await puppeteer.launch({headless: true}),
  page = await browser.newPage();
  return new Promise(async function(resolve, reject) {
    try {
      console.log("load ACT Health website ...");
      await page.goto("https://www.covid19.act.gov.au/updates/confirmed-case-information");
      await page.waitForSelector("#table42313");
      console.log("scrape data ...");
      data = await page.evaluate(function() {
        let cells = document.querySelectorAll("#table42313 td");
        let ages = document.querySelectorAll("td[headers='table81686r1c1'");
        let data = {
          cases: cells[0].innerText,
          negative: cells[1].innerText,
          recovered: cells[2].innerText,
          dead: cells[3].innerText,
          age1: ages[6].innerText,
          age2: ages[7].innerText,
          age3: ages[8].innerText,
          age4: ages[9].innerText,
          age5: ages[10].innerText,
          age6: ages[11].innerText,
        };
        return data;
      });
      console.log("collected these data:\n");
      for (key in data) {
        console.log(key + ": " + data[key]);
      }
      browser.close();
      return resolve(data);
    } catch (error) {
      return reject(error);
    }
  });
}

scrape()
  .then(function(data) {
    fs.writeFile("./latestCount.json", JSON.stringify(data), function(error) {
      console.log("\nlatestCount.json written");
    });
  })
  .catch(console.error);
