
const request = require('request');
const cheerio = require('cheerio');
const log = require('signale');
const fs = require('fs');

module.exports.crawl_a_story = function crawl_a_story(story_url) {
  var options = {url : story_url, headers : {'User-Agent' : 'request'}};

  request.get(options, (error, response, html) => {
    if (error) {
      log.error("could not fetch the source");
      return;
    } else if (!error && response.statusCode === 200) {

      log.success("successfully fetched");
      const $ = cheerio.load(html);
      var story_name = "";
      var author = "";

      try {

        story_name =
            $('div[class="col-12 abp-storypage-headline"]').text().trim();
        author = $('ul[class="author"]').text().trim();

      } catch (error) {
        return;
      }

      var story_name_html = '<h1 align=center>' + story_name + '</h1>\n';
      var author_html = '<h2 align=center>' + author + '</h2>\n';

      var img_div = "";
      var img_src = "";

      try {
        img_div = $('div[id="abp-storypage-img-section"]');
        img_src = img_div.find('img[class="img-fluid"]')
                      .attr('src'); // returns with leading '//'

      } catch (err) {
        log.info("NO IMAGE FOUND... " + err);
        img_src = "";
      }
      if (img_src === undefined) {
        no_image = true;
        return;
      }
      img_src = img_src.substr(2);

      // check if this already exists don't inlude it again
      if (fs.existsSync('./metadata/rabibasariya/' +
                        story_name.replace(/ /g, "-") + ".json")) {
        var check = fs.readFileSync('./metadata/rabibasariya/' +
                                        story_name.replace(/ /g, "-") + ".json",
                                    {encoding : 'utf8', flag : 'r'});
        var data = JSON.parse(check);

        if (data.author.trim() === author) {
          log.warn("story already exist");
          return;
        }
        story_name += "_" + author;
      }

      var readme_entry = story_name.split("_", 1)[0] + " - " + author;
      var readme_entry_text = "1.  [ " + readme_entry +
                              " ](./stories/rabibasariya/" +
                              story_name.replace(/ /g, "-") + ".md)\n";
      fs.appendFileSync('./README.md', readme_entry_text);

      // download image
      var image = "http://" + img_src;

      var options2 = {url : image, headers : {'User-Agent' : 'request'}};

      if (!no_img) {

        request(image, options2)
            .pipe(fs.createWriteStream('./metadata/images/rabibasariya/' +
                                       story_name.replace(/ /g, "-") + '.jpg'))
            .on('close', () => {
              log.success(story_name.replace(/ /g, "-") + '.jpg created');
              if (!no_img) {
                return;
                var img_html =
                    '<div align=center> <img src="./../../metadata/images/rabibasariya/' +
                    story_name.replace(/ /g, "-") +
                    '.jpg" align="center" ></div>\n';
              }

              var story_html = "";
              $("div[class='col-12 abp-storypage-articlebody abp-videoarticle-content']")
                  .find('p')
                  .each(function(index, element) {
                    stry_elm = $(element).html().trim();
                    if (index != 0) {
                      if (stry_elm.search('feedback@abpdigital.in') == -1 ||
                          stry_elm.search('rabibasariya@abp.in') == -1 ||
                          stry_elm.search('YouTube Channel') == -1) {
                        story_html = story_html + '<p>' + stry_elm + '</p>';
                      }
                    } else if (index == 0) {
                      story_html = '<div>' +
                                   '<p>' + stry_elm + '</p>';
                    }
                  });
              story_html += '</div>';
              var out_stream =
                  fs.createWriteStream('./stories/rabibasariya/' +
                                       story_name.replace(/ /g, "-") + '.md');
              out_stream.write(img_html);
              out_stream.write(story_name_html);
              out_stream.write(author_html);
              out_stream.write(story_html);

              log.success(story_name.replace(/ /g, "-") + '.md created')

              metadata = {};
              metadata.url = story_url;
              metadata.author = author;
              metadata.crawl_date = Date();

              var json_stream =
                  fs.createWriteStream('./metadata/rabibasariya/' +
                                       story_name.replace(/ /g, "-") + '.json');
              json_stream.write(JSON.stringify(metadata));
              log.success(story_name.replace(/ /g, "-") + '.json created');

              log.complete();
            });
      }
    }
  });
}
