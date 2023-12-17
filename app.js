const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const https = require('https');

const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));

const base_url = "https://onlinecertificates.gitam.edu/View_Result_Grid2.aspx?QT=QRCODE$";

app.get('/', (req, res) => {
  res.render('index', { results: null, error: null });
});

app.post('/scrape', async (req, res) => {
  const input = req.body.input;

  if (!input) {
    res.render('index', { results: null, error: 'Please enter a valid input.' });
    return;
  }

  const url = `${base_url}${input}$5$nov$2023$R$`;
  const results = [];

  try {
    const httpsAgent = new https.Agent({ rejectUnauthorized: false });
    const response = await axios.get(url, { httpsAgent });

    if (response.status === 200) {
      const $ = cheerio.load(response.data);
      const lblname_tag = $("#lblname");
      const lblgpa_tag = $("#lblgpa");
      const lblcgpa_tag = $("#lblcgpa");

      if (lblname_tag.text() !== "lblname") {
        const result_data = {
          "Roll Number": input,
          "Name": lblname_tag.text() || "N/A",
          "GPA": lblgpa_tag.text() || "N/A",
          "CGPA": lblcgpa_tag.text() || "N/A",
          "URL": url
        };

        results.push(result_data);
      }
    } else {
      console.log(`Failed to retrieve the page for URL ${url}. Status code: ${response.status}`);
    }
  } catch (error) {
    console.error(`Error occurred while fetching URL ${url}: ${error.message}`);
  }

  res.render('index', { results });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
