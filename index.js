const request = require("request");
const cheerio = require("cheerio");
const log = require("signale");
const fs = require("fs");

if (!fs.existsSync("./stories")) {
  fs.mkdirSync("./stories");
}

if (!fs.existsSync("./metadata")) {
  fs.mkdirSync("./metadata");
}

if (!fs.existsSync("./metadata/images")) {
  fs.mkdirSync("./metadata/images");
}

const rabibashoriyo_url =
  "https://www.anandabazar.com/supplementary/rabibashoriyo/archive?page=1&slab=0&tnp=50";

get_recent_stories(rabibashoriyo_url);

/* Only for manual entry */
/*
 for ( var i = 1;i<=50;i++)
{
    var archive_url =
"https://www.anandabazar.com/supplementary/rabibashoriyo/archive?page="+i+"&slab=0&tnp=50";
    get_recent_stories(archive_url);
}
*/

function get_recent_stories(url) {
  const options = { url, headers: { "User-Agent": "request" } };

  request.get(options, (error, response, html) => {
    if (error) {
      log.error("could not fetch the source");
    } else if (!error && response.statusCode === 200) {
      const $ = cheerio.load(html);

      $('article[class="search-result row"]').each((index, element) => {
        const article_link =
          "https://www.anandabazar.com" +
          $(element).find('a[class = "thumbnail"]').attr("href").trim();

        // Now get only the links that contains the word 'short-story'
        if (article_link.search("short-story") !== -1) {
          log.start(article_link);
          crawl_a_story(article_link);
        }
      });
    }
  });
}

function crawl_a_story(story_url) {
  const options = { url: story_url, headers: { "User-Agent": "request" } };

  request.get(options, (error, response, html) => {
    if (error) {
      log.error("could not fetch the source");
    } else if (!error && response.statusCode === 200) {
      log.success("successfully fetched");
      const $ = cheerio.load(html);

      const story_name = $('div[class="col-12 abp-storypage-headline"]')
        .text()
        .trim();
      const story_name_html = "<h1 align=center>" + story_name + "</h1>\n";

      const author = $('ul[class="author"]').text().trim();
      const author_html = "<h2 align=center>" + author + "</h2>\n";

      // Check if this already exists don't inlude it again
      if (fs.existsSync("./stories/" + story_name.replace(/ /g, "-") + ".md")) {
        log.info("File already exists");
        return;
      }

      try {
        const img_div = $('div[id="abp-storypage-img-section"]');
        var img_src = img_div.find('img[class="img-fluid"]').attr("src"); // Returns with leading '//'
        img_src = img_src.slice(2);
      } catch {
        return;
      }

      const readme_entry = story_name + " - " + author;
      const readme_entry_text =
        "1. [ " +
        readme_entry +
        " ](./stories/" +
        story_name.replace(/ /g, "-") +
        ".md)\n";
      fs.appendFileSync("./README.md", readme_entry_text);
      // Download image
      const image = "http://" + img_src;

      const options2 = { url: image, headers: { "User-Agent": "request" } };

      request(image, options2)
        .pipe(
          fs.createWriteStream(
            "./metadata/images/" + story_name.replace(/ /g, "-") + ".jpg"
          )
        )
        .on("close", () => {
          log.success(story_name.replace(/ /g, "-") + ".jpg created");
          const img_html =
            '<div align=center> <img src="./../metadata/images/' +
            story_name.replace(/ /g, "-") +
            '.jpg" align="center" ></div>\n';

          let story_html = "";
          $(
            "div[class='col-12 abp-storypage-articlebody abp-videoarticle-content']"
          )
            .find("p")
            .each((index, element) => {
              if (index != 0) {
                if (
                  $(element).html().trim().search("feedback@abpdigital.in") ==
                  -1
                ) {
                  story_html =
                    story_html + "<br> <br>" + $(element).html().trim();
                }
              } else if (index == 0) {
                story_html = $(element).html().trim();
              }
            });

          const out_stream = fs.createWriteStream(
            "./stories/" + story_name.replace(/ /g, "-") + ".md"
          );
          out_stream.write(img_html);
          out_stream.write(story_name_html);
          out_stream.write(author_html);
          out_stream.write(story_html);

          // Out_stream.destroy();
          log.success(story_name.replace(/ /g, "-") + ".md created");

          const metadata = {};
          metadata.url = story_url;
          metadata.author = author;
          metadata.crawl_date = new Date();

          const json_stream = fs.createWriteStream(
            "./metadata/" + story_name.replace(/ /g, "-") + ".json"
          );
          json_stream.write(JSON.stringify(metadata));
          log.success(story_name.replace(/ /g, "-") + ".json created");

          // Json_stream.destroy();
          log.complete();
        });
    }
  });
}
