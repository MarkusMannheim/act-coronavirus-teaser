puppeteer = require("puppeteer"),
d3 = require("d3"),
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
                 actRecovered: cells[2].innerText
               };
      });
      console.log(actData);
      console.log("load NSW page");
      await page.goto("https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-lga.aspx");
      await page.waitForSelector(".moh-rteTable-6");
      console.log("scrape NSW page");
      let nswData = await page.evaluate(function() {
        let names = document.querySelector(".moh-rteTable-6").querySelectorAll("tbody tr td:first-child");
        let cases = document.querySelector(".moh-rteTable-6").querySelectorAll("tbody tr td:last-child");
        data = {};
        councils = ["Queanbeyan-Palerang Regional", "Goulburn Mulwaree", "Eurobodalla", "Yass Valley", "Snowy Monaro Regional"];
        for (i = 0; i < names.length; i++) {
          if (councils.includes(names[i].innerText)) {
            data[names[i].innerText.replace(" Regional", "")] = cases[i].innerText;
          }
        }
        return data;
      });
      console.log(nswData);
      browser.close();
      data = Object.assign(actData, nswData);
      return resolve(data);
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
