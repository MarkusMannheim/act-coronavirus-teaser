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
      await page.goto("https://www.health.act.gov.au/about-our-health-system/novel-coronavirus-covid-19/confirmed-case-details");
      await page.waitForSelector(".clearfix tbody");
      console.log("scrape ACT page");
      let actData = await page.evaluate(function() {
        let rows = document.querySelector(".clearfix tbody").querySelectorAll("tr td:nth-child(2)");
        return { actConfirmedCases: rows[1].innerText,
                 actNegativeTests: rows[2].innerText,
                 actRecovered: rows[3].innerText
               };
      });
      console.log(actData);
      console.log("load NSW page");
      await page.goto("https://www.health.nsw.gov.au/Infectious/diseases/Pages/covid-19-latest.aspx");
      await page.waitForSelector(".moh-rteTable-6");
      console.log("scrape NSW page");
      let nswData = await page.evaluate(function() {
        let names = document.querySelectorAll(".moh-rteTable-6")[4].querySelectorAll("tr td:first-child");
        let cases = document.querySelectorAll(".moh-rteTable-6")[4].querySelectorAll("tr td:last-child");
        data = {};
        councils = ["Queanbeyan-Palerang Regional", "Gouldburn Mulwaree", "Eurobodalla", "Yass Valley", "Snowy Monaro Regional"]
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
      console.log("./latestCount.json written");
    });
  })
  .catch(console.error);
