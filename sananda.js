const request = require('request');
const cheerio = require('cheerio');
const log = require('signale');
const fs = require('fs');


if (!fs.existsSync('./stories')) {
    fs.mkdirSync('./stories');
}
if (!fs.existsSync('./stories/iexpress')) {
    fs.mkdirSync('./stories/iexpress');
}
if (!fs.existsSync('./metadata')) {
    fs.mkdirSync('./metadata');
}
if (!fs.existsSync('./metadata/iexpress')) {
    fs.mkdirSync('./metadata/iexpress');
}

if (!fs.existsSync('./metadata/images')) {
    fs.mkdirSync('./metadata/images');
}
if (!fs.existsSync('./metadata/images/iexpress')) {
    fs.mkdirSync('./metadata/images/iexpress');
}


const url = "https://bengali.indianexpress.com/about/bengali-short-story/";


var stories_id = [144609,142923,141659,140963,140024,139095,137920,134723,132915,129318,128632,127696,126143,125736,
124195,123808,122728,122087,121051,119334,118444,117754,117164,116450,114530,113742,112468,
108753,108138,106532,105549,104930,103900,103308,97145,95762,94021,92503,90156,88766,81596,80294,79331,
78136,76148];
var img_link = "https://api.sananda.in/image/journal/article?img_id=76148";





function crawl_a_story(story_url) {

    var options = {
        url: story_url,
        headers: {
            'User-Agent': 'request'
        }
    };

    request.get(options, (error, response, html) => {
        if (error) {
            log.error("could not fetch the source");
        }
        else if (!error && response.statusCode === 200) {
            log.success("successfully fetched");
            const $ = cheerio.load(html);

            var story_name = $('div[class="col-12 abp-storypage-headline"]').text().trim();

            var story_name_html = '<h1 align=center>' + story_name + '</h1>\n';

            var author = $('ul[class="author"]').text().trim();
            var author_html = '<h2 align=center>' + author + '</h2>\n';


            // check if this already exists don't inlude it again
            if (fs.existsSync('./stories/rabibasariya/' + story_name.replace(/ /g, "-") + ".md")) {
                log.info("File already exists");
                return;
            }

            var readme_entry = story_name + " - " + author;
            var readme_entry_text = "1.  [ " + readme_entry + " ](./stories/rabibasariya/" + story_name.replace(/ /g, "-") + ".md)\n";
            fs.appendFileSync('./README.md', readme_entry_text);


            var img_div = $('div[id="abp-storypage-img-section"]');
            var img_src = img_div.find('img[class="img-fluid"]').attr('src'); // returns with leading '//'
            img_src = img_src.substr(2);

            // download image
            var image = "http://" + img_src;

            var options2 = {
                url: image,
                headers: {
                    'User-Agent': 'request'
                }
            };

            request(image, options2).pipe(fs.createWriteStream('./metadata/images/rabibasariya/' + story_name.replace(/ /g, "-") + '.jpg')).on('close', () => {
                log.success(story_name.replace(/ /g, "-") + '.jpg created')
                var img_html = '<div align=center> <img src="./../../metadata/images/rabibasariya/' + story_name.replace(/ /g, "-") + '.jpg" align="center" ></div>\n';


                var story_html = "";
                $("div[class='col-12 abp-storypage-articlebody abp-videoarticle-content']").find('p').each(function (index, element) {
                    stry_elm = $(element).html().trim();
                    if (index != 0) {
                        if (stry_elm.search('feedback@abpdigital.in') == -1 || stry_elm.search('rabibasariya@abp.in') == -1 || stry_elm.search('YouTube Channel') == -1 ) {
                            story_html = story_html + '<p>' + stry_elm +'</p>';
                        }
                    } else if (index == 0) {
                        story_html = '<div>'+ '<p>' + stry_elm +'</p>';
                    }
                    
                });
                story_html += '</div>';
                var out_stream = fs.createWriteStream('./stories/rabibasariya/' + story_name.replace(/ /g, "-") + '.md');
                out_stream.write(img_html);
                out_stream.write(story_name_html);
                out_stream.write(author_html);
                out_stream.write(story_html);

                // out_stream.destroy();
                log.success(story_name.replace(/ /g, "-") + '.md created')

                metadata = {};
                metadata.url = story_url;
                metadata.author = author;
                metadata.crawl_date = Date();

                var json_stream = fs.createWriteStream('./metadata/rabibasariya/' + story_name.replace(/ /g, "-") + '.json');
                json_stream.write(JSON.stringify(metadata));
                log.success(story_name.replace(/ /g, "-") + '.json created');

                // json_stream.destroy();
                log.complete();
            });
        }
    });
}
